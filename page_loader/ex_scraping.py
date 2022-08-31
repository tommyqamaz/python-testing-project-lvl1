import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re

from page_loader.utils import filter_name, join_urls


def scrap_files(base_url: str, path: str = os.getcwd()) -> BeautifulSoup:
    """Downloades page and returns html page with downloaded files.

    Args:
        base_url (str): web adress
        path (str, optional): where to save. Defaults to os.getcwd().

    Returns:
        BeautifulSoup: modified soup
    """
    path = os.getcwd() if path == "cwd" else path
    html_page = requests.get(base_url)
    soup = BeautifulSoup(html_page.content, "html.parser")
    dir_path = os.path.join(path, filter_name(base_url) + "_files")

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    soup = scrap_content(soup, base_url, dir_path)
    return soup


def scrap_content(soup: BeautifulSoup, base_url: str, dir_path: str) -> BeautifulSoup:
    dir_name = filter_name(base_url) + "_files"
    url_netloc = urlparse(base_url).netloc
    for tag in soup.find_all(["link", "script", "img"]):
        tag_to_change, attr_in = get_tag_attrs(tag)

        if tag_to_change.startswith("/"):
            content_src = get_content_src(base_url, tag_to_change)
            content_url = join_urls(base_url, tag_to_change)

        else:
            attr_netloc = urlparse(tag_to_change).netloc
            if url_netloc == attr_netloc:
                content_src = filter_name(tag_to_change)
            else:
                continue  # we dont need to download content from other hosts

        response = requests.get(content_url)
        if response.status_code == 200:
            content_src = transfrom_content_src(content_src, dir_path)
            path_to_save = join_urls(dir_path, content_src)
            tag[attr_in] = join_urls(dir_name, content_src)

            save_content(path_to_save, response.content)

    return soup


def save_content(path_to_save: str, content: bytes) -> None:
    file = open(f"{path_to_save}", "wb")
    file.write(content)
    file.close()


def get_tag_attrs(tag):
    for attr in ["href", "src"]:
        if attr in tag.attrs:
            attr_in = attr
            tag_to_change = tag[attr]
    return tag_to_change, attr_in


def get_content_src(base_url, tag):
    src = join_urls(urlparse(base_url).netloc.replace(".", "/"), tag).replace("/", "-")
    return src


def transfrom_content_src(content_src: str, dir_path: str) -> str:
    content_src = re.sub(
        r"-(?=[\w]{1,4}$)", ".", content_src
    )  # replace '/' to '.' in the end of the string
    if "." not in content_src:
        content_src += ".html"
    return content_src
