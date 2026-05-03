"""Tests for weatherquery configuration."""

from pathlib import Path
from weatherquery.config import (
    WeatherConfig,
    CacheConfig,
    RequestConfig,
    create_config,
    merge_configs,
)


def test_default_config():
    """Test default configuration creation."""
    config = create_config()
    assert config.default_language == "en"
    assert config.default_units == "metric"
    assert config.cache.enabled is True
    assert config.cache.cache_type == "memory"
    assert config.request.timeout == 10
    assert config.api_base_url == "https://wttr.in"


def test_config_from_kwargs():
    """Test configuration from keyword arguments."""
    config = create_config(
        default_location="London",
        default_language="zh",
        default_units="imperial",
    )
    assert config.default_location == "London"
    assert config.default_language == "zh"
    assert config.default_units == "imperial"


def test_config_from_env(monkeypatch):
    """Test configuration from environment variables."""
    monkeypatch.setenv("WEATHERQUERY_LOCATION", "Tokyo")
    monkeypatch.setenv("WEATHERQUERY_LANGUAGE", "ja")
    monkeypatch.setenv("WEATHERQUERY_UNITS", "imperial")
    monkeypatch.setenv("WEATHERQUERY_CACHE_ENABLED", "false")
    monkeypatch.setenv("WEATHERQUERY_TIMEOUT", "30")

    config = create_config()
    assert config.default_location == "Tokyo"
    assert config.default_language == "ja"
    assert config.default_units == "imperial"
    assert config.cache.enabled is False
    assert config.request.timeout == 30


def test_merge_configs():
    """Test configuration merging."""
    config1 = {"a": 1, "b": {"c": 2, "d": 3}}
    config2 = {"b": {"c": 4, "e": 5}, "f": 6}
    result = merge_configs(config1, config2)
    assert result["a"] == 1
    assert result["b"]["c"] == 4
    assert result["b"]["d"] == 3
    assert result["b"]["e"] == 5
    assert result["f"] == 6


def test_cache_config():
    """Test cache configuration."""
    cache_config = CacheConfig(
        enabled=True,
        cache_type="file",
        ttl_seconds=600,
        cache_dir=Path("/tmp/cache"),
    )
    assert cache_config.enabled is True
    assert cache_config.cache_type == "file"
    assert cache_config.ttl_seconds == 600
    assert cache_config.cache_dir == Path("/tmp/cache")


def test_request_config():
    """Test request configuration."""
    request_config = RequestConfig(
        timeout=30,
        max_retries=5,
        retry_delay=2.0,
    )
    assert request_config.timeout == 30
    assert request_config.max_retries == 5
    assert request_config.retry_delay == 2.0


def test_weather_config():
    """Test weather configuration."""
    config = WeatherConfig(
        default_location="Berlin",
        default_language="de",
        default_units="metric",
        cache=CacheConfig(enabled=False),
        request=RequestConfig(timeout=15),
        api_base_url="https://api.wttr.in",
    )
    assert config.default_location == "Berlin"
    assert config.default_language == "de"
    assert config.default_units == "metric"
    assert config.cache.enabled is False
    assert config.request.timeout == 15
    assert config.api_base_url == "https://api.wttr.in"
