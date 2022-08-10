import os
from page_loader.loggers import Logger
from page_loader.utils import filter_name, scrap_files


def download(url_path: str, dir: str = "cwd", logger=Logger()) -> str:
    """Downloades web page in html format and saves all content to dir directory

    Args:
        url_path (str): web url to save
        dir (str, optional): where to save. Defaults to "cwd".
        logger (_type_, optional): log the events (like saving, removing etc.). Defaults to Logger().

    Returns:
        str: path where all was saved
    """
    dir = os.getcwd() if dir == "cwd" else dir
    base_name = filter_name(url_path)
    html_name = base_name + ".html"
    path_to_save = os.path.join(dir, html_name)
    soup = scrap_files(url_path, dir)
    logger.save(soup.prettify(), path_to_save)  # creating file full_path
    logger.log(path_to_save)

    return path_to_save
