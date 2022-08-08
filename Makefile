assembly: lint black install build package-install

start: install build package-install

black:
	poetry run black .

lint:
	poetry run flake8 .

install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov-report xml --cov-report term-missing --cov=gendiff tests/