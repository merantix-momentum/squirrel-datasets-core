from pathlib import Path
from typing import Callable, Dict, Iterator, List, Tuple

import pytest
from squirrel_datasets_core.datasets.imagenet import RawImageNetDriver

from mock_utils import create_image_folder, create_random_str


def mock_imagenet_data(n_classes: int, tmp_path: Path) -> Tuple:
    """Create a dataset mock for imagenet"""
    n_val_images = 10
    n_test_images = 10
    n_train_images_per_class = 2

    val_image_names = [f"{create_random_str()}_{i:08d}" for i in range(n_val_images)]
    test_image_names = [f"{create_random_str()}_{i:08d}" for i in range(n_test_images)]
    train_image_names = [create_random_str() for _ in range(n_train_images_per_class)]

    cls_names = [f"n{create_random_str(5)}" for _ in range(n_classes)]

    create_image_folder(
        folder=tmp_path / "source/test",
        image_names=test_image_names,
        resolution=(256, 256),
        format="JPEG",
    )

    create_image_folder(
        folder=tmp_path / "source/val",
        image_names=val_image_names,
        resolution=(256, 256),
        format="JPEG",
    )

    for c_name in cls_names:
        create_image_folder(
            folder=tmp_path / f"source/train/{c_name}",
            image_names=train_image_names,
            resolution=(256, 256),
            format="JPEG",
        )

    return tmp_path / "source", cls_names, train_image_names, val_image_names, test_image_names


def mock_imagenet_cls_mapping(cls_names: List, tmp_path: Path) -> str:
    """Create a mock for imagenet class mappings"""
    txt_loc = tmp_path / "metadata/map_clsloc.txt"
    txt_loc.parent.mkdir(exist_ok=True, parents=True)

    with open(txt_loc, "w") as f:
        for i, name in enumerate(cls_names):
            f.write(f"{name} {i} {create_random_str(3)}\n")

    return txt_loc


def mock_location_info(image_names: List, cls_names: List, tmp_path: Path) -> str:
    """Create a mock for imagenet location labels"""
    txt_loc = tmp_path / "metadata/LOC_val_solution.csv"
    txt_loc.parent.mkdir(exist_ok=True, parents=True)

    with open(txt_loc, "w") as f:
        for i, name in enumerate(image_names):
            cls = cls_names[i % len(cls_names)]
            f.write(f"{name},{cls} 1 161 383 268\n")

    return txt_loc


def mock_cls_info(image_names: List, cls_names: List, tmp_path: Path) -> str:
    """Create a mock for imagenet class labels"""
    txt_loc = tmp_path / "metadata/ILSVRC2015_clsloc_validation_ground_truth.txt"
    txt_loc.parent.mkdir(exist_ok=True, parents=True)

    with open(txt_loc, "w") as f:
        for i, _ in enumerate(image_names):
            f.write(f"{i % len(cls_names)}\n")

    return txt_loc


def mock_blacklist_info(tmp_path: Path) -> str:
    """Create a mock for a blacklist"""
    txt_loc = tmp_path / "metadata/ILSVRC2015_clsloc_validation_blacklist.txt"
    txt_loc.parent.mkdir(exist_ok=True, parents=True)

    with open(txt_loc, "w") as f:
        f.write("0\n1")

    return txt_loc


@pytest.fixture
def imagenet_generate_data(tmp_path: Path) -> None:
    """Generate imagenet mock data"""
    N_CLASSES = 10

    source_path, cls_names, train_image_names, val_image_names, _ = mock_imagenet_data(N_CLASSES, tmp_path)
    mapping_url = mock_imagenet_cls_mapping(cls_names, tmp_path)
    val_loc_url = mock_location_info(val_image_names, cls_names, tmp_path)
    train_loc_url = mock_location_info(train_image_names, cls_names, tmp_path)
    val_cls_url = mock_cls_info(val_image_names, cls_names, tmp_path)
    blacklist_url = mock_blacklist_info(tmp_path)

    return {
        "source_path": source_path,
        "cls_val_mapping_url": val_cls_url,
        "loc_val_mapping_url": val_loc_url,
        "cls_mapping_url": mapping_url,
        "loc_train_mapping_url": train_loc_url,
        "val_blacklist_url": blacklist_url,
    }


def _assert_sample_correct(
    sample: Dict, cls_mapping_exists: bool, split_mapping_exists: bool, loc_mapping_exists: bool
) -> None:
    """Makes sure that the returned sample obeys the expected schema."""
    assert isinstance(sample["url"], str)
    assert (sample["image"] > 0).any()

    if not cls_mapping_exists:
        return

    if split_mapping_exists:
        assert type(sample["classification_label"]) == int
        assert type(sample["classification_label_name"]) == str
        assert type(sample["class_id"]) == str

    if loc_mapping_exists:
        assert type(sample["bboxes"]) == list
        for bbox in sample["bboxes"]:
            assert type(bbox["classification_label"]) == int
            assert type(bbox["classification_label_name"]) == str
            assert type(bbox["class_id"]) == str
            assert isinstance(bbox["loc"], list)
            assert len(bbox["loc"]) == 4
            for coord in bbox["loc"]:
                assert type(coord) == int


@pytest.mark.parametrize("use_hook", [True, False])
@pytest.mark.parametrize("parse", [True, False])
def test_raw_imagenet_driver_test_set(use_hook: bool, parse: bool, imagenet_generate_data: Callable) -> None:
    """Test imagenet driver loading raw imagenet dataset test samples."""
    source_path = imagenet_generate_data["source_path"]
    N_SAMPLES_TO_TAKE = 2

    def _test_hook(it: Iterator) -> Iterator:
        for element in it:
            yield element
            break

    hooks = None
    if use_hook:
        hooks = [_test_hook]

    imagenet_driver = RawImageNetDriver(url=source_path)
    samples = (
        imagenet_driver.get_iter(split="test", parse=parse, hooks=hooks, buffer_size=N_SAMPLES_TO_TAKE)
        .take(N_SAMPLES_TO_TAKE)
        .collect()
    )

    assert len(samples) == 1 if use_hook else N_SAMPLES_TO_TAKE

    if parse:
        for sample in samples:
            _assert_sample_correct(
                sample,
                cls_mapping_exists=False,
                split_mapping_exists=False,
                loc_mapping_exists=False,
            )


@pytest.mark.parametrize("use_cls_mapping_url", [True, False])
@pytest.mark.parametrize("use_loc_val_mapping_url", [True, False])
@pytest.mark.parametrize("use_cls_val_mapping_url", [True, False])
@pytest.mark.parametrize("use_val_blacklist_url", [True, False])
def test_raw_imagenet_driver_val_set(
    use_cls_mapping_url: bool,
    use_loc_val_mapping_url: bool,
    use_cls_val_mapping_url: bool,
    use_val_blacklist_url: bool,
    imagenet_generate_data: Callable,
) -> None:
    """Test imagenet driver loading raw imagenet dataset validation samples."""

    source_path = imagenet_generate_data["source_path"]
    N_SAMPLES_TO_TAKE = 2

    imagenet_driver = RawImageNetDriver(
        url=source_path,
        cls_mapping_url=imagenet_generate_data["cls_mapping_url"] if use_cls_mapping_url else None,
        loc_val_mapping_url=imagenet_generate_data["loc_val_mapping_url"] if use_loc_val_mapping_url else None,
        cls_val_mapping_url=imagenet_generate_data["cls_val_mapping_url"] if use_cls_val_mapping_url else None,
        val_blacklist_url=imagenet_generate_data["val_blacklist_url"] if use_val_blacklist_url else None,
    )
    samples = imagenet_driver.get_iter(split="val", buffer_size=N_SAMPLES_TO_TAKE).take(N_SAMPLES_TO_TAKE)

    for sample in samples:
        _assert_sample_correct(
            sample,
            cls_mapping_exists=use_cls_mapping_url,
            split_mapping_exists=use_cls_val_mapping_url,
            loc_mapping_exists=use_loc_val_mapping_url,
        )


@pytest.mark.parametrize("use_cls_mapping_url", [True, False])
@pytest.mark.parametrize("use_loc_train_mapping_url", [True, False])
def test_raw_imagenet_driver_train_set(
    use_cls_mapping_url: bool, use_loc_train_mapping_url: bool, imagenet_generate_data: Callable
) -> None:
    """Test imagenet driver loading raw imagenet dataset training samples."""
    source_path = imagenet_generate_data["source_path"]
    N_SAMPLES_TO_TAKE = 2

    imagenet_driver = RawImageNetDriver(
        url=source_path,
        cls_mapping_url=imagenet_generate_data["cls_mapping_url"],
        loc_train_mapping_url=imagenet_generate_data["loc_train_mapping_url"],
    )
    samples = imagenet_driver.get_iter(split="train", buffer_size=N_SAMPLES_TO_TAKE).take(N_SAMPLES_TO_TAKE)

    for sample in samples:
        _assert_sample_correct(
            sample,
            cls_mapping_exists=use_cls_mapping_url,
            split_mapping_exists=True,
            loc_mapping_exists=use_loc_train_mapping_url,
        )
