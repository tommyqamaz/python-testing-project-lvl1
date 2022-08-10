import os
from page_loader.loggers import Logger
from page_loader.utils import filter_name, scrap_files, get_path_to_save


def download(url_path: str, dir: str = "cwd", logger=Logger()) -> str:
    """Downloades web page in html format and saves all content to dir directory

    Args:
        url_path (str): web url to save
        dir (str, optional): where to save. Defaults to "cwd".
        logger (_type_, optional): log the events (like saving, removing etc.).
                                    Defaults to Logger().

    Returns:
        str: path where all was saved
    """

    path_to_save = get_path_to_save(dir, url_path)
    soup = scrap_files(url_path, dir)
    logger.save(soup.prettify(), path_to_save)  # creating file full_path
    logger.log(path_to_save)

    return path_to_save
