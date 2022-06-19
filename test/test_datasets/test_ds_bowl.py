from pathlib import Path
from typing import Iterator

import numpy as np
from squirrel_datasets_core.datasets.ds_bowl_2018.driver import (
    DataScienceBowl2018Driver,
)

from mock_utils import create_image, create_image_folder, create_random_name


def mock_ds_bowl_data(samples: int, tmp_path: Path) -> None:
    """Create a dataset mock for datascience bowl"""
    for _ in range(samples):
        random_str_train = create_random_name()
        random_str_test1 = create_random_name()
        random_str_test2 = create_random_name()

        create_image(tmp_path / "stage1_train" / random_str_train / "images", random_str_train, (256, 256))
        create_image_folder(tmp_path / "stage1_train" / random_str_train / "masks", np.random.randint(1, 5), (256, 256))

        create_image(tmp_path / "stage1_test" / random_str_test1 / "images", random_str_test1, (256, 256))
        create_image(tmp_path / "stage2_test_final" / random_str_test2 / "images", random_str_test2, (256, 256))


def test_ds_bowl_driver(tmp_path: Path) -> None:
    """Unit test for datascience bowl driver with mocked data"""
    N = 10
    mock_ds_bowl_data(N, tmp_path)

    driver = DataScienceBowl2018Driver(tmp_path)

    assert len(driver.get_iter("stage1_train").collect()) == N
    assert len(driver.get_iter("stage1_test").collect()) == N
    assert len(driver.get_iter("stage2_test_final").collect()) == N

    sample = driver.get_iter("stage1_train").take(1).collect()[0]
    assert sample["split"] == "stage1_train"
    assert sample["image"].shape == (256, 256, 4)
    assert sample["masks"][0].shape == (256, 256, 4)

    def _test_hook(it: Iterator) -> Iterator:
        for element in it:
            yield element
            break

    assert len(driver.get_iter("stage1_train", hooks=[_test_hook]).collect()) == 1
