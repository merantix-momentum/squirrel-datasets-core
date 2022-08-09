from pathlib import Path
from typing import Iterator, Tuple

from squirrel_datasets_core.datasets.camvid import CamvidDriver

from mock_utils import create_image_folder, create_random_str


def mock_camvid_data(samples: int, tmp_path: Path, shape: Tuple) -> None:
    """Create a dataset mock for camvid"""
    image_names_test = [create_random_str() for _ in range(samples)]
    image_names_train = [create_random_str() for _ in range(samples)]
    image_names_val = [create_random_str() for _ in range(samples)]

    create_image_folder(tmp_path / "test", image_names_test, shape)
    create_image_folder(tmp_path / "testannot", image_names_test, shape)
    create_image_folder(tmp_path / "train", image_names_train, shape)
    create_image_folder(tmp_path / "trainannot", image_names_train, shape)
    create_image_folder(tmp_path / "val", image_names_val, shape)
    create_image_folder(tmp_path / "valannot", image_names_val, shape)


def test_camvid(tmp_path: Path) -> None:
    """Unit test for camvid driver with mocked data"""
    N = 10
    shape = (480, 360)

    mock_camvid_data(N, tmp_path, shape)
    driver = CamvidDriver(tmp_path)

    assert len(driver.get_iter("train").collect()) == N
    assert len(driver.get_iter("test").collect()) == N
    assert len(driver.get_iter("val").collect()) == N

    for sample in driver.get_iter("train"):
        assert Path(sample["image_url"]).stem == Path(sample["label_url"]).stem
        assert sample["split"] == "train"
        assert sample["image"].shape == shape + (4,)
        assert sample["label"].shape == shape + (4,)

    def _test_hook(it: Iterator) -> Iterator:
        for element in it:
            yield element
            break

    assert len(driver.get_iter("val", hooks=[_test_hook], parse_label=False, parse_image=False).collect()) == 1
