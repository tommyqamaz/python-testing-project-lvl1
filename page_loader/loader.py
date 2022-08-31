import os
from page_loader.utils import get_path_to_save, get_soup
from page_loader.scrap import replace_links


def download(url: str, dir: str = "cwd") -> str:
    """Downloades web page in html format and saves all content to dir directory

    Args:
        url_path (str): web url to save
        dir (str, optional): where to save. Defaults to "cwd".
        logger (_type_, optional): log the events (like saving, removing etc.).
                                    Defaults to Logger().

    Returns:
        str: path where content was saved
    """
    path_to_save = get_path_to_save(dir, url)
    soup = get_soup(url)
    soup = replace_links(soup)

    files_path = donwload_links(soup, dir)

    logger.log(path_to_save)

    return path_to_save
