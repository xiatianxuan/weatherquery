"""WeatherQuery - A Python library for querying weather data from wttr.in API."""

from .async_client import AsyncWeatherClient
from .client import WeatherClient
from .config import WeatherConfig, create_config
from .exceptions import (
    APIError,
    CacheError,
    ConfigError,
    InvalidFormatError,
    LocationNotFoundError,
    NetworkError,
    ParseError,
    RateLimitExceededError,
    TimeoutError,
    WeatherQueryError,
)
from .formatters import (
    CustomFormatter,
    Formatter,
    JsonFormatter,
    PlainFormatter,
    PlainTextFormatter,
    TextFormatter,
    get_formatter,
)
from .models import (
    Astronomy,
    CurrentCondition,
    DailyForecast,
    HourlyForecast,
    Location,
    WeatherData,
    WeatherDescription,
)

__version__ = "0.1.0"
__all__ = [
    # Clients
    "WeatherClient",
    "AsyncWeatherClient",
    # Configuration
    "WeatherConfig",
    "create_config",
    # Models
    "WeatherData",
    "CurrentCondition",
    "DailyForecast",
    "HourlyForecast",
    "Location",
    "WeatherDescription",
    "Astronomy",
    # Formatters
    "Formatter",
    "JsonFormatter",
    "TextFormatter",
    "PlainFormatter",
    "PlainTextFormatter",
    "CustomFormatter",
    "get_formatter",
    # Exceptions
    "WeatherQueryError",
    "APIError",
    "LocationNotFoundError",
    "RateLimitExceededError",
    "InvalidFormatError",
    "NetworkError",
    "TimeoutError",
    "ParseError",
    "ConfigError",
    "CacheError",
]
