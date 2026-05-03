"""Cache implementations for weatherquery."""

import hashlib
import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from .config import CacheConfig
from .exceptions import CacheError


class Cache(ABC):
    """Abstract base class for cache implementations."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete value from cache."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all cached values."""
        pass


class MemoryCache(Cache):
    """In-memory cache implementation."""

    def __init__(self, default_ttl: int = 300):
        self._cache: dict[str, tuple[Any, float]] = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self._cache:
            return None

        value, expiry = self._cache[key]
        if time.time() > expiry:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        if ttl is None:
            ttl = self._default_ttl

        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """Delete value from cache."""
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()


class FileCache(Cache):
    """File-based cache implementation."""

    def __init__(self, cache_dir: Path, default_ttl: int = 300):
        self._cache_dir = cache_dir
        self._default_ttl = default_ttl

        # Create cache directory if it doesn't exist
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for key."""
        # Create a hash of the key for filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self._cache_dir / f"{key_hash}.json"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check expiry
            if time.time() > data.get("expiry", 0):
                cache_path.unlink()
                return None

            return data.get("value")
        except (json.JSONDecodeError, KeyError, OSError):
            # If cache file is corrupted, delete it
            cache_path.unlink(missing_ok=True)
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        if ttl is None:
            ttl = self._default_ttl

        cache_path = self._get_cache_path(key)

        data = {
            "value": value,
            "expiry": time.time() + ttl,
            "key": key,
        }

        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise CacheError(f"Failed to write cache file: {e}") from e

    def delete(self, key: str) -> None:
        """Delete value from cache."""
        cache_path = self._get_cache_path(key)
        cache_path.unlink(missing_ok=True)

    def clear(self) -> None:
        """Clear all cached values."""
        for cache_file in self._cache_dir.glob("*.json"):
            cache_file.unlink()


class NullCache(Cache):
    """No-op cache implementation."""

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        pass

    def delete(self, key: str) -> None:
        """Delete value from cache."""
        pass

    def clear(self) -> None:
        """Clear all cached values."""
        pass


def create_cache(config: CacheConfig) -> Cache:
    """Create cache instance based on configuration."""
    if not config.enabled:
        return NullCache()

    if config.cache_type == "memory":
        return MemoryCache(default_ttl=config.ttl_seconds)
    elif config.cache_type == "file":
        cache_dir = config.cache_dir or Path.home() / ".cache" / "weatherquery"
        return FileCache(cache_dir=cache_dir, default_ttl=config.ttl_seconds)
    elif config.cache_type == "none":
        return NullCache()
    else:
        raise CacheError(f"Unknown cache type: {config.cache_type}")
