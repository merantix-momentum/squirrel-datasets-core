from pathlib import Path
from typing import Iterator

from squirrel_datasets_core.datasets.bdd100k import BDD100KDriver

from mock_utils import create_image_folder, create_random_str


def mock_bdd100k_data(samples: int, tmp_path: Path) -> None:
    """Create a dataset mock for bdd100k"""
    image_names_train = [create_random_str() for _ in range(samples)]
    image_names_test = [create_random_str() for _ in range(samples)]

    create_image_folder(tmp_path / "images/10k/train", image_names_train, (1280, 720))
    create_image_folder(tmp_path / "images/10k/test", image_names_test, (1280, 720))
    create_image_folder(tmp_path / "labels/sem_seg/masks/train", image_names_train, (1280, 720))


def test_bdd100k(tmp_path: Path) -> None:
    """Unit test for bdd100k driver (segmentation) with mocked data"""
    N = 10
    mock_bdd100k_data(N, tmp_path)
    driver = BDD100KDriver(tmp_path)

    assert len(driver.get_iter("train").collect()) == N
    assert len(driver.get_iter("test").collect()) == N

    sample = driver.get_iter("train").take(1).collect()[0]
    assert sample["image_url"][-5:] == sample["label_url"][-5:]
    assert sample["split"] == "train"
    assert sample["image"].shape == (1280, 720, 4)
    assert sample["label"].shape == (1280, 720, 4)

    def _test_hook(it: Iterator) -> Iterator:
        for element in it:
            yield element
            break

    assert len(driver.get_iter("test", hooks=[_test_hook], parse_label=False, parse_image=False).collect()) == 1
