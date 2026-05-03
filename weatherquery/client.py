"""Synchronous weather client for wttr.in API."""

import httpx
from typing import Optional, Union

from .cache import Cache, create_cache
from .config import WeatherConfig, create_config
from .exceptions import (
    APIError,
    LocationNotFoundError,
    NetworkError,
    RateLimitExceededError,
    TimeoutError,
)
from .models import WeatherData
from .parsers import parse_weather_data


class WeatherClient:
    """Synchronous weather client."""

    def __init__(
        self,
        config: Optional[WeatherConfig] = None,
        cache: Optional[Cache] = None,
    ):
        self._config = config or create_config()
        self._cache = cache or create_cache(self._config.cache)
        self._client = httpx.Client(
            base_url=self._config.api_base_url,
            timeout=self._config.request.timeout,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def _build_url(self, location: str, **params) -> str:
        """Build API URL with parameters."""
        # Clean location string
        location = location.strip()

        # Build query parameters
        query_params = {}

        # Add format parameter
        format_type = params.get("format", "json")
        if format_type == "json":
            query_params["format"] = "j1"
        elif format_type == "text":
            query_params["format"] = "v2"
        elif format_type == "plain":
            query_params["format"] = "2"
        else:
            query_params["format"] = format_type

        # Add language parameter
        if lang := params.get("lang"):
            query_params["lang"] = lang

        # Add units parameter
        if units := params.get("units"):
            if units == "imperial":
                query_params["u"] = ""

        # Add number of days
        if days := params.get("days"):
            query_params["n"] = str(days)

        # Add other parameters
        for key, value in params.items():
            if key not in ("format", "lang", "units", "days") and value is not None:
                query_params[key] = str(value)

        return f"/{location}", query_params

    def _make_request(self, location: str, **params) -> dict | str:
        """Make HTTP request to wttr.in API."""
        url, query_params = self._build_url(location, **params)

        try:
            response = self._client.get(url, params=query_params)

            # Check for rate limiting
            if response.status_code == 429:
                raise RateLimitExceededError(
                    "Rate limit exceeded. Please wait before making more requests."
                )

            # Check for location not found
            if response.status_code == 404:
                raise LocationNotFoundError(f"Location '{location}' not found.")

            # Check for other errors
            if response.status_code >= 400:
                raise APIError(
                    f"API request failed with status {response.status_code}",
                    status_code=response.status_code,
                    response=response,
                )

            # Return JSON for json format, text for other formats
            format_type = params.get("format", "json")
            if format_type == "json":
                return response.json()
            else:
                return response.text

        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {e}") from e

    def _get_cache_key(self, location: str, **params) -> str:
        """Generate cache key for request."""
        # Create a deterministic key from location and parameters
        key_parts = [location]
        for k, v in sorted(params.items()):
            if v is not None:
                key_parts.append(f"{k}={v}")
        return "|".join(key_parts)

    def get_weather(
        self,
        location: Optional[str] = None,
        format: str = "json",
        lang: Optional[str] = None,
        units: Optional[str] = None,
        **kwargs,
    ) -> Union[WeatherData, str]:
        """
        Get current weather for a location.

        Args:
            location: Location to query (city name, coordinates, IP, etc.)
            format: Output format ("json", "text", "plain")
            lang: Language code (e.g., "zh", "en")
            units: Units system ("metric" or "imperial")
            **kwargs: Additional parameters

        Returns:
            WeatherData object for JSON format, string for other formats
        """
        # Use default location if not provided
        if location is None:
            location = self._config.default_location
            if location is None:
                raise ValueError(
                    "No location provided and no default location configured."
                )

        # Use default values from config
        lang = lang or self._config.default_language
        units = units or self._config.default_units

        # Check cache
        cache_key = self._get_cache_key(
            location, format=format, lang=lang, units=units, **kwargs
        )
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        # Make API request
        data = self._make_request(
            location, format=format, lang=lang, units=units, **kwargs
        )

        # Parse response based on format
        if format == "json":
            result = parse_weather_data(data)
        else:
            # For text formats, return the raw response
            result = data if isinstance(data, str) else str(data)

        # Cache the result
        self._cache.set(cache_key, result)

        return result

    def get_forecast(
        self,
        location: Optional[str] = None,
        days: int = 3,
        format: str = "json",
        lang: Optional[str] = None,
        units: Optional[str] = None,
        **kwargs,
    ) -> Union[WeatherData, str]:
        """
        Get weather forecast for a location.

        Args:
            location: Location to query
            days: Number of forecast days (1-3)
            format: Output format
            lang: Language code
            units: Units system
            **kwargs: Additional parameters

        Returns:
            WeatherData object for JSON format, string for other formats
        """
        # Validate days
        if not 1 <= days <= 3:
            raise ValueError("Days must be between 1 and 3.")

        return self.get_weather(
            location=location,
            format=format,
            lang=lang,
            units=units,
            days=days,
            **kwargs,
        )
