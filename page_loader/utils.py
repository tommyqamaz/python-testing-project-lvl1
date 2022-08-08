import re


def filter_name(url_path):
    """
    https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html

    """
    url_path = re.sub(r"^(https|http|):/+", "", url_path)
    url_path = re.sub(r"(/+\b)|\.", "-", url_path)
    # we add \b because we don't want to replace the last slash
    # avoiding this situation: yandex-ru-.html
    url_path = url_path.replace("/", "")
    return url_path + ".html"
