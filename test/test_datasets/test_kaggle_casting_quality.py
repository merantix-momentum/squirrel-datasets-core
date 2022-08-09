from pathlib import Path
from typing import Iterator

from squirrel_datasets_core.datasets.kaggle_casting_quality.driver import (
    RawKaggleCastingQualityDriver,
)

from mock_utils import create_image_folder, create_random_str


def mock_casting_quality_data(samples: int, tmp_path: Path) -> None:
    """Create a dataset mock for casting quality"""
    image_names_test_ok = [create_random_str() for _ in range(samples)]
    image_names_train_ok = [create_random_str() for _ in range(samples)]
    image_names_test_def = [create_random_str() for _ in range(samples)]
    image_names_train_def = [create_random_str() for _ in range(samples)]

    create_image_folder(tmp_path / "train" / "ok_front", image_names_train_ok, (300, 300))
    create_image_folder(tmp_path / "train" / "def_front", image_names_train_def, (300, 300))
    create_image_folder(tmp_path / "test" / "ok_front", image_names_test_ok, (300, 300))
    create_image_folder(tmp_path / "test" / "def_front", image_names_test_def, (300, 300))


def test_casting_quality_driver(tmp_path: Path) -> None:
    """Unit test for casting quality driver with mocked data"""
    N = 10
    mock_casting_quality_data(N, tmp_path)
    driver = RawKaggleCastingQualityDriver(tmp_path)

    assert len(driver.get_iter("train").collect()) == N * 2
    assert len(driver.get_iter("test").collect()) == N * 2

    for sample in driver.get_iter("train"):
        assert sample["url"] is not None
        assert sample["label"] is not None
        assert sample["image"].shape == (300, 300, 4)

    def _test_hook(it: Iterator) -> Iterator:
        for element in it:
            if element["label"] == 0:
                yield element

    assert len(driver.get_iter("train", parse=False, hooks=[_test_hook]).collect()) == N
