import requests_mock
from page_loader.scrap import replace_links
from page_loader.utils import get_soup
from bs4 import BeautifulSoup


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
