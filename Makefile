
clear:
	-rm -r $(shell find . -name __pycache__) build dist .mypy_cache aioload.egg-info .eggs

build: clear
	python setup.py sdist bdist_wheel

upload_pypi: build
	pip install twine
	twine upload dist/*
