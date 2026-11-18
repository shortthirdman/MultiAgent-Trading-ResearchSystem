.PHONY: lint app coverage audit

lint:
	ruff check --fix .
	ruff format .

app:
	uv run streamlit run main.py

coverage:
	coverage run -m pytest
	coverage html

audit:
	uv run pip-audit