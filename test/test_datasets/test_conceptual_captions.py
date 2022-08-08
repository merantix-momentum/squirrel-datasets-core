import io
import urllib
from typing import Any, Iterable
from unittest.mock import patch

import numpy as np
import requests
from PIL import Image
from squirrel_datasets_core.datasets.conceptual_captions.driver import CC12MDriver

from mock_utils import create_random_str

SHAPE = (10, 10, 3)


class MockImageResponse:
    calls = 0
    fail_n_times = 1

    def read(self) -> bytes:
        """Mock reading file. This method will be called for each url returned by MockTextResponse."""
        MockImageResponse.calls += 1
        if MockImageResponse.calls > 1 and MockImageResponse.calls < MockImageResponse.fail_n_times + 2:
            # test broken URL
            raise urllib.error.HTTPError(None, None, None, None, None)

        rand_img = np.random.randint(0, 255, size=SHAPE).astype(np.uint8)
        img_byte_arr = io.BytesIO()
        Image.fromarray(rand_img).save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return img_byte_arr.read()


class MockTextResponse:
    N_SAMPLES = 10

    def iter_lines(self) -> Iterable:
        """Mock iteratively fetching lines from web document"""
        for _ in range(MockTextResponse.N_SAMPLES):
            url, caption = f"https://{create_random_str()}", create_random_str()
            yield f"{url}\t{caption}".encode("utf-8")

    def __enter__(self, *args, **kwargs) -> Any:
        """Mock using block"""
        return self

    def __exit__(self, *args, **kwargs) -> None:
        """Mock using block"""
        pass


def open_url_mock(*args, **kwargs) -> MockImageResponse:
    """Get mock for loading files"""
    return MockImageResponse()


def requests_get_mock(*args, **kwargs) -> MockTextResponse:
    """Get mock for loading text with references"""
    return MockTextResponse()


@patch("urllib.request.urlopen", open_url_mock)
@patch("requests.get", requests_get_mock)
def test_read_from_mocks() -> None:
    """Test all the mocks themselves"""
    req = urllib.request.Request("http://test.png", headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    image = np.array(Image.open(resp))

    assert image.shape == SHAPE

    req = requests.get("some_url", stream=True)

    for line in req.iter_lines():
        line.decode("utf-8").split("\t")


@patch("urllib.request.urlopen", open_url_mock)
@patch("requests.get", requests_get_mock)
def test_conceptual_captions_driver() -> None:
    """Unit test for conceptual captions driver with mocked data"""
    driver = CC12MDriver("test")
    assert len(driver.get_iter().collect()) == MockTextResponse.N_SAMPLES - MockImageResponse.fail_n_times

    sample = driver.get_iter().take(1).collect()[0]
    assert sample["caption"] is not None
    assert sample["url"] is not None
    assert not sample["error"]
    assert sample["image"].shape == SHAPE
