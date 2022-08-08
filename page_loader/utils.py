import re


def filter_name(url_path):
    """
    https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html

    """
    url_path = re.sub(r"^(https|http|):/+", "", url_path)
    url_path = re.sub(r"(/+)|\.", "-", url_path)
    return url_path + ".html"
