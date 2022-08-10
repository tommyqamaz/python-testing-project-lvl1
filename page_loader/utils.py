import re
import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse


def filter_name(url_path: str) -> str:
    """https://ru.hexlet.io/courses -> ru-hexlet-io-courses

    Args:
        url_path (str): path to transform

    Returns:
        str: modified url_path
    """

    url_path = re.sub(r"^http[s]?:/+", "", url_path)
    url_path = re.sub(r"(/+\b)|\.", "-", url_path)
    # we add \b because we don't want to replace the last slash
    # avoiding this situation: yandex-ru-.html
    url_path = url_path.replace("/", "")
    return url_path


def get_path_to_save(dir, url_path):
    dir = os.getcwd() if dir == "cwd" else dir
    base_name = filter_name(url_path)
    html_name = base_name + ".html"
    path_to_save = os.path.join(dir, html_name)
    return path_to_save


def join_urls(url1: str, url2: str) -> str:
    """Joins two urls into one

    Args:
        url1 (str): web adress 1
        url2 (str): web adress 1

    Returns:
        str: joined url
    """

    if url1.endswith("/"):
        url1 = url1[:-1]
    if url2.startswith("/"):
        url2 = url2[1:]
    return os.path.join(url1, url2)


def scrap_files(base_url: str, path: str = os.getcwd()) -> BeautifulSoup:
    """Downloades page and returns html page with downloaded files.

    Args:
        base_url (str): web adress
        path (str, optional): where to save. Defaults to os.getcwd().

    Returns:
        BeautifulSoup: modified soup
    """

    html_page = requests.get(base_url)
    soup = BeautifulSoup(html_page.content, "html.parser")
    # dir_name = filter_name(base_url) + "_files"
    dir_path = os.path.join(path, filter_name(base_url) + "_files")

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    soup = scrap_images(soup, base_url, dir_path)

    return soup


def scrap_images(soup: BeautifulSoup, base_url: str, dir_path: str) -> BeautifulSoup:
    """Scrap images from soup objescts and saves it in dir_path

    Args:
        soup (BeautifulSoup): soup object
        base_url (str): web url or host
        dir_path (str): where to save images

    Raises:
        RuntimeError: when receives status code distinct from 200

    Returns:
        BeautifulSoup: modified soup with replaced images src to local copies
    """

    dir_name = filter_name(base_url) + "_files"
    for image in soup.find_all("img"):
        image_url = join_urls(base_url, image["src"])
        response = requests.get(image_url)
        if response.status_code == 200:

            image_src = join_urls(
                urlparse(base_url).netloc.replace(".", "/"), image["src"]
            ).replace("/", "-")

            path_to_save = join_urls(dir_path, image_src)

            image["src"] = join_urls(dir_name, image_src)

            file = open(f"{path_to_save}", "wb")
            file.write(response.content)
            file.close()
        else:
            raise RuntimeError(response.status_code)

    return soup
