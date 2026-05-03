"""Tests for weatherquery parsers."""

from weatherquery.parsers import (
    parse_weather_data,
    parse_location,
    parse_current_condition,
    parse_daily_forecast,
    parse_hourly_forecast,
    parse_astronomy,
    parse_weather_description,
)


def test_parse_weather_description():
    """Test parsing weather description."""
    data = [{"value": "Sunny"}]
    result = parse_weather_description(data)
    assert result.value == "Sunny"


def test_parse_weather_description_empty():
    """Test parsing empty weather description."""
    data = []
    result = parse_weather_description(data)
    assert result.value == "Unknown"


def test_parse_location(sample_weather_data):
    """Test parsing location data."""
    data = sample_weather_data["nearest_area"]
    result = parse_location(data)
    assert result.area_name == "Beijing"
    assert result.country == "China"
    assert result.region == "Beijing"
    assert result.latitude == 39.9042
    assert result.longitude == 116.4074
    assert result.population == 21540000


def test_parse_current_condition(sample_weather_data):
    """Test parsing current condition."""
    data = sample_weather_data["current_condition"]
    result = parse_current_condition(data)
    assert result.temp_c == 20.0
    assert result.temp_f == 68.0
    assert result.feels_like_c == 18.0
    assert result.feels_like_f == 64.0
    assert result.humidity == 50
    assert result.weather_desc.value == "Sunny"


def test_parse_hourly_forecast(sample_weather_data):
    """Test parsing hourly forecast."""
    data = sample_weather_data["weather"][0]["hourly"]
    result = parse_hourly_forecast(data)
    assert len(result) == 1
    assert result[0].time == 0
    assert result[0].temp_c == 18.0
    assert result[0].weather_desc.value == "Clear"


def test_parse_astronomy(sample_weather_data):
    """Test parsing astronomy data."""
    data = sample_weather_data["weather"][0]["astronomy"]
    result = parse_astronomy(data)
    assert result.sunrise == "06:00 AM"
    assert result.sunset == "06:00 PM"
    assert result.moon_phase == "Waxing Crescent"
    assert result.moon_illumination == 25


def test_parse_daily_forecast(sample_weather_data):
    """Test parsing daily forecast."""
    data = sample_weather_data["weather"]
    result = parse_daily_forecast(data)
    assert len(result) == 1
    assert result[0].date == "2024-01-01"
    assert result[0].max_temp_c == 25.0
    assert result[0].min_temp_c == 15.0
    assert len(result[0].hourly) == 1


def test_parse_weather_data(sample_weather_data):
    """Test parsing complete weather data."""
    result = parse_weather_data(sample_weather_data)
    assert result.location.area_name == "Beijing"
    assert result.current_condition.temp_c == 20.0
    assert len(result.forecast) == 1
    assert result.request_query == "Beijing"
    assert result.request_type == "City"
