import json
from pathlib import Path

from squirrel_datasets_core.datasets.monthly_german_tweets.driver import (
    MonthlyGermanTweetsDriver,
)

from mock_utils import create_random_dict, save_gzip


def mock_german_tweets_data(samples: int, tmp_path: Path) -> None:
    """Create a dataset mock for german tweets"""
    record = "[\n "

    for _ in range(samples):
        content = json.dumps(
            create_random_dict(
                [
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
            )
        )
        record += f"{content},\n"

    record = record[:-2] + " \n]"
    save_path = tmp_path / "record.json.gz"
    save_gzip(save_path, record)


def test_german_tweets(tmp_path: Path) -> None:
    """Unit test for german tweets driver with mocked data"""
    N = 2
    mock_german_tweets_data(N, tmp_path)

    driver = MonthlyGermanTweetsDriver(tmp_path)
    assert len(driver.get_iter().collect()) == N

    sample = driver.get_iter().take(1).collect()[0]
    assert sample["type"] is not None
    assert sample["id"] is not None
    assert sample["user"] is not None
    assert sample["created_at"] is not None
    assert sample["recorded_at"] is not None
    assert sample["retweets"] is not None
    assert sample["favourites"] is not None
    assert sample["source"] is not None
    assert sample["lang"] is not None
    assert sample["hashtags"] is not None
    assert sample["urls"] is not None
    assert sample["mentions"] is not None
    assert sample["mentioned_ids"] is not None
    assert sample["refers_to"] is not None
