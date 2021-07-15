setup/dev:
	poetry install
	poetry shell

run/format:
	poetry run black .
	poetry run isort .

start:
	poetry run heimdall