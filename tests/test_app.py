import pytest
from fastapi import HTTPException
from src.StockWatch.stock_service import StockAPI  # Ensure correct import

# Sample mock data for stock API responses 
MOCK_STOCK_DATA = {
    "2025-03-07": {
        "1. open": "150.00",
        "2. high": "155.00",
        "3. low": "145.00",
        "4. close": "152.00",
        "5. volume": "1000000",
    },
    "2025-03-06": {
        "1. open": "148.00",
        "2. high": "152.00",
        "3. low": "144.00",
        "4. close": "150.00",
        "5. volume": "950000",
    },
    "2025-03-05": {
        "1. open": "145.00",
        "2. high": "149.00",
        "3. low": "140.00",
        "4. close": "146.00",
        "5. volume": "900000",
    },
}

@pytest.fixture
def stock_api():
    """Fixture to initialize StockAPI instance and inject mock data."""
    api = StockAPI()
    api.cache["APPL"] = MOCK_STOCK_DATA  # Simulated Cache hit for Mock functionality test
    return api

@pytest.mark.unit
def test_lookup_valid_date_cached(stock_api):
    """Test lookup function for a valid date."""
    result = stock_api.lookup("APPL", "2025-03-07")
    expected = {
        "open": 150.00,
        "high": 155.00,
        "low": 145.00,
        "close": 152.00,
        "volume": 1000000,
    }
    assert result == expected

@pytest.mark.unit
def test_lookup_invalid_date_cached(stock_api):
    """Test lookup function with a date not in the dataset."""
    with pytest.raises(HTTPException) as excinfo:
        stock_api.lookup("APPL", "2025-03-01")
    assert excinfo.value.status_code == 404
    assert "Data not available for the given date" in str(excinfo.value.detail)

@pytest.mark.unit
def test_get_min_valid_range_cached(stock_api):
    """Test get_min function with a valid range."""
    result = stock_api.get_min("APPL", 3)
    assert result == {"min": 140.00}

@pytest.mark.unit
def test_get_min_invalid_range_cached(stock_api):
    """Test get_min function with an invalid range (greater than available data)."""
    with pytest.raises(HTTPException) as excinfo:
        stock_api.get_min("APPL", 10)
    assert excinfo.value.status_code == 400
    assert "Requested range `n` exceeds available data" in str(excinfo.value.detail)

@pytest.mark.unit
def test_get_min_negative_range_cached(stock_api):
    with pytest.raises(HTTPException) as excinfo:
        stock_api.get_min("APPL", -1)
    assert excinfo.value.status_code == 400
    assert "Range `n` must be greater than 0" in str(excinfo.value.detail)

@pytest.mark.unit
def test_get_max_valid_range_cached(stock_api):
    """Test get_max function with a valid range."""
    result = stock_api.get_max("APPL", 3)
    assert result == {"max": 155.00}

@pytest.mark.unit
def test_get_max_invalid_range_cached(stock_api):
    """Test get_max function with an invalid range (negative or zero)."""
    with pytest.raises(HTTPException) as excinfo:
        stock_api.get_max("APPL", 0)
    assert excinfo.value.status_code == 400
    assert "Range `n` must be greater than 0" in str(excinfo.value.detail)

@pytest.mark.unit
def test_get_max_negative_range_cached(stock_api):
    with pytest.raises(HTTPException) as excinfo:
        stock_api.get_max("APPL", -1)
    assert excinfo.value.status_code == 400
    assert "Range `n` must be greater than 0" in str(excinfo.value.detail)

# integration tests
@pytest.mark.integration
def test_lookup_valid_date(stock_api):
    """Test lookup function for a valid date."""
    result = stock_api.lookup("IBM", "2025-03-07")
    expected = {
        "open": 245.95,
        "high": 261.96,
        "low": 245.1823,
        "close": 261.54,
        "volume": 6700184
    }
    assert result == expected

@pytest.mark.integration
def test_lookup_invalid_date(stock_api): 
    """Test lookup function with a date not in the dataset(market closure handling/ Date not in last 100 days / Future date)."""
    with pytest.raises(HTTPException) as excinfo:
        stock_api.lookup("IBM", "2025-03-01")
    assert excinfo.value.status_code == 404
    assert "Data not available for the given date" in str(excinfo.value.detail)

# Relative to the day of execution hence commenting it out
@pytest.mark.integration
def test_get_min_valid_range(stock_api):
    """Test get_min function with a valid range."""
    result = stock_api.get_min("IBM", 3)
    assert result == {"min": 245.1823}

@pytest.mark.integration
def test_get_max_valid_range(stock_api):
    """Test get_max function with a valid range."""
    result = stock_api.get_max("IBM", 3)
    assert result == {"max": 261.9600}

@pytest.mark.integration
def test_cache_hit(stock_api): # Actual Cache hit for end to end test
    """Test cache hit."""
    result1 = stock_api.get_min("IBM", 2) 
    result2 = stock_api.get_max("IBM", 2)
    # Test log should contain cache hit message. Using pytest -s to see logs
    assert result1 == result2