from unittest.mock import Mock
import requests_mock
import os
import tempfile
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
            f.write(value)


def test_loader():
    url = "https://ru.hexlet.io/courses"
    image_url = "https://ru.hexlet.io/courses/assets/professions/python.png"
    logger = FakeLogger()

    with open("tests/fixtures/before.html", "r") as f:
        before = f.read()

    with open("tests/fixtures/after.html", "r") as f:
        after = f.read()
    with open(
        "tests/fixtures/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-python.png",  # noqa E501
        "rb",
    ) as f:
        img = f.read()

    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock:
            mock.register_uri("GET", url, text=str(before))
            mock.register_uri("GET", image_url, content=img)
            other_urls = [
                "https://ru.hexlet.io/courses/courses",
                "https://ru.hexlet.io/courses/assets/application.css",
            ]
            for ou in other_urls:
                mock.register_uri("GET", ou, text="got it")
            result = download(url, dir=temp_dir)
            with open(result, "r") as f:
                res = f.read()
    assert res == after
    # assert logger.mock.call_count == 1
    # assert result == logger.mock.call_args.args[0]
