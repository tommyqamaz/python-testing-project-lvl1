import re
import os
from bs4 import BeautifulSoup
import requests


def filter_name(url_path):
    """
    https://ru.hexlet.io/courses -> ru-hexlet-io-courses
    """
    url_path = re.sub(r"^http[s]?:/+", "", url_path)
    url_path = re.sub(r"(/+\b)|\.", "-", url_path)
    # we add \b because we don't want to replace the last slash
    # avoiding this situation: yandex-ru-.html
    url_path = url_path.replace("/", "")
    return url_path


def scrap_images(base_url: str, path: str = os.getcwd()) -> BeautifulSoup:
    """
    Downloades page and returns html page with replaced to local copies images.
    """

    html_page = requests.get(base_url)
    soup = BeautifulSoup(html_page.content, "html.parser")
    base_dir = os.path.join(path, filter_name(base_url) + "_files")

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for image in soup.find_all("img"):
        image_url = os.path.join(base_url, image["src"])
        response = requests.get(image_url)
        if response.status_code == 200:

            path_to_save = os.path.join(base_dir, filter_name(image_url))
            path_to_save = re.sub(r"-(?=[\w]*$)", ".", path_to_save)

            image["src"] = path_to_save

            file = open(f"{path_to_save}", "wb")
            file.write(response.content)
            file.close()
        else:
            raise RuntimeError(response.status_code)

    return soup, base_dir
