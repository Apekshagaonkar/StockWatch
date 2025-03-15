import os
from datetime import datetime
from typing import Dict

import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"


class StockAPI:
    """Wrapper class for fetching and analyzing stock data using the Alpha Vantage API."""

    def __init__(self):
        """Initialize a new instance of the StockAPI class."""
        self.cache: Dict[str, Dict] = {}  # In-memory cache
        self.datetime = datetime.now()
        self.cache_hit = 0

    def _clear_cache(self):
        self.cache = {}
        self.cache_hit = 0

    def _fetch_stock_data(self, symbol: str, outputsize: str = "compact"):
        """
        Helper function to fetch stock prices for a given symbol from AlphaVantage API, using cache if available.

        :param symbol: The stock symbol for which to retrieve the data.
        :return: A dictionary containing the stock prices for the specified symbol.
        """
        # Check if the cache is expired match date with current date
        if self.datetime.date() != datetime.now().date():
            print("Cache expired")
            self._clear_cache()

        # Check if the symbol is already cached
        symbol = symbol.upper()
        if symbol in self.cache:
            print("Cache hit")
            self.cache_hit += 1
            return self.cache[symbol]

        # Fetch the stock data from AlphaVantage API
        params = {
            "function": "TIME_SERIES_DAILY",  # daily stock prices
            "symbol": symbol,  # Assuming its all uppercase
            "apikey": API_KEY,
            "outputsize": outputsize,  # default compact returns the last 100 days of data
            "datatype": "json",  # json is the default
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=20)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise HTTPException(status_code=504, detail="AlphaVantage API timeout")
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=500, detail="Failed to fetch stock data")

        # Parse the response
        data = response.json()

        if (
            "Information" in data
            and "our standard API rate limit is 25 requests per day"
            in data["Information"]
        ):
            raise HTTPException(status_code=429, detail="API rate limit exceeded")

        if "Time Series (Daily)" not in data:
            raise HTTPException(
                status_code=400, detail="Invalid symbol or API limit exceeded"
            )

        # Cache the response
        self.cache[symbol] = data["Time Series (Daily)"]
        return self.cache[symbol]

    def lookup(self, symbol: str, date: str):
        """
        Retrieve stock details like open, high, low, close, and volume for a specific symbol and date.

        :param symbol: The stock symbol for which to retrieve the data.
        :param date: The date for which to retrieve the data in the format "YYYY-MM-DD".
        :return: A dictionary containing the open, high, low, close, and volume for the specified symbol and date.
        """
        # Fetch the stock data
        stock_data = self._fetch_stock_data(symbol)

        # Check if the date is available in the stock data.
        # (market closure handling/ Date not in last 100 days / Future date
        if date not in stock_data:
            raise HTTPException(
                status_code=404, detail="Data not available for the given date"
            )

        day_data = stock_data[date]

        result = {
            "open": float(day_data["1. open"]),
            "high": float(day_data["2. high"]),
            "low": float(day_data["3. low"]),
            "close": float(day_data["4. close"]),
            "volume": int(day_data["5. volume"]),
        }

        return result

    def get_min(self, symbol: str, n: int):
        """Retrieve the lowest trading price over the last `n` days for a given symbol.

        :param symbol: The stock symbol for which to retrieve the data.
        :param n: The number of days to retrieve data for.
        :return: A dictionary containing the lowest price for the specified symbol over the last `n` days.
        """
        # Validate the range `n`
        if n <= 0:
            raise HTTPException(
                status_code=400, detail="Range `n` must be greater than 0"
            )

        # Fetch the stock data
        stock_data = self._fetch_stock_data(symbol)

        # Get all available dates from the stock data
        all_dates = stock_data.keys()

        # Check if the requested range exceeds available data
        if n > len(all_dates):
            raise HTTPException(
                status_code=400, detail="Requested range `n` exceeds available data"
            )

        # Sort dates in descending order (newest first)
        sorted_dates = sorted(all_dates, reverse=True)

        # Select the most recent 'n' days
        recent_dates = sorted_dates[:n]

        # Get the minimum low price for the recent days
        low_prices = [float(stock_data[date]["3. low"]) for date in recent_dates]

        # Find the minimum low price
        min_price = min(low_prices)

        result = {"min": min_price}

        return result

    def get_max(self, symbol: str, n: int):
        """Retrieve the highest trading price over the last `n` days for a given symbol.

        :param symbol: The stock symbol for which to retrieve the data.
        :param n: The number of days to retrieve data for.
        :return: A dictionary containing the highest price for the specified symbol over the last `n` days.
        """
        # Validate the range `n`
        if n <= 0:
            raise HTTPException(
                status_code=400, detail="Range `n` must be greater than 0"
            )

        # Fetch the stock data
        stock_data = self._fetch_stock_data(symbol)

        # Get all available dates from the stock data
        all_dates = stock_data.keys()

        # Check if the requested range exceeds available data
        if n > len(all_dates):
            raise HTTPException(
                status_code=400, detail="Requested range `n` exceeds available data"
            )

        # Sort dates in descending order (newest first)
        sorted_dates = sorted(all_dates, reverse=True)

        # Select the most recent 'n' days
        recent_dates = sorted_dates[:n]

        # Get the high prices for the recent days
        high_prices = [float(stock_data[date]["2. high"]) for date in recent_dates]

        # Find the maximum high price
        max_price = max(high_prices)

        result = {"max": max_price}

        return result
