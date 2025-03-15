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
```poetry add --group dev black isort flake8``` 

    #### Tool Descriptions

    | Tool         | Purpose |
    |-------------|---------|
    | **black** | Auto-formats Python code to follow best practices. |
    | **isort** | Automatically sorts and organizes Python imports. |
    | **flake8** | Checks for syntax errors and style violations. |

4. Install Required Packages
  - run `make build` to build the project.
    - Sets up a virtual environment (build/venv/).
    - Installs project dependencies via Poetry.

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

10. Execute curl command to test the endpoints. **Tested on 9th March 2025**
    ```bash
    curl -X 'GET' 'http://127.0.0.1:8000/status' -H 'accept: application/json'

    output : {"app":"StockWatch"}

    curl -X 'GET' 'http://127.0.0.1:8000/lookup?symbol=IBM&date=2025-03-06' -H 'accept: application/json'

    {"open":249.75,"high":252.1,"low":246.8019,"close":248.69,"volume":3254358}

    curl -X 'GET' 'http://127.0.0.1:8000/min?symbol=IBM&n=5' -H 'accept: application/json'

    output : {"min":245.1823}

    curl -X 'GET' 'http://127.0.0.1:8000/max?symbol=IBM&n=5' -H 'accept: application/json'

    output : {"max":261.96}

    # Error Response

    curl -X 'GET' 'http://127.0.0.1:8000/lookup?symbol=IBM&date=2020-03-06' -H 'accept: application/json'

    output : {"detail":"Data not available for the given date"}

    curl -X 'GET' 'http://127.0.0.1:8000/max?symbol=IBM&n=10000' -H 'accept: application/json'

    output : {"detail":"Requested range `n` exceeds available data"}% 

    curl -X 'GET' 'http://127.0.0.1:8000/min?symbol=IBM&n=10000' -H 'accept: application/json'

    output : {"detail":"Requested range `n` exceeds available data"}

    curl -X 'GET' 'http://127.0.0.1:8000/max?symbol=IBM&n=0' -H 'accept: application/json'

    output : {"detail":"Range `n` must be greater than 0"}

    curl -X 'GET' 'http://127.0.0.1:8000/min?symbol=IBM&n=0' -H 'accept: application/json'

    output : {"detail":"Range `n` must be greater than 0"}
    ```

11. Created the tests/test_app.py file with the required test cases.
- Added test cases for the lookup, min, and max endpoints.

12. Execute `make test` to run the tests.
    ```
      make test 
      build/venv/bin/pytest -v --disable-warnings
      ======================================================================================== test session starts =========================================================================================
      platform darwin -- Python 3.12.9, pytest-7.4.4, pluggy-1.5.0 -- /Users/apekshagaonkar/Downloads/updated_backend_take_home_assessment_20250228/StockWatch/build/venv/bin/python
      cachedir: .pytest_cache
      rootdir: /Users/apekshagaonkar/Downloads/updated_backend_take_home_assessment_20250228/StockWatch
      plugins: cov-6.0.0, anyio-4.6.2.post1
      collected 13 items                                                                                                                                                                                   

      tests/test_app.py::test_lookup_valid_date_cached PASSED                                                                                                                                        [  7%]
      tests/test_app.py::test_lookup_invalid_date_cached PASSED                                                                                                                                      [ 15%]
      tests/test_app.py::test_get_min_valid_range_cached PASSED                                                                                                                                      [ 23%]
      tests/test_app.py::test_get_min_invalid_range_cached PASSED                                                                                                                                    [ 30%]
      tests/test_app.py::test_get_min_negative_range_cached PASSED                                                                                                                                   [ 38%]
      tests/test_app.py::test_get_max_valid_range_cached PASSED                                                                                                                                      [ 46%]
      tests/test_app.py::test_get_max_invalid_range_cached PASSED                                                                                                                                    [ 53%]
      tests/test_app.py::test_get_max_negative_range_cached PASSED                                                                                                                                   [ 61%]
      tests/test_app.py::test_lookup_valid_date PASSED                                                                                                                                               [ 69%]
      tests/test_app.py::test_lookup_invalid_date PASSED                                                                                                                                             [ 76%]
      tests/test_app.py::test_cache_hit PASSED                                                                                                                                                       [ 84%]
      tests/test_app.py::test_get_min_valid_range PASSED                                                                                                                                             [ 92%]
      tests/test_app.py::test_get_max_valid_range PASSED                                                                                                                                             [100%]

      ================================================================================== 13 passed, 13 warnings in 2.98s ===================================================================================
    ```
13. Run to format the code
    ```
    poetry run black .
    poetry run isort . --profile black
    poetry run flake8 .
    ```

14. Push the code to github
    ```bash
    git add .
    git commit -m "Message"
    git branch -M main
    git remote add origin https://github.com/apekshagaonkar/StockWatch.git
    git push -u origin main
    ```

Learnings from this project : 

- **What compromises did you make due to time constraints?**
  - **Limited Historical Data** – The API retrieves only the most recent 100 days of stock data using `outputsize=compact`, instead of fetching the full dataset.
  - **Cache Concurrency Handling Not Implemented** – The caching mechanism does not handle concurrent access, which could lead to race conditions.
  - **No Rate Limiting** – The API does not enforce request rate limits, making it susceptible to excessive requests.
  - **No Authentication** – The API does not restrict access, allowing unrestricted access to stock data.

- **What would you do differently if this software was meant for production use?**
  - **Use the full dataset** (`outputsize=full`) to provide a more complete historical analysis.
  - **Implement concurrent cache handling** using `asyncio.Lock` to prevent race conditions.
  - **Enforce rate limiting** using FastAPI middleware (`slowapi`).
  - **Implement authentication and authorization** using API keys to restrict access.

- **Propose how you might implement authentication, such that only authorized users may hit these endpoints.**
  - **Assign a Unique API Key** :Upon registration, each user receives a unique, cryptographically secure API key (e.g., generated via secrets.token_hex(32)).
  Store only a hashed version of this key (e.g., using hashlib.sha256()) in a secure database table with fields for api_key_hash, user_id, status, and expiration_date.
  - **Require API Key in the Authorization Header** : Clients must include the API key in the request header. Any request without a valid API key should be rejected with 401 Unauthorized.
  - **Validate and Revoke API Keys** : On every request, lookup the API key in the database (by comparing its hashed form). Check if the key is still active, not expired, or not revoked. If invalid, return 401 Unauthorized or 403 Forbidden (depending on the reason).
  - **Implement Key Expiry** : Assign an expiration date to each API key.

- **How much time did you spend on this exercise?**
  - Understanding the problem, API, and tools: **~1-2 hours**
  - Implementing the solution and writing unit tests (`pytest`): **~2 hours**
  - Debugging and refining: **~30 minutes**
  - Writing documentation and comments: **~30 minutes**

- **Please include any other comments about your implementation.**
  - The project effectively demonstrates **FastAPI, caching, and API interactions**.
  - Unit tests cover basic functionality but could be expanded for **edge cases**, such as ensuring the cache resets correctly at the start of a new day.
  - Implemented **cache cleanup** during API calls to prevent stale data from persisting.

- **Please include any general feedback you have about the exercise.**
  - This exercise effectively covers real-world API design considerations like **caching, authentication, rate limiting, and data integrity**. I found it engaging and insightful.

- **You will need a GitHub account for the next round. What is your GitHub username?**
  - [https://github.com/Apekshagaonkar](https://github.com/Apekshagaonkar)
