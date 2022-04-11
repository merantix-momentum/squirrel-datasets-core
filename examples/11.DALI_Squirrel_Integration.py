from __future__ import annotations

import time
import types
from collections import defaultdict
from typing import Any, Dict, List

import cupy
import numpy as np
import nvidia.dali.fn as fn
import nvidia.dali.types as types
import torch
from nvidia.dali import pipeline_def
from nvidia.dali.plugin.pytorch import DALIGenericIterator
from squirrel.catalog import Catalog
from squirrel.iterstream import Composable

#### INSTALLATION
# pip install cupy-cuda110 squirrel-core squirrel-datasets-core
# pip install --extra-index-url https://developer.download.nvidia.com/compute/redist --upgrade nvidia-dali-cuda110
#### INSTALLATION END

# some metadata for cifar100
BATCH_SIZE = 16
DS_SPLIT = "train"
DS = "cifar100"
DS_LEN = 50000
DS_VERSION = 1 # uses Huggingface version of the dataset
NUM_OUTPUTS = 3  # img, fine_label, coarse_label


def cupy_collate(records: List[Dict[str, Any]]) -> List[cupy.ndarray]:
    """Converts a batch of a list of dicts to a list of cupy arrays.

    Args:
        records (List[Dict[str, Any]]): A batch to convert.

    Returns:
        List[cupy.ndarray]: Re-formatted batch of cupy arrays. For CIFAR-100,
            this returns List[batch_imgs, batch_fine_labels, batch_coarse_labels].
    """
    batch = defaultdict(list)
    for elem in records:
        for k, v in elem.items():
            batch[k].append(np.array(v))
    return [cupy.asarray(np.array(v), dtype=np.uint8) for v in batch.values()]


class SquirrelGpuIterator(object):
    """External source iterator for a Squirrel driver. By using the cupy_collate function
    for batch collation, we support the cuda array interface. Hence, data is returned
    on the GPU. The below example was mainly based on the below tutorial.
    https://docs.nvidia.com/deeplearning/dali/user-guide/docs/examples/general/data_loading/external_input.html
    """

    def __init__(
        self,
        iterable: Composable,
        batch_size: int,
        ds_len: int,
    ):
        """Constructs the SquirrelGpuIterator.

        Args:
            iterable (Composable): A Squirrel iterable object you'd like to use with DALI.
            batch_size (int): How many samples are contained in one batch.
            ds_len (int): How many samples are in your dataset. We need to know this here, because, as of now,
                Squirrel drivers do not implement the __len__() method.
        """
        self.batch_size = batch_size
        self.it = iter(iterable.batched(self.batch_size, collation_fn=cupy_collate, drop_last_if_not_full=False))
        self.ds_len = ds_len

    def __iter__(self) -> SquirrelGpuIterator:
        """Returns the iterator and sets variables that DALI uses internally for tracking iteration progress.

        Returns:
            SquirrelGpuIterator: The iterator object.
        """
        self.i = 0
        self.n = self.ds_len
        return self

    def __next__(self) -> List[cupy.ndarray]:
        """Advances the index by batch_size and returns the next item of the iterator.

        Returns:
            List[cupy.ndarray]: The next batch of your dataset (on GPU).
        """

        self.i = (self.i + self.batch_size) % self.n
        return next(self.it)


cat = Catalog.from_plugins()
it = cat[DS][DS_VERSION].get_driver().get_iter(DS_SPLIT)
source = SquirrelGpuIterator(it, BATCH_SIZE, DS_LEN)


@pipeline_def
def pipeline():
    imgs, fine_labels, coarse_labels = fn.external_source(
        source=it,
        num_outputs=NUM_OUTPUTS,
        device="gpu",
        dtype=types.UINT8,
    )
    enhanced = fn.brightness_contrast(imgs, contrast=2)
    return enhanced, fine_labels, coarse_labels


pipe = pipeline(batch_size=BATCH_SIZE, num_threads=2, device_id=0)
pipe.build()

# this is the DALI equivalent of torch.utils.data.DataLoader
dali_iter = DALIGenericIterator([pipe], ["img", "fine_label", "coarse_label"])

print("Iterating over dataset ...")
t = time.time()
for idx, item in enumerate(dali_iter):
    if idx == 0:
        # item is a list of length 1
        assert type(item) == list
        assert len(item) == 1

        # let's see what's in the list, it's a dict with our data!
        data = item[0]
        assert type(data) == dict

        # the data is already in torch format and on GPU!
        assert type(data["img"]) == torch.Tensor
        assert data["img"].shape == torch.Size([BATCH_SIZE, 32, 32, 3])
        assert data["img"].device == torch.device("cuda:0")
        assert data["fine_label"].shape[0] == BATCH_SIZE

        print("Data in torch format!")

samples_ps = DS_LEN / (time.time() - t)
print(f"Iteration speed: {samples_ps} samples per second")

print("Done. Have a nice day.")
