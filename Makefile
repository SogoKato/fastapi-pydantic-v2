run:
	rye run uvicorn main:app --reload

format:
	rye run isort . && rye run black .
