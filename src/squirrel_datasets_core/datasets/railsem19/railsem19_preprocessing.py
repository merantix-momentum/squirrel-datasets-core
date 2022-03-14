"""
This script can be used to extract the RailSem19 data and store it in a specified GCP location. The data
is found at `https://wilddash.cc/download`. You will need to download the files 'rs19_val.zip' and 'rs19_splits4000.zip'
and extract them into a <WORKDIR> that will be entered into the script at a later stage.

Please ensure you are compliant with the RailSem19 license before using the data.
"""
import typing as t
import os
from glob import glob
import gzip
import json
from collections import defaultdict
import concurrent.futures as fut

import gcsfs
from tqdm.auto import tqdm
from PIL import Image
import numpy as np
import fire


def write_to_gcp(shard: t.List[t.Dict[str, t.Any]], idx: int, split: str, gcp_project: str, gcp_location: str) -> None:
    """
    Write a shard of RailSem19 samples to a specified GCP project and location.

    Args:
        shard: A list of dictionaries containing the combined data and metadata of a RailSem19 sample.
        idx: integer specifying the number of the shard
        split: A string containing the split to extract. One of (val|test|train|additional)
        gcp_project: Project ID where to store the data
        gcp_location: bucket path to the storage location
    """

    fs = gcsfs.GCSFileSystem(project=gcp_project)
    with fs.open(os.path.join(gcp_location, split, f"{idx:05d}.jsonl.gz"), "wb") as fp:
        with gzip.GzipFile(fileobj=fp) as gz:
            for elem in tqdm(shard, leave=False, desc=f"Writing shard {idx}"):
                text = json.dumps(elem) + "\n"
                gz.write(text.encode("utf-8"))


def get_train_split(workdir: str) -> t.List[str]:
    """
    Load the train splits of the original 4000 image datasets.

    Args:
        workdir: full path to the folder containing the raw and extracted data sources
    """

    with open(os.path.join(workdir, "rs19_splits4000/train.txt")) as fp:
        train_splits = [line.strip() for line in fp.readlines()]
    return train_splits


def get_val_split(workdir: str) -> t.List[str]:
    """
    Load the validation splits of the original 4000 image datasets.

    Args:
        workdir: full path to the folder containing the raw and extracted data sources
    """

    with open(os.path.join(workdir, "rs19_splits4000/val.txt")) as fp:
        val_splits = [line.strip() for line in fp.readlines()]
    return val_splits


def get_test_split(workdir: str) -> t.List[str]:
    """
    Load the test splits of the original 4000 image datasets.

    Args:
        workdir: full path to the folder containing the raw and extracted data sources
    """

    with open(os.path.join(workdir, "rs19_splits4000/test.txt")) as fp:
        test_splits = [line.strip() for line in fp.readlines()]
    return test_splits


def get_data_index(workdir: str) -> t.Dict[str, t.Dict[str, str]]:
    """
    Construct the index that maps the ID of a RailSem19 sample to a dict containing the locations
    of all relevant data and metadata of that sample.

    Args:
        workdir: full path to the folder containing the raw and extracted data sources
    """

    data_index = defaultdict(dict)
    for elem in glob(os.path.join(workdir, "rs19_val/jsons/rs19_val/*")):
        fname = elem.split("/")[-1].split(".")[0]
        data_index[fname]["object_label"] = elem

    for elem in glob(os.path.join(workdir, "rs19_val/jpgs/rs19_val/*")):
        fname = elem.split("/")[-1].split(".")[0]
        data_index[fname]["image"] = elem

    for elem in glob(os.path.join(workdir, "rs19_val/uint8/rs19_val/*")):
        fname = elem.split("/")[-1].split(".")[0]
        data_index[fname]["segmentation_label"] = elem

    return data_index


def get_additional_splits(workdir: str) -> t.List[str]:
    """
    Load the additional splits not in the original 4000 image datasets.

    Args:
        workdir: full path to the folder containing the raw and extracted data sources
    """
    data_index = get_data_index(workdir)
    train_splits = get_train_split(workdir)
    val_splits = get_val_split(workdir)
    test_splits = get_test_split(workdir)
    additional_splits = []
    for k in data_index.keys():
        if k not in test_splits + val_splits + train_splits:
            additional_splits.append(k)

    return additional_splits


def load_record(r: t.Dict[str, str]) -> t.Dict[str, t.Any]:
    """
    Construct a single data record by loading all the relevant data and metadata and combining it
    into a single dictionary.

    Args:
        r: Dictionary containing the location of the segmentation masks,
            the image data and other metadata
    """

    objects = json.load(open(r["object_label"], "r"))

    rgb_image = np.array(Image.open(r["image"]))
    seg_mask = np.array(Image.open(r["segmentation_label"]))

    meta_data = {"frame": objects["frame"], "dtype": "uint8", "size": rgb_image.shape, "channel_order": "rgb"}

    return {
        "meta": meta_data,
        "objects": objects["objects"],
        "image": rgb_image.tolist(),
        "segmentation_mask": seg_mask.tolist(),
    }


def load_shard(sample_ids: t.List[str], id_data_locs: t.Dict[str, t.Dict[str, str]]) -> t.List[t.Dict[str, t.Any]]:
    """
    Load a shard of data records.

    Args:
        sample_ids: list of ids to be loaded into a shard.
        id_data_locs: Dictionary containing a map of the sample ID to the data and metadata information of the sample
    """

    return [load_record(id_data_locs[_id]) for _id in sample_ids]


def process_shard(
    sample_ids: t.List[str],
    id_data_locs: t.Dict[str, t.Dict[str, str]],
    shard_id: int,
    split: str,
    gcp_project: str,
    gcp_location: str,
) -> str:
    """
    Load a list of samples into a shard and write to GCP.

    Args:
        sample_ids: list of ids to be loaded into a shard.
        id_data_locs: Dictionary containing a map of the sample ID to the data and metadata information of the sample
        shard_id: integer specifying the number of the shard
        split: A string containing the split to extract. One of (val|test|train|additional)
        gcp_project: Project ID where to store the data
        gcp_location: bucket path to the storage location
    """

    sh = load_shard(sample_ids, id_data_locs)
    write_to_gcp(shard=sh, idx=shard_id, split=split, gcp_project=gcp_project, gcp_location=gcp_location)
    return f"success_{shard_id:03d}"


def main(split_key: str, workdir: str, gcp_project: str, gcp_location: str, num_workers: int = 4) -> None:
    """
    Main entrypoint to extract the RailSem19 dataset and split it into the different subsets.

    Args:
        split_key: A string containing the split to extract. One of (val|test|train|additional)
        workdir: full path to the folder containing the raw and extracted data sources
        gcp_project: Project ID where to store the data
        gcp_location: bucket path to the storage location
        num_workers: integer specifying the number of ProcessPoolExecutors
    """

    splits = {
        "val": get_val_split,
        "test": get_test_split,
        "train": get_train_split,
        "additional": get_additional_splits,
    }[split_key](workdir)

    data_index = get_data_index(workdir)
    _data_index_filtered = {k: v for k, v in data_index.items() if k in splits}
    shard_idx = np.asarray(splits).reshape(-1, 50).tolist()

    with fut.ProcessPoolExecutor(max_workers=num_workers) as pool:
        _futs = [
            pool.submit(process_shard, ids, _data_index_filtered, cntr, split_key, gcp_project, gcp_location)
            for cntr, ids in enumerate(shard_idx)
        ]
        with tqdm(total=len(_futs)) as pbar:
            for f in fut.as_completed(_futs):
                print(f.result())
                pbar.update()


if __name__ == "__main__":
    """
    To extract the RailSem19 dataset call

        python railsem19_preprocessing.py --split_key=<SPLIT> --workdir=<PATH TO RAW RS19 DATA>
                                          --gcp_project=<GCP PROJECT> --gcp_location=<GCP LOCATION>
    """
    fire.Fire(main)
