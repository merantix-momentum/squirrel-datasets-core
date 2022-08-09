import json
from pathlib import Path
from typing import List

from squirrel_datasets_core.datasets.monthly_german_tweets.driver import (
    MonthlyGermanTweetsDriver,
)

from mock_utils import create_random_dict, save_gzip


def mock_german_tweets_data(samples: int, tmp_path: Path, keys: List) -> None:
    """Create a dataset mock for german tweets"""
    contents = [json.dumps(create_random_dict(keys)) for _ in range(samples)]
    record = ",\n".join(contents)
    record = f"[\n{record}\n]"

    save_path = tmp_path / "record.json.gz"
    save_gzip(save_path, record)


def test_german_tweets(tmp_path: Path) -> None:
    """Unit test for german tweets driver with mocked data"""
    N = 2
    keys = [
        "type",
        "id",
        "user",
        "created_at",
        "recorded_at",
        "retweets",
        "favourites",
        "source",
        "lang",
        "hashtags",
        "urls",
        "mentions",
        "mentioned_ids",
        "refers_to",
    ]

    mock_german_tweets_data(N, tmp_path, keys)

    driver = MonthlyGermanTweetsDriver(tmp_path)
    assert len(driver.get_iter().collect()) == N

    for sample in driver.get_iter():
        for k in keys:
            assert sample[k] is not None
