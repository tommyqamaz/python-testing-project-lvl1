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

    html_page = requests.get(base_url)
    soup = BeautifulSoup(html_page.content, "html.parser")
    # dir_name = filter_name(base_url) + "_files"
    dir_path = os.path.join(path, filter_name(base_url) + "_files")

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    soup = scrap_images(soup, base_url, dir_path)
    soup = scrap_content(soup, base_url, dir_path)
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
        if image["src"].startswith("/"):
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


def scrap_content(soup: BeautifulSoup, base_url: str, dir_path: str) -> BeautifulSoup:
    dir_name = filter_name(base_url) + "_files"
    url_netloc = urlparse(base_url).netloc
    for tag in soup.find_all(["link", "script"]):
        for attr in ["href", "src"]:
            if attr in tag.attrs:
                attr_in = attr
                tag_to_change = tag[attr]
        if tag_to_change.startswith("/"):
            content_src = join_urls(
                url_netloc.replace(".", "/"), tag_to_change
            ).replace("/", "-")
            content_url = join_urls(base_url, tag_to_change)
        else:
            attr_netloc = urlparse(tag_to_change).netloc
            if url_netloc == attr_netloc:
                content_src = filter_name(tag_to_change)
            else:
                continue

        response = requests.get(content_url)

        if response.status_code == 200:
            content_src = re.sub(r"-(?=[\w]{1,4}$)", ".", content_src)
            if "." not in content_src:
                content_src += ".html"
            path_to_save = join_urls(dir_path, content_src)
            tag[attr_in] = join_urls(dir_name, content_src)

            file = open(f"{path_to_save}", "wb")
            file.write(response.content)
            file.close()

    return soup
