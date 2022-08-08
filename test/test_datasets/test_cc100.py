from pathlib import Path

import numpy as np
from squirrel_datasets_core.datasets.cc100 import CC100Driver

from mock_utils import create_random_str, save_xz


def mock_cc100_data(samples: int, tmp_path: Path) -> Path:
    """Create a dataset mock for cc100"""
    record = ""

    for _ in range(samples):
        l_str = np.random.randint(10, 100)
        record += create_random_str(l_str) + "\n\n"

    save_path = tmp_path / "record.txt.xz"
    save_xz(save_path, record[:-2])
    return save_path


def test_cc100(tmp_path: Path) -> None:
    """Unit test for cc100 driver with mocked data"""
    N = 10
    save_path = mock_cc100_data(N, tmp_path)

    config = {}
    config["af"] = save_path

    driver = CC100Driver(config)

    assert len(driver.select("af").get_iter().collect()) == N

    sample = driver.select("af").get_iter().take(1).collect()[0]
    assert sample["text"] is not None
    assert driver.available_languages == ["af"]
