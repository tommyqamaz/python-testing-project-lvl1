from typing import List, Tuple
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse
import os
import re
import requests
from page_loader.utils import filter_name, join_urls


def replace_links(
    soup: BeautifulSoup, base_url: str, save_dir: str = ""
) -> Tuple[BeautifulSoup, List[Tuple[str]]]:
    """Replace all links, images, css styles, scripts, etc.
    to local copies in beatiful soup html document.

    Example with url = "https://ru.hexlet.io/courses"
    before:
        <link href="/assets/application.css" media="all" rel="stylesheet"/>
        <img alt="Иконка профессии Python-программист"
         src="/assets/professions/python.png"/>
    after:
        <link href="ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css"
        media="all" rel="stylesheet"/>
        <img alt="Иконка профессии Python-программист"
        src="ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-python.png"/>

    Args:
        soup (BeautifulSoup): The original document in which
        you need to replace the links
        base_url (str): Origin url for soup.
        save_dir (str): Where to place replaced links.
    Returns:
        Tuple[BeautifulSoup, List[str]]: Soup with replaced links,
        list with Tuple, where first element is link and second one is file name
    """
    links = []

    for tag in soup.find_all(["link", "script", "img"]):
        link, attr = get_link(tag)
        if link:

            file_ext = get_file_ext(link)
            link_netloc = link.replace(file_ext, "")
            url_netloc = urlparse(base_url).netloc

            if link.startswith("/"):

                new_link = filter_name(join_urls(url_netloc, link_netloc)) + file_ext

                link_to_save = join_urls(base_url, link)
                links.append((link_to_save, new_link))

            elif url_netloc == urlparse(link).netloc:
                new_link = filter_name(link_netloc) + file_ext
                links.append((link_netloc + file_ext, new_link))
            else:
                continue  # we dont need to change or save other types of links
            save_dir = filter_name(base_url) + "_files"
            tag[attr] = join_urls(save_dir, new_link)

    return soup, links


def download_links(pairs: list, base_url, path_to_save=""):
    save_dir = filter_name(base_url) + "_files"
    os.mkdir(os.path.join(path_to_save, save_dir))
    for pair in pairs:
        url, name = pair
        content = get_content(url)
        save_content(
            content, os.path.join(path_to_save, save_dir, name)
        )  # ex: os.getcwd() + sitename-io + filename.ext


def get_content(url: str) -> str:
    res = requests.get(url)
    return res.content


def save_content(content: bytes, path_to_save: str):
    with open(f"{path_to_save}", "wb") as f:
        f.write(content)


def get_link(tag: Tag) -> Tuple[str]:
    for attr in ["href", "src"]:
        link = tag.attrs.get(attr)
        if link:
            return link, attr
    return None, None


def get_file_ext(link):
    file_ext = re.findall(r"\.[\w]*$", link)
    if not file_ext:
        return ".html"
    else:
        return file_ext[0]
