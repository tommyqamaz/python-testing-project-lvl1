import pytest
from page_loader.utils import filter_name


all_cases = [
    ("https://ru.hexlet.io/courses", "ru-hexlet-io-courses"),
    (
        "https://ods.ai/competitions/dl-fintech-bki",
        "ods-ai-competitions-dl-fintech-bki",
    ),
    ("https://www.kinopoisk.ru/lists", "www-kinopoisk-ru-lists"),
    ("https://yandex.ru/", "yandex-ru"),
]


@pytest.mark.parametrize("url, expected", all_cases)
def test_cases(url, expected):
    result = filter_name(url)
    assert result == expected
