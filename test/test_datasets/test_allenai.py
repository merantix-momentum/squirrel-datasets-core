import json
from collections import defaultdict
from pathlib import Path
from typing import Iterator, Tuple

import pytest
from squirrel_datasets_core.datasets.allenai_c4 import C4DatasetDriver

from mock_utils import create_random_dict, save_gzip


def mock_allenai_data(tmp_path: Path) -> Iterator[Tuple[str, str, int, Path]]:
    """Create a dataset mock for allenai"""
    for language, split, samples in [
        ("af", "train", 64),
        ("af", "valid", 1),
        ("am", "train", 3),
        ("am", "valid", 2),
        ("zu", "train", 5),
        ("zu", "valid", 5),
    ]:
        contents = [json.dumps(create_random_dict(["text", "timestamp", "url"])) for _ in range(samples)]
        record = "\n".join(contents)

        save_path = tmp_path / language / split / "record.json.gz"
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        save_gzip(save_path, record)
        yield (language, split, samples, save_path)


def test_allenai(tmp_path: Path) -> None:
    """Unit test for allenai c4 driver with mocked data"""
    mock_data = list(mock_allenai_data(tmp_path))
    config = defaultdict(dict)

    for language, split, _, save_path in mock_data:
        config[language][split] = [save_path]

    driver = C4DatasetDriver(config)

    for language, split, samples, _ in mock_data:
        assert len(driver.select(language, split).get_iter().collect()) == samples

        for sample in driver.select(language, split).get_iter():
            assert sample["text"] is not None
            assert sample["timestamp"] is not None
            assert sample["url"] is not None
            assert language in driver.available_languages

    assert len(driver.select().get_iter().collect()) == sum(
        samples for _, split, samples, _ in mock_data if split == "train"
    )
    with pytest.raises(ValueError):
        driver.select("en").get_iter().collect()
