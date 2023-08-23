SHELL := /bin/bash

install_dependencies:
	python3.10 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	source venv/bin/activate && pre-commit install --hook-type pre-push --hook-type post-checkout --hook-type pre-commit

run_precommit:
	pre-commit run --all-files

run_tests:
	# allows to run tests from the terminal using the 'make run_tests' command
	pytest tests/

