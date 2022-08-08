import os
import requests
from page_loader.loggers import Logger
from page_loader.utils import filter_name


def download(url_path: str, dir: str = "cwd", logger=Logger()):
    dir = os.getcwd() if dir == "cwd" else dir
    name_to_save = filter_name(url_path)
    full_path = os.path.join(dir, name_to_save)
    content = requests.get(url_path).text
    logger.save(content, full_path)  # creating file full_path
    logger.log(full_path)

    return full_path
