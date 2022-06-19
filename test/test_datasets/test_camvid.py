from pathlib import Path
from typing import Iterator

from squirrel_datasets_core.datasets.camvid import CamvidDriver

from mock_utils import create_image_folder, create_random_name


def mock_camvid_data(samples: int, tmp_path: Path) -> None:
    """Create a dataset mock for camvid"""
    image_names_test = [create_random_name() for _ in range(samples)]
    image_names_train = [create_random_name() for _ in range(samples)]
    image_names_val = [create_random_name() for _ in range(samples)]

    create_image_folder(tmp_path / "test", image_names_test, (480, 360))
    create_image_folder(tmp_path / "testannot", image_names_test, (480, 360))
    create_image_folder(tmp_path / "train", image_names_train, (480, 360))
    create_image_folder(tmp_path / "trainannot", image_names_train, (480, 360))
    create_image_folder(tmp_path / "val", image_names_val, (480, 360))
    create_image_folder(tmp_path / "valannot", image_names_val, (480, 360))


def test_camvid_driver(tmp_path: Path) -> None:
    """Unit test for camvid driver with mocked data"""
    N = 10
    mock_camvid_data(N, tmp_path)
    driver = CamvidDriver(tmp_path)

    assert len(driver.get_iter("train").collect()) == N
    assert len(driver.get_iter("test").collect()) == N
    assert len(driver.get_iter("val").collect()) == N

    sample = driver.get_iter("train").take(1).collect()[0]
    assert sample["image_url"][-5:] == sample["label_url"][-5:]
    assert sample["split"] == "train"
    assert sample["image"].shape == (480, 360, 4)
    assert sample["label"].shape == (480, 360, 4)

    def _test_hook(it: Iterator) -> Iterator:
        for element in it:
            yield element
            break

    assert len(driver.get_iter("val", hooks=[_test_hook], parse_label=False, parse_image=False).collect()) == 1
