import re
import os
from bs4 import BeautifulSoup
import requests


def filter_name(url_path: str) -> str:
    """https://ru.hexlet.io/courses -> ru-hexlet-io-courses

    Args:
        url_path (str): path to transform

    Returns:
        str: modified url_path
    """

    url_path = re.sub(r"^http[s]?:/+", "", url_path)  # remove http/https
    url_path = re.sub(r"\b(/+\b)|\.", "-", url_path)  # replace dots and slashes
    # we add \b because we don't want to replace the last slash
    # avoiding this situation: yandex-ru-.html
    url_path = url_path.replace("/", "")
    return url_path


def get_path_to_save(dir: str, url_path: str) -> str:
    dir = os.getcwd() if dir == "cwd" else dir
    base_name = filter_name(url_path)
    html_name = base_name + ".html"
    path_to_save = os.path.join(dir, html_name)
    return path_to_save


def join_urls(url1: str, url2: str) -> str:
    """Joins two urls into one

    Args:
        url1 (str): web adress 1
        url2 (str): web adress 2

    Returns:
        str: joined url
    """

    if url1.endswith("/"):
        url1 = url1[:-1]
    if url2.startswith("/"):
        url2 = url2[1:]
    return os.path.join(url1, url2)


def get_soup(url: str) -> BeautifulSoup:
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, "html.parser")
    return soup
