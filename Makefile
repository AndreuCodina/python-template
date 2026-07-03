.PHONY: lint
lint:
	uv run -- ruff check
	uv run -- ruff format --diff
	uv run -- ty check