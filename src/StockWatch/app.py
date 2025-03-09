import os
from fastapi import FastAPI
from dotenv import load_dotenv
from .stock_service import StockAPI

# Load API Key from environment
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"
app = FastAPI()

stock_api = StockAPI()

@app.get("/status")
def status():
    return {"app": "StockWatch"}

@app.get("/lookup")
async def lookup(symbol: str, date: str):
    """Fetch stock price details for a given symbol and date."""
    return stock_api.lookup(symbol, date)

@app.get("/min")
async def get_min(symbol: str, n: int):
    """Fetch the lowest price for the last `n` days."""
    return stock_api.get_min(symbol, n)

@app.get("/max")
async def get_max(symbol: str, n: int):
    """Fetch the highest price for the last `n` days."""
    return stock_api.get_max(symbol, n)
