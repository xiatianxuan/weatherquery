"""Tests for weatherquery formatters."""

import json
import pytest
from weatherquery.formatters import (
    JsonFormatter,
    TextFormatter,
    PlainFormatter,
    CustomFormatter,
    get_formatter,
)
from weatherquery.models import (
    WeatherData,
    CurrentCondition,
    DailyForecast,
    HourlyForecast,
    Location,
    WeatherDescription,
    Astronomy,
)


@pytest.fixture
def sample_weather_data():
    """Create sample weather data for testing."""
    location = Location(
        area_name="Beijing",
        country="China",
        region="Beijing",
        latitude=39.9042,
        longitude=116.4074,
        population=21540000,
        weather_url="https://wttr.in/Beijing",
    )

    current_condition = CurrentCondition(
        temp_c=20.0,
        temp_f=68.0,
        feels_like_c=18.0,
        feels_like_f=64.0,
        humidity=50,
        cloud_cover=25,
        pressure_mb=1013.0,
        pressure_in=30.0,
        visibility_km=10.0,
        visibility_miles=6.0,
        uv_index=5,
        precip_mm=0.0,
        precip_in=0.0,
        weather_code=113,
        weather_desc=WeatherDescription(value="Sunny"),
        wind_speed_kmph=15.0,
        wind_speed_miles=9.0,
        wind_dir_degree=180,
        wind_dir_16_point="S",
        observation_time="10:00 AM",
        local_obs_datetime="2024-01-01 10:00",
    )

    astronomy = Astronomy(
        sunrise="06:00 AM",
        sunset="06:00 PM",
        moonrise="08:00 PM",
        moonset="06:00 AM",
        moon_phase="Waxing Crescent",
        moon_illumination=25,
    )

    hourly_forecast = HourlyForecast(
        time=0,
        temp_c=18.0,
        temp_f=64.0,
        feels_like_c=16.0,
        feels_like_f=61.0,
        humidity=55,
        cloud_cover=20,
        pressure_mb=1012.0,
        pressure_in=30.0,
        visibility_km=10.0,
        visibility_miles=6.0,
        uv_index=0,
        precip_mm=0.0,
        precip_in=0.0,
        weather_code=113,
        weather_desc=WeatherDescription(value="Clear"),
        wind_speed_kmph=10.0,
        wind_speed_miles=6.0,
        wind_dir_degree=180,
        wind_dir_16_point="S",
        chance_of_rain=0,
        chance_of_snow=0,
        chance_of_thunder=0,
        chance_of_fog=0,
        chance_of_frost=0,
        chance_of_high_temp=0,
        chance_of_overcast=0,
        chance_of_sunshine=100,
        chance_of_windy=0,
        dew_point_c=10.0,
        dew_point_f=50.0,
        heat_index_c=18.0,
        heat_index_f=64.0,
        wind_chill_c=16.0,
        wind_chill_f=61.0,
        wind_gust_kmph=15.0,
        wind_gust_miles=9.0,
        short_rad=0.0,
        diff_rad=0.0,
    )

    daily_forecast = DailyForecast(
        date="2024-01-01",
        date_epoch=1704067200,
        max_temp_c=25.0,
        max_temp_f=77.0,
        min_temp_c=15.0,
        min_temp_f=59.0,
        avg_temp_c=20.0,
        avg_temp_f=68.0,
        sun_hour=8.0,
        total_snow_cm=0.0,
        uv_index=5,
        astronomy=astronomy,
        hourly=[hourly_forecast],
    )

    return WeatherData(
        location=location,
        current_condition=current_condition,
        forecast=[daily_forecast],
        request_query="Beijing",
        request_type="City",
    )


def test_json_formatter(sample_weather_data):
    """Test JSON formatter."""
    formatter = JsonFormatter()
    result = formatter.format(sample_weather_data)

    # Parse JSON to verify it's valid
    parsed = json.loads(result)
    assert parsed["location"]["area_name"] == "Beijing"
    assert parsed["current_condition"]["temp_c"] == 20.0
    assert len(parsed["forecast"]) == 1


def test_text_formatter(sample_weather_data):
    """Test text formatter."""
    formatter = TextFormatter()
    result = formatter.format(sample_weather_data)

    assert "Weather report: Beijing, China" in result
    assert "Temperature: 20.0°C (68.0°F)" in result
    assert "Weather: Sunny" in result
    assert "Wind: 15.0 km/h S" in result
    assert "Forecast:" in result
    assert "2024-01-01:" in result


def test_plain_formatter(sample_weather_data):
    """Test plain formatter."""
    formatter = PlainFormatter()
    result = formatter.format(sample_weather_data)

    assert "Beijing, China" in result
    assert "Sunny" in result
    assert "20.0°C" in result
    assert "Wind: 15.0 km/h S" in result


def test_custom_formatter(sample_weather_data):
    """Test custom formatter."""
    format_string = "{location}, {country}: {temp_c}°C, {weather_desc}"
    formatter = CustomFormatter(format_string)
    result = formatter.format(sample_weather_data)

    assert result == "Beijing, China: 20.0°C, Sunny"


def test_custom_formatter_with_forecast(sample_weather_data):
    """Test custom formatter with forecast variables."""
    format_string = "Max: {max_temp_c}°C, Min: {min_temp_c}°C, Sunrise: {sunrise}"
    formatter = CustomFormatter(format_string)
    result = formatter.format(sample_weather_data)

    assert result == "Max: 25.0°C, Min: 15.0°C, Sunrise: 06:00 AM"


def test_custom_formatter_invalid_variable(sample_weather_data):
    """Test custom formatter with invalid variable."""
    format_string = "{invalid_variable}"
    formatter = CustomFormatter(format_string)

    with pytest.raises(ValueError, match="Unknown variable"):
        formatter.format(sample_weather_data)


def test_get_formatter():
    """Test get_formatter function."""
    # Test known formatters
    assert isinstance(get_formatter("json"), JsonFormatter)
    assert isinstance(get_formatter("text"), TextFormatter)
    assert isinstance(get_formatter("plain"), PlainFormatter)

    # Test custom formatter
    custom = get_formatter("custom", format_string="{location}")
    assert isinstance(custom, CustomFormatter)

    # Test custom formatter without format_string
    with pytest.raises(ValueError, match="Custom format requires"):
        get_formatter("custom")

    # Test unknown formatter
    with pytest.raises(ValueError, match="Unknown format type"):
        get_formatter("unknown")
