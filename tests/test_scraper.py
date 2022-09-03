import pytest
import os
import re
import tempfile

from bs4 import BeautifulSoup
import requests_mock
from urllib.parse import urlparse

from page_loader.scrap import replace_links, download_links
from page_loader.utils import get_soup, check_path_to_save


pairs = [
    (
        "https://ru.hexlet.io/courses/assets/application.css",
        "ru-hexlet-io-assets-application.css",
    ),
    ("https://ru.hexlet.io/courses/courses", "ru-hexlet-io-courses.html"),
    (
        "https://ru.hexlet.io/courses/assets/professions/python.png",
        "ru-hexlet-io-assets-professions-python.png",
    ),
    ("https://ru.hexlet.io/packs/js/runtime.js", "ru-hexlet-io-packs-js-runtime.js"),
]

url = "https://ru.hexlet.io/courses"


def test_download_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock:
            matcher = re.compile(urlparse(url).netloc)
            mock.register_uri("GET", matcher, content=b"content")
            download_links(pairs, url, temp_dir)
            dr = os.listdir(temp_dir)
            # assert os.getcwd() == temp_dir
            assert len(dr) == 1
            files = os.listdir(os.path.join(temp_dir, dr[0]))
            assert len(files) == 4
            for file in files:
                with open(f"{os.path.join(temp_dir, dr[0], file)}", "rb") as f:
                    content = f.read()
                assert content == b"content"


def test_replace_links():
    url = "https://ru.hexlet.io/courses"

    with open("tests/fixtures/before.html", "r") as f:
        before = f.read()

    with open("tests/fixtures/after.html", "r") as f:
        after = f.read()

        asoup_orig = BeautifulSoup(after, "html.parser")
        with requests_mock.Mocker() as mock:
            mock.register_uri("GET", url, text=str(before))
            bsoup = get_soup(url)
            asoup, _ = replace_links(bsoup, base_url=url, save_dir="")

    assert asoup_orig == asoup


cases = [
    ("https://ru.hexlet.io/courses/404", "404"),
    (
        "https://ods.ai/competitions/500",
        "500",
    ),
]


@pytest.mark.parametrize("some_url, status_code", cases)
def test_availability(some_url, status_code):
    with requests_mock.Mocker() as mock:
        mock.register_uri("GET", some_url, status_code=status_code)
        with pytest.raises(SystemExit) as ex:
            res = get_soup(some_url)
            assert res is None
            assert ex.value.code == 0


def test_check_path():
    os.makedirs("temp")
    res = check_path_to_save("temp", url)
    os.rmdir("temp")
    assert res == "temp/ru-hexlet-io-courses.html"
    with pytest.raises(SystemExit) as ex:
        res = check_path_to_save("not/existing/dir", url)
        assert ex.value.code == 0
