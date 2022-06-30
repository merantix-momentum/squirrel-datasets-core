from pathlib import Path

import numpy as np
from squirrel_datasets_core.driver.hub import HubDriver


def test_hub_driver(tmp_path: Path) -> None:
    """Test writing and reading using hub driver."""
    driver = HubDriver(str(tmp_path))

    # create dummy hub dataset
    SAMPLES = 10
    SPLIT = "train"
    with driver.get_hub(overwrite=True) as ds:
        ds.create_group(SPLIT)
        ds[SPLIT].create_tensor("image", htype="image", sample_compression="jpg")
        for _ in range(SAMPLES):
            ds[SPLIT].image.append(np.random.randint(0, 255, size=(32, 32, 3), dtype=np.uint8))

    # get iterstream from hub dataset
    it = driver.get_iter(SPLIT)
    i = 0
    for s in it:
        assert s["image"].numpy().shape == (32, 32, 3)
        i += 1
    assert i == SAMPLES
