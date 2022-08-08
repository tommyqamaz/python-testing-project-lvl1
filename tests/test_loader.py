from unittest.mock import Mock
import requests_mock
import os

from page_loader import __version__
from page_loader import download


def test_version():
    assert __version__ == "0.1.0"


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        raise FileExistsError


class FakeLogger:
    def __init__(self, mock=Mock()):
        self.mock = mock

    def log(self, value):
        self.mock(value)

    def save(self, value, path):
        with open(path, "w") as f:
            # add tempfile
            f.write(value)


def test_logger():
    url = "https://ru.hexlet.io/courses"
    logger = FakeLogger()
    content = "res"
    with requests_mock.Mocker() as mock:
        mock.get(url, text=content)
        result = download(url, logger=logger)
        with open(result, "r") as f:
            res = f.read()
    assert res == content
    assert logger.mock.call_count == 1
    assert result == logger.mock.call_args.args[0]

    delete_file(result)
