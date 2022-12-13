import typing as t
from pathlib import Path

import deeplake
import hub
import numpy as np

from squirrel_datasets_core.driver.deeplake import DeeplakeDriver
from squirrel_datasets_core.driver.hub import HubDriver


def test_hub_driver(tmp_path: Path) -> None:
    """Test writing and reading using hub driver."""
    driver = HubDriver(str(tmp_path))
    empty_dataset = driver.get_hub(overwrite=True)
    _run_activeloop(driver, empty_dataset)


def test_deeplake_driver(tmp_path: Path) -> None:
    """Test writing and reading using deeplake driver."""
    driver = DeeplakeDriver(str(tmp_path))
    empty_dataset = deeplake.empty(tmp_path)
    _run_activeloop(driver, empty_dataset)


def _run_activeloop(
    driver: t.Union[DeeplakeDriver, HubDriver], empty_dataset: t.Union[deeplake.Dataset, hub.Dataset]
) -> None:
    """Tests both drivers for Activeloop hub as well as deeplake because they have similar APIs."""

    SAMPLES = 10
    SPLIT = "train"
    with empty_dataset as ds:
        ds.create_group(SPLIT)
        ds[SPLIT].create_tensor("image", htype="image", sample_compression="jpg")
        for _ in range(SAMPLES):
            ds[SPLIT].image.append(np.random.randint(0, 255, size=(32, 32, 3), dtype=np.uint8))

    # get iterstream from dataset
    it = driver.get_iter(SPLIT)
    i = 0
    for s in it:
        assert s["image"].numpy().shape == (32, 32, 3)
        i += 1
    assert i == SAMPLES
