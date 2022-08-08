### Hexlet tests and linter status

[![Actions Status](https://github.com/tommyqamaz/python-testing-project-lvl1/workflows/hexlet-check/badge.svg)](https://github.com/tommyqamaz/python-testing-project-lvl1/actions)
![Project-check](https://github.com/tommyqamaz/python-project-lvl2/actions/workflows/project-check.yml/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/93182c28d1d412d5ca63/maintainability)](https://codeclimate.com/github/tommyqamaz/python-testing-project-lvl1/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/93182c28d1d412d5ca63/test_coverage)](https://codeclimate.com/github/tommyqamaz/python-testing-project-lvl1/test_coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Usage

### As external library

```python
from page_loader import download

file_path = download('https://ru.hexlet.io/courses', '/var/tmp')
print(file_path)  # => '/var/tmp/ru-hexlet-io-courses.html'
```

### As CLI tool

```
# по умолчанию output это os.getcwd()
page-loader --output /var/tmp https://ru.hexlet.io/courses
/var/tmp/ru-hexlet-io-courses.html  # путь к загруженному файлу
```
