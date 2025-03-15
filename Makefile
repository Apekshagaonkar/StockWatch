build: poetry.lock pyproject.toml
	python -m venv build/venv
	. build/venv/bin/activate && poetry install

test: build
	build/venv/bin/pytest -v --disable-warnings

run: build
	# Starts the server on port 8000 by default. This can be changed by setting UVICORN_PORT.
	build/venv/bin/uvicorn StockWatch.app:app --reload

clean:
	rm -rf build
