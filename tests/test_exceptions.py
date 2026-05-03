"""Tests for weatherquery exceptions."""

from weatherquery.exceptions import (
    WeatherQueryError,
    APIError,
    LocationNotFoundError,
    RateLimitExceededError,
    InvalidFormatError,
    NetworkError,
    TimeoutError,
    ParseError,
    ConfigError,
    CacheError,
)


def test_weather_query_error():
    """Test base WeatherQueryError."""
    error = WeatherQueryError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_api_error():
    """Test APIError."""
    error = APIError("API failed", status_code=500)
    assert str(error) == "API failed"
    assert error.status_code == 500
    assert error.response is None
    assert isinstance(error, WeatherQueryError)


def test_location_not_found_error():
    """Test LocationNotFoundError."""
    error = LocationNotFoundError("Location not found")
    assert str(error) == "Location not found"
    assert isinstance(error, WeatherQueryError)


def test_rate_limit_exceeded_error():
    """Test RateLimitExceededError."""
    error = RateLimitExceededError("Rate limit exceeded")
    assert str(error) == "Rate limit exceeded"
    assert isinstance(error, WeatherQueryError)


def test_invalid_format_error():
    """Test InvalidFormatError."""
    error = InvalidFormatError("Invalid format")
    assert str(error) == "Invalid format"
    assert isinstance(error, WeatherQueryError)


def test_network_error():
    """Test NetworkError."""
    error = NetworkError("Network failed")
    assert str(error) == "Network failed"
    assert isinstance(error, WeatherQueryError)


def test_timeout_error():
    """Test TimeoutError."""
    error = TimeoutError("Request timed out")
    assert str(error) == "Request timed out"
    assert isinstance(error, WeatherQueryError)


def test_parse_error():
    """Test ParseError."""
    error = ParseError("Parse failed")
    assert str(error) == "Parse failed"
    assert isinstance(error, WeatherQueryError)


def test_config_error():
    """Test ConfigError."""
    error = ConfigError("Config failed")
    assert str(error) == "Config failed"
    assert isinstance(error, WeatherQueryError)


def test_cache_error():
    """Test CacheError."""
    error = CacheError("Cache failed")
    assert str(error) == "Cache failed"
    assert isinstance(error, WeatherQueryError)


def test_exception_hierarchy():
    """Test exception hierarchy."""
    # All custom exceptions should inherit from WeatherQueryError
    exceptions = [
        APIError("test"),
        LocationNotFoundError("test"),
        RateLimitExceededError("test"),
        InvalidFormatError("test"),
        NetworkError("test"),
        TimeoutError("test"),
        ParseError("test"),
        ConfigError("test"),
        CacheError("test"),
    ]

    for exc in exceptions:
        assert isinstance(exc, WeatherQueryError)
        assert isinstance(exc, Exception)
