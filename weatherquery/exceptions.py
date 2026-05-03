"""Custom exceptions for weatherquery."""

from typing import Optional

import httpx


class WeatherQueryError(Exception):
    """Base exception for weatherquery."""

    pass


class APIError(WeatherQueryError):
    """API request error."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[httpx.Response] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class LocationNotFoundError(WeatherQueryError):
    """Location not found error."""

    pass


class RateLimitExceededError(WeatherQueryError):
    """Rate limit exceeded error."""

    pass


class InvalidFormatError(WeatherQueryError):
    """Invalid format error."""

    pass


class NetworkError(WeatherQueryError):
    """Network connection error."""

    pass


class TimeoutError(WeatherQueryError):
    """Request timeout error."""

    pass


class ParseError(WeatherQueryError):
    """Response parsing error."""

    pass


class ConfigError(WeatherQueryError):
    """Configuration error."""

    pass


class CacheError(WeatherQueryError):
    """Cache operation error."""

    pass
