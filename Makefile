.PHONY: check-code
check-code:
	uv run -- ruff check
	uv run -- ruff format --diff
	uv run -- ty check