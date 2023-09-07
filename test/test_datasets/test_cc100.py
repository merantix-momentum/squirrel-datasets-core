from pathlib import Path

import numpy as np
import pytest
from squirrel.catalog import Catalog

from mock_utils import create_random_str, save_xz
from squirrel_datasets_core.datasets.cc100 import CC100Driver
from squirrel_datasets_core.datasets.cc100.constants import CC_100_CONFIG


def mock_cc100_data(samples: int, tmp_path: Path) -> Path:
    """Create a dataset mock for cc100"""
    record = "\n\n".join([create_random_str(np.random.randint(10, 100)) for _ in range(samples)]) + "\n\n"
    save_path = tmp_path / "record.txt.xz"
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    save_xz(save_path, record[:-2])
    return save_path


def test_cc100(tmp_path: Path) -> None:
    """Unit test for cc100 driver with mocked data"""
    N_af = 10
    N_am = 15

    save_path_af = mock_cc100_data(N_af, tmp_path / "af")
    save_path_am = mock_cc100_data(N_am, tmp_path / "am")

    config = {}
    config["af"] = save_path_af
    config["am"] = save_path_am

    driver = CC100Driver(config)

    assert len(driver.select("af").get_iter().collect()) == N_af
    assert len(driver.select("am").get_iter().collect()) == N_am
    assert "af" in driver.available_languages
    assert "am" in driver.available_languages

    for sample in driver.select("af").get_iter():
        assert sample["text"] is not None

    assert len(driver.select().get_iter().collect()) == 25

    with pytest.raises(KeyError):
        driver.select("en").get_iter().collect()


@pytest.mark.skip(reason="Dataset is on public storage.")
def test_cc100_public_data(plugin_catalog: Catalog) -> None:
    """Test loading a single language from the CC100 corpus."""
    driver: CC100Driver = plugin_catalog["cc100"].get_driver()
    assert sorted(driver.available_languages) == sorted(CC_100_CONFIG.keys())

    TAKE = 10
    it = driver.select("as").get_iter(shuffle_key_buffer=1, shuffle_item_buffer=1, prefetch_buffer=1)
    data = it.take(TAKE).tqdm().collect()
    assert len(data) == TAKE
