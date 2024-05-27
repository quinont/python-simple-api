test:
	python3 -m pytest tests -p no:warnings
	python3 -m pytest --cov . -p no:warnings

install:
	pip3 install -r requirements.txt

linting:
	flake8 --max-line-length 100


.PHONY: test
