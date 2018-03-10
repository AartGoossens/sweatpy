test:
	pytest

# make build should eventually replace make test in the automated tests/builds
build: test
	isort -rc .

coverage:
	coverage run --source=sweat -m pytest --
	coverage report
	coverage html

isort:
	isort --skip=venv
