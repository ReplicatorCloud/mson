PYTHON_BIN ?= poetry run python

format: isort black
	exit 0

black:
	$(PYTHON_BIN) -m black --target-version py38 --exclude '/(\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|build|dist|node_modules|webpack_bundles)/' src tests

isort:
	$(PYTHON_BIN) -m isort src tests
