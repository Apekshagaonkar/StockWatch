# StockWatch

**StockWatch** is a Python-based backend project built with **FastAPI**. It will serve as an API to fetch stock price data from the **AlphaVantage API**.

## Getting Started

1. To get started, install the following:
    - [Python 3.12](https://docs.python.org/3.12/)
    - [Poetry](https://python-poetry.org/)
    - [Make](https://www.gnu.org/software/make/)

2. Initialize the Project with Poetry \
  ```poetry init``` 

3. Installed additional package for development setup. \
```poetry add --group dev pytest-cov black isort flake8 bandit safety``` 

    #### Tool Descriptions

    | Tool         | Purpose |
    |-------------|---------|
    | **pytest-cov** | Measures test coverage when running `pytest`. |
    | **black** | Auto-formats Python code to follow best practices. |
    | **isort** | Automatically sorts and organizes Python imports. |
    | **flake8** | Checks for syntax errors and style violations. |
    | **bandit** | Scans Python code for security vulnerabilities. |
    | **safety** | Checks installed dependencies for known security issues. |

4. Install Required Packages
  - run `make build` to build the project.
    - Set up a virtual environment (build/venv/).
    - Install project dependencies via Poetry.

5. Setting up github for the project. 
  - Initialised git repository ```git init``` 
  - Added .gitignore file ```touch .gitignore``` and updated it referencing https://www.toptal.com/developers/gitignore/api/python.

6. Installed the requests package for the http requests to the AlphaVantage API. 
- Added requests in pyproject.toml
- ```poetry update requests``` to lock the version

7. Added API_KEY of the AlphaVantage API in .env
- Added python-dotenv to pyproject.toml
- ```poetry update python-dotenv``` to lock the version

8. Run `make run` to start the application.

9. Execute `make test` to run the tests.
```
make test
build/venv/bin/pytest -v
================================================================================ test session starts ================================================================================
platform darwin -- Python 3.12.9, pytest-7.4.4, pluggy-1.5.0 -- /Users/apekshagaonkar/Downloads/updated_backend_take_home_assessment_20250228/StockWatch/build/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/apekshagaonkar/Downloads/updated_backend_take_home_assessment_20250228/StockWatch
plugins: cov-6.0.0, anyio-4.6.2.post1
collected 1 item                                                                                                                                                                    

tests/test_app.py::test_pass PASSED                                                                                                                                           [100%]

================================================================================= 1 passed in 0.01s =================================================================================

```

execute curl command to test the endpoints.
```bash
curl -X 'GET' 'http://127.0.0.1:8000/status' -H 'accept: application/json'

output : {"app":"StockWatch"}%
```

Push the code to github
```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/apekshagaonkar/StockWatch.git
git push -u origin main
```
