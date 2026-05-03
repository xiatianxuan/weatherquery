"""Configuration management for weatherquery."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import tomllib

from .exceptions import ConfigError


@dataclass
class CacheConfig:
    """Cache configuration."""

    enabled: bool = True
    cache_type: str = "memory"  # "memory", "file", or "none"
    ttl_seconds: int = 300  # 5 minutes
    cache_dir: Optional[Path] = None


@dataclass
class RequestConfig:
    """Request configuration."""

    timeout: int = 10  # seconds
    max_retries: int = 3
    retry_delay: float = 1.0  # seconds


@dataclass
class WeatherConfig:
    """Main configuration class."""

    default_location: Optional[str] = None
    default_language: str = "en"
    default_units: str = "metric"  # "metric" or "imperial"
    cache: CacheConfig = field(default_factory=CacheConfig)
    request: RequestConfig = field(default_factory=RequestConfig)
    api_base_url: str = "https://wttr.in"


def find_config_file() -> Optional[Path]:
    """Find configuration file in standard locations."""
    # Check environment variable first
    env_config = os.environ.get("WEATHERQUERY_CONFIG")
    if env_config:
        config_path = Path(env_config)
        if config_path.exists():
            return config_path

    # Check current directory
    current_dir_config = Path.cwd() / ".weatherquery.toml"
    if current_dir_config.exists():
        return current_dir_config

    # Check home directory
    home_config = Path.home() / ".weatherquery.toml"
    if home_config.exists():
        return home_config

    # Check XDG config directory
    xdg_config = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    xdg_config_path = Path(xdg_config) / "weatherquery" / "config.toml"
    if xdg_config_path.exists():
        return xdg_config_path

    return None


def load_config_from_file(config_path: Path) -> dict:
    """Load configuration from TOML file."""
    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        raise ConfigError(f"Failed to load config file: {e}") from e


def load_config_from_env() -> dict:
    """Load configuration from environment variables."""
    config = {}

    # Location
    if location := os.environ.get("WEATHERQUERY_LOCATION"):
        config["default_location"] = location

    # Language
    if language := os.environ.get("WEATHERQUERY_LANGUAGE"):
        config["default_language"] = language

    # Units
    if units := os.environ.get("WEATHERQUERY_UNITS"):
        config["default_units"] = units

    # Cache settings
    cache_config = {}
    if cache_enabled := os.environ.get("WEATHERQUERY_CACHE_ENABLED"):
        cache_config["enabled"] = cache_enabled.lower() in ("true", "1", "yes")
    if cache_type := os.environ.get("WEATHERQUERY_CACHE_TYPE"):
        cache_config["cache_type"] = cache_type
    if cache_ttl := os.environ.get("WEATHERQUERY_CACHE_TTL"):
        cache_config["ttl_seconds"] = int(cache_ttl)
    if cache_dir := os.environ.get("WEATHERQUERY_CACHE_DIR"):
        cache_config["cache_dir"] = Path(cache_dir)

    if cache_config:
        config["cache"] = cache_config

    # Request settings
    request_config = {}
    if timeout := os.environ.get("WEATHERQUERY_TIMEOUT"):
        request_config["timeout"] = int(timeout)
    if max_retries := os.environ.get("WEATHERQUERY_MAX_RETRIES"):
        request_config["max_retries"] = int(max_retries)
    if retry_delay := os.environ.get("WEATHERQUERY_RETRY_DELAY"):
        request_config["retry_delay"] = float(retry_delay)

    if request_config:
        config["request"] = request_config

    # API base URL
    if api_base_url := os.environ.get("WEATHERQUERY_API_BASE_URL"):
        config["api_base_url"] = api_base_url

    return config


def merge_configs(*configs: dict) -> dict:
    """Merge multiple configuration dictionaries."""
    merged = {}
    for config in configs:
        for key, value in config.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = merge_configs(merged[key], value)
            else:
                merged[key] = value
    return merged


def create_config(config_file: Optional[Path] = None, **kwargs) -> WeatherConfig:
    """Create configuration from various sources."""
    # Start with default config
    default_config = {
        "default_location": None,
        "default_language": "en",
        "default_units": "metric",
        "cache": {
            "enabled": True,
            "cache_type": "memory",
            "ttl_seconds": 300,
            "cache_dir": None,
        },
        "request": {
            "timeout": 10,
            "max_retries": 3,
            "retry_delay": 1.0,
        },
        "api_base_url": "https://wttr.in",
    }

    # Load from file if provided or found
    file_config = {}
    if config_file is None:
        config_file = find_config_file()

    if config_file and config_file.exists():
        file_config = load_config_from_file(config_file)

    # Load from environment
    env_config = load_config_from_env()

    # Merge configs (priority: kwargs > env > file > default)
    merged = merge_configs(default_config, file_config, env_config, kwargs)

    # Create config objects
    cache_config = CacheConfig(**merged.get("cache", {}))
    request_config = RequestConfig(**merged.get("request", {}))

    return WeatherConfig(
        default_location=merged.get("default_location"),
        default_language=merged.get("default_language", "en"),
        default_units=merged.get("default_units", "metric"),
        cache=cache_config,
        request=request_config,
        api_base_url=merged.get("api_base_url", "https://wttr.in"),
    )
