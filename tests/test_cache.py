"""Tests for weatherquery cache implementations."""

import time
import pytest
from weatherquery.cache import MemoryCache, FileCache, NullCache, create_cache
from weatherquery.config import CacheConfig


def test_memory_cache():
    """Test memory cache implementation."""
    cache = MemoryCache(default_ttl=1)

    # Test set and get
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"

    # Test non-existent key
    assert cache.get("nonexistent") is None

    # Test TTL expiration
    cache.set("key2", "value2", ttl=0)
    time.sleep(0.1)
    assert cache.get("key2") is None

    # Test delete
    cache.set("key3", "value3")
    cache.delete("key3")
    assert cache.get("key3") is None

    # Test clear
    cache.set("key4", "value4")
    cache.set("key5", "value5")
    cache.clear()
    assert cache.get("key4") is None
    assert cache.get("key5") is None


def test_file_cache(tmp_path):
    """Test file cache implementation."""
    cache = FileCache(cache_dir=tmp_path, default_ttl=1)

    # Test set and get
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"

    # Test non-existent key
    assert cache.get("nonexistent") is None

    # Test TTL expiration
    cache.set("key2", "value2", ttl=0)
    time.sleep(0.1)
    assert cache.get("key2") is None

    # Test delete
    cache.set("key3", "value3")
    cache.delete("key3")
    assert cache.get("key3") is None

    # Test clear
    cache.set("key4", "value4")
    cache.set("key5", "value5")
    cache.clear()
    assert cache.get("key4") is None
    assert cache.get("key5") is None

    # Test complex data
    complex_data = {"nested": {"key": "value"}, "list": [1, 2, 3]}
    cache.set("complex", complex_data)
    assert cache.get("complex") == complex_data


def test_null_cache():
    """Test null cache implementation."""
    cache = NullCache()

    # Test set and get
    cache.set("key1", "value1")
    assert cache.get("key1") is None

    # Test delete (should not raise)
    cache.delete("key1")

    # Test clear (should not raise)
    cache.clear()


def test_create_cache():
    """Test cache creation from config."""
    # Test memory cache
    config = CacheConfig(enabled=True, cache_type="memory", ttl_seconds=60)
    cache = create_cache(config)
    assert isinstance(cache, MemoryCache)

    # Test file cache
    config = CacheConfig(enabled=True, cache_type="file", ttl_seconds=60)
    cache = create_cache(config)
    assert isinstance(cache, FileCache)

    # Test null cache
    config = CacheConfig(enabled=False)
    cache = create_cache(config)
    assert isinstance(cache, NullCache)

    # Test unknown cache type
    config = CacheConfig(enabled=True, cache_type="unknown")
    with pytest.raises(Exception):
        create_cache(config)
