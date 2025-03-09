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


Learning from this project : 

- What compromises did you make due to time constraints?
  - Limited Historical Data – The API only retrieves data for the most recent 100 days by using outputsize: compact, instead of a full historical dataset.
  - Cache Concurrency Handling Not Implemented – The caching mechanism is basic and does not handle simultaneous requests modifying cache.
  - No Rate Limiting – The API does not enforce request rate limits, making it vulnerable to excessive requests.
  - No Authentication – The API does not restrict access, meaning anyone can access stock data without authorization.

  
- What would you do differently if this software was meant for production use?
  - Persistent and Concurrent Cache Handling – Store cached data in a database (Redis/PostgreSQL) instead of in-memory storage and implement concurrency control.
  - Rate Limiting – Use tools like FastAPI’s dependencies middleware or Redis-based rate limiting to prevent API abuse.
  - Authentication & Authorization – Restrict API access using API keys, OAuth, or JWT authentication to allow only authorized users.


- Propose how you might implement authentication, such that only authorized users may hit these endpoints.
  - Each user gets a unique API key.
  - Requests must include a valid key in the header.
  - Requests without a valid API key will be rejected with a 401 Unauthorized error.
  - API keys can be stored in a database and revoked when necessary.


- How much time did you spend on this exercise?
    -  Approximately 5 hours, covering:
      Understanding the problem, API, and tools (~1 hour)
      Researching FastAPI best practices (~30 minutes)
      Implementing the solution (~2 hours)
      Writing unit tests with pytest (~30 minutes)
      Debugging and refining (~30 minutes)
      Documenting the implementation (~30 minutes)

- Please include any other comments about your implementation.
  -  The project effectively demonstrates FastAPI, caching, and API interactions.
  - Unit tests provide reasonable coverage but could be expanded for edge cases.
  - The caching mechanism works but needs improvements for concurrent handling.

- Please include any general feedback you have about the exercise.
  - Covers real-world API design challenges (caching, rate limiting, data integrity). I really enjoyed this exercise and learned a lot.
