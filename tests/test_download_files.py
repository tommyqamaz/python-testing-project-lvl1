from page_loader.scrap import download_links
import requests_mock
import tempfile
import re
from urllib.parse import urlparse
import os


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
            assert len(os.listdir(os.path.join(temp_dir, dr[0]))) == 4
            for file in os.listdir(os.path.join(temp_dir, dr[0])):
                with open(f"{os.path.join(temp_dir, dr[0], file)}", "rb") as f:
                    content = f.read()
                assert content == b"content"
