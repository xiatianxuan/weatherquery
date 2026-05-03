"""Integration tests for weatherquery (real API calls)."""

import pytest
from weatherquery.client import WeatherClient
from weatherquery.async_client import AsyncWeatherClient
from weatherquery.config import create_config
from weatherquery.exceptions import LocationNotFoundError


@pytest.mark.integration
def test_get_weather_json():
    """Test getting weather in JSON format."""
    config = create_config(cache_enabled=False)

    with WeatherClient(config=config) as client:
        result = client.get_weather("Beijing", format="json")

        assert result is not None
        assert result.location.area_name == "Beijing"
        assert result.current_condition.temp_c is not None
        assert len(result.forecast) > 0


@pytest.mark.integration
def test_get_weather_text():
    """Test getting weather in text format."""
    config = create_config(cache_enabled=False)

    with WeatherClient(config=config) as client:
        result = client.get_weather("London", format="text")

        assert isinstance(result, str)
        assert "Weather report:" in result
        assert "Temperature:" in result


@pytest.mark.integration
def test_get_weather_plain():
    """Test getting weather in plain format."""
    config = create_config(cache_enabled=False)

    with WeatherClient(config=config) as client:
        result = client.get_weather("Tokyo", format="plain")

        assert isinstance(result, str)
        assert "Tokyo" in result


@pytest.mark.integration
def test_get_forecast():
    """Test getting weather forecast."""
    config = create_config(cache_enabled=False)

    with WeatherClient(config=config) as client:
        result = client.get_forecast("Paris", days=2, format="json")

        assert result is not None
        assert len(result.forecast) == 2
        assert result.location.area_name == "Paris"


@pytest.mark.integration
def test_get_weather_with_language():
    """Test getting weather with language parameter."""
    config = create_config(cache_enabled=False)

    with WeatherClient(config=config) as client:
        result = client.get_weather("Berlin", format="json", lang="zh")

        assert result is not None
        assert result.location.area_name == "Berlin"


@pytest.mark.integration
def test_get_weather_with_units():
    """Test getting weather with units parameter."""
    config = create_config(cache_enabled=False)

    with WeatherClient(config=config) as client:
        result = client.get_weather("New York", format="json", units="imperial")

        assert result is not None
        assert result.current_condition.temp_f is not None


@pytest.mark.integration
def test_get_weather_invalid_location():
    """Test getting weather for invalid location."""
    config = create_config(cache_enabled=False)

    with WeatherClient(config=config) as client:
        with pytest.raises(LocationNotFoundError):
            client.get_weather("InvalidLocationThatDoesNotExist12345", format="json")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_async_get_weather_json():
    """Test async getting weather in JSON format."""
    config = create_config(cache_enabled=False)

    async with AsyncWeatherClient(config=config) as client:
        result = await client.get_weather("Beijing", format="json")

        assert result is not None
        assert result.location.area_name == "Beijing"
        assert result.current_condition.temp_c is not None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_async_get_forecast():
    """Test async getting weather forecast."""
    config = create_config(cache_enabled=False)

    async with AsyncWeatherClient(config=config) as client:
        result = await client.get_forecast("London", days=1, format="json")

        assert result is not None
        assert len(result.forecast) == 1
        assert result.location.area_name == "London"
