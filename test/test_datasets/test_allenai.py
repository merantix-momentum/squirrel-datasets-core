import json
from collections import defaultdict
from pathlib import Path

from squirrel_datasets_core.datasets.allenai_c4 import C4DatasetDriver

from mock_utils import create_random_dict, save_gzip


def mock_allenai_data(samples: int, tmp_path: Path) -> None:
    """Create a dataset mock for allenai"""
    record = ""

    for _ in range(samples):
        record += json.dumps(create_random_dict(["text", "timestamp", "url"])) + "\n"

    save_path = tmp_path / "record.json.gz"
    save_gzip(save_path, record)
    return save_path


def test_allenai(tmp_path: Path) -> None:
    """Unit test for allenai c4 driver with mocked data"""
    N = 10
    save_path = mock_allenai_data(N, tmp_path)

    config = defaultdict(dict)
    config["zu"]["train"] = [save_path]

    driver = C4DatasetDriver(config)

    assert len(driver.select("zu", "train").get_iter().collect()) == N

    sample = driver.select("zu", "train").get_iter().take(1).collect()[0]
    assert sample["text"] is not None
    assert sample["timestamp"] is not None
    assert sample["url"] is not None
    assert driver.available_languages == ["zu"]
