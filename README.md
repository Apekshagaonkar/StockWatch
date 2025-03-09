# StockWatch

**StockWatch** is a Python-based backend project built with **FastAPI**. It will serve as an API to fetch stock price data from the **AlphaVantage API**.

Used AlphaVantage [TIME_SERIES_DAILY](https://www.alphavantage.co/documentation/#daily) API
endpoint as the source of prices. Got a free API key for AlphaVantage from [here](https://www.alphavantage.co/support/#api-key). 
Note : Limited to 25 calls per day.

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


8. Created the app.py file with the required endpoints and implemented the caching logic.
- Added StockAPI class to handle stock data fetching and caching from AlphaVantage API.
- Implemented the fetch_stock_data method to fetch stock data from the AlphaVantage API and cache the results.
- Implemented the lookup method to retrieve stock details for a specific date.
- Implemented the get_min and get_max methods to retrieve the lowest and highest prices for a given symbol and range 'n'.

9. Run `make run` to start the application.

10. execute curl command to test the endpoints.
    ```bash
    curl -X 'GET' 'http://127.0.0.1:8000/status' -H 'accept: application/json'

    output : {"app":"StockWatch"}%

    curl -X 'GET' 'http://127.0.0.1:8000/lookup?symbol=IBM&date=2025-03-06' -H 'accept: application/json'

    output : {"open":127.1000,"high":128.2900,"low":126.5300,"close":127.9600,"volume":3671903}

    curl -X 'GET' 'http://127.0.0.1:8000/min?symbol=IBM&n=5' -H 'accept: application/json'

    output : {"min":122.685}

    curl -X 'GET' 'http://127.0.0.1:8000/max?symbol=IBM&n=5' -H 'accept: application/json'

    output : {"max":128.93}

    # Error Response

    curl -X 'GET' 'http://127.0.0.1:8000/lookup?symbol=IBM&date=2023-01-01' -H 'accept: application/json'

    output : {"detail":"Data not available for the given date"}

    curl -X 'GET' 'http://127.0.0.1:8000/min?symbol=IBM&n=1000' -H 'accept: application/json'

    output : {"detail":"Requested range `n` exceeds available data"}

    curl -X 'GET' 'http://127.0.0.1:8000/max?symbol=IBM&n=1000' -H 'accept: application/json'

    output : {"detail":"Requested range `n` exceeds available data"}

    curl -X 'GET' 'http://127.0.0.1:8000/min?symbol=IBM&n=0' -H 'accept: application/json'

    output : {"detail":"Range `n` must be greater than 0"}

    curl -X 'GET' 'http://127.0.0.1:8000/max?symbol=IBM&n=0' -H 'accept: application/json'

    output : {"detail":"Range `n` must be greater than 0"}
    ```

11. Created the tests/test_app.py file with the required test cases.
- Added test cases for the lookup, min, and max endpoints.

12. Execute `make test` to run the tests.
    ```
      make test
      build/venv/bin/pytest -v -s --disable-warnings
      ================================================================================ test session starts ================================================================================
      platform darwin -- Python 3.12.9, pytest-7.4.4, pluggy-1.5.0 -- /Users/apekshagaonkar/Downloads/updated_backend_take_home_assessment_20250228/StockWatch/build/venv/bin/python
      cachedir: .pytest_cache
      rootdir: /Users/apekshagaonkar/Downloads/updated_backend_take_home_assessment_20250228/StockWatch
      plugins: cov-6.0.0, anyio-4.6.2.post1
      collected 13 items                                                                                                                                                                  

      tests/test_app.py::test_lookup_valid_date_cached Cache hit
      PASSED
      tests/test_app.py::test_lookup_invalid_date_cached Cache hit
      PASSED
      tests/test_app.py::test_get_min_valid_range_cached Cache hit
      PASSED
      tests/test_app.py::test_get_min_invalid_range_cached Cache hit
      PASSED
      tests/test_app.py::test_get_min_negative_range_cached PASSED
      tests/test_app.py::test_get_max_valid_range_cached Cache hit
      PASSED
      tests/test_app.py::test_get_max_invalid_range_cached PASSED
      tests/test_app.py::test_get_max_negative_range_cached PASSED
      tests/test_app.py::test_lookup_valid_date PASSED
      tests/test_app.py::test_lookup_invalid_date PASSED
      tests/test_app.py::test_get_min_valid_range PASSED
      tests/test_app.py::test_get_max_valid_range PASSED
      tests/test_app.py::test_cache_hit Cache hit 
      PASSED

      ========================================================================== 13 passed, 13 warnings in 0.65s ==========================================================================
    ```


13. Push the code to github
    ```bash
    git add .
    git commit -m "Message"
    git branch -M main
    git remote add origin https://github.com/apekshagaonkar/StockWatch.git
    git push -u origin main
    ```