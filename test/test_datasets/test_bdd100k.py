from pathlib import Path
from typing import Iterator, Tuple

import pytest
from squirrel_datasets_core.datasets.bdd100k import BDD100KDriver

from mock_utils import create_image_folder, create_random_str


def mock_bdd100k_data(samples: int, tmp_path: Path, image_shape: Tuple) -> None:
    """Create a dataset mock for bdd100k"""
    image_names_train = [create_random_str() for _ in range(samples)]
    image_names_test = [create_random_str() for _ in range(samples)]

    create_image_folder(tmp_path / "images/10k/train", image_names_train, image_shape)
    create_image_folder(tmp_path / "images/10k/test", image_names_test, image_shape)
    create_image_folder(tmp_path / "labels/sem_seg/masks/train", image_names_train, image_shape)


@pytest.mark.parametrize("parse_label", [True, False])
@pytest.mark.parametrize("parse_image", [True, False])
@pytest.mark.parametrize("split", ["train", "test"])
def test_bdd100k(tmp_path: Path, parse_label: bool, parse_image: bool, split: str) -> None:
    """Unit test for bdd100k driver (segmentation) with mocked data"""
    N = 10
    image_shape = (1280, 720)

    mock_bdd100k_data(N, tmp_path, image_shape)
    driver = BDD100KDriver(tmp_path)

    assert len(driver.get_iter(split).collect()) == N

    for sample in driver.get_iter(split):
        assert sample["split"] == split
        assert sample["image"].shape == image_shape + (4,)

        if split == "train":
            # labels exist
            assert Path(sample["image_url"]).stem == Path(sample["label_url"]).stem
            assert sample["label"].shape == image_shape + (4,)

    def _test_hook(it: Iterator) -> Iterator:
        for element in it:
            yield element
            break

    assert (
        len(driver.get_iter(split, hooks=[_test_hook], parse_label=parse_label, parse_image=parse_image).collect()) == 1
    )
