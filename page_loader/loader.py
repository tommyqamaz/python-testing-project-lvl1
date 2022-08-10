import os
from page_loader.loggers import Logger
from page_loader.utils import filter_name, scrap_images


def download(url_path: str, dir: str = "cwd", logger=Logger()):
    dir = os.getcwd() if dir == "cwd" else dir
    base_name = filter_name(url_path)
    html_name = base_name + ".html"
    path_to_save = os.path.join(dir, html_name)
    soup = scrap_images(url_path, dir)
    logger.save(soup.prettify(), path_to_save)  # creating file full_path
    logger.log(path_to_save)

    return path_to_save
