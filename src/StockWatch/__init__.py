# src/StockWatch/__init__.py

from .app import app
from .stock_service import StockAPI

__all__ = ["app", "StockAPI"]
