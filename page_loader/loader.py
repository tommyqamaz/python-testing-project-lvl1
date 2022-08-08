import os
import requests
from typing import Callable
from page_loader.loggers import Logger
from page_loader.utils import filter_name


def download(url_path: str, dir: str = os.getcwd(), logger=Logger):
    name_to_save = filter_name(url_path)
    full_path = os.path.join(dir, name_to_save)
    downloaded_file = "file :)"  # requests.get(full_path).text

    logger.log(full_path)
    logger.save(downloaded_file, full_path)

    return full_path
