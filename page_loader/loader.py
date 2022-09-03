from page_loader.utils import get_soup, check_path_to_save
from page_loader.scrap import replace_links, download_links, save_content

import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel("INFO")


def download(url: str, dir: str = os.getcwd()) -> str:
    """Downloades web page in html format and saves all content to dir directory

    Args:
        url_path (str): web url to save
        dir (str, optional): where to save. Defaults to "cwd".

    Returns:
        str: path where content was saved
    """

    path_to_save = check_path_to_save(dir, url)
    if path_to_save is None:
        return
    soup = get_soup(url)
    if soup is None:
        return
    soup, pairs = replace_links(soup, url, dir)

    logger.info(f"write html file: {path_to_save}")
    save_content(soup.prettify(), path_to_save, mode="w")

    download_links(pairs, url, dir)
    return path_to_save
