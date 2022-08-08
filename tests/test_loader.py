import pytest
from unittest.mock import Mock

from page_loader import __version__
from page_loader import download


def test_version():
    assert __version__ == "0.1.0"


class FakeLogger:
    def __init__(self, mock=Mock()):
        self.mock = mock

    def log(self, value):
        self.mock(value)

    def save(self, value, path):
        with open(path) as f:
            f.write(value)


def test_logger():
    url = "https://ru.hexlet.io/courses"
    logger = FakeLogger()
    result = download(url, logger=logger)
    assert logger.mock.call_count == 1
    assert result == logger.mock.call_args.args[0]


def test_write():
    """check that utility downloads file to correct adress"""
    pass
