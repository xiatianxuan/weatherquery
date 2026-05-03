"""Pytest configuration for weatherquery tests."""

import pytest
from weatherquery.config import WeatherConfig, CacheConfig, RequestConfig


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    return WeatherConfig(
        default_location="Beijing",
        default_language="en",
        default_units="metric",
        cache=CacheConfig(enabled=False),
        request=RequestConfig(timeout=5, max_retries=1),
        api_base_url="https://wttr.in",
    )


@pytest.fixture
def sample_weather_data():
    """Sample weather data for testing."""
    return {
        "current_condition": [
            {
                "temp_C": "20",
                "temp_F": "68",
                "FeelsLikeC": "18",
                "FeelsLikeF": "64",
                "humidity": "50",
                "cloudcover": "25",
                "pressure": "1013",
                "pressureInches": "30",
                "visibility": "10",
                "visibilityMiles": "6",
                "uvIndex": "5",
                "precipMM": "0.0",
                "precipInches": "0.0",
                "weatherCode": "113",
                "weatherDesc": [{"value": "Sunny"}],
                "windspeedKmph": "15",
                "windspeedMiles": "9",
                "winddirDegree": "180",
                "winddir16Point": "S",
                "observation_time": "10:00 AM",
                "localObsDateTime": "2024-01-01 10:00",
            }
        ],
        "nearest_area": [
            {
                "areaName": [{"value": "Beijing"}],
                "country": [{"value": "China"}],
                "region": [{"value": "Beijing"}],
                "latitude": "39.9042",
                "longitude": "116.4074",
                "population": "21540000",
                "weatherUrl": [{"value": "https://wttr.in/Beijing"}],
            }
        ],
        "request": [
            {
                "query": "Beijing",
                "type": "City",
            }
        ],
        "weather": [
            {
                "date": "2024-01-01",
                "date_epoch": "1704067200",
                "maxtempC": "25",
                "maxtempF": "77",
                "mintempC": "15",
                "mintempF": "59",
                "avgtempC": "20",
                "avgtempF": "68",
                "sunHour": "8.0",
                "totalSnow_cm": "0.0",
                "uvIndex": "5",
                "astronomy": [
                    {
                        "sunrise": "06:00 AM",
                        "sunset": "06:00 PM",
                        "moonrise": "08:00 PM",
                        "moonset": "06:00 AM",
                        "moon_phase": "Waxing Crescent",
                        "moon_illumination": "25",
                    }
                ],
                "hourly": [
                    {
                        "time": "0",
                        "tempC": "18",
                        "tempF": "64",
                        "FeelsLikeC": "16",
                        "FeelsLikeF": "61",
                        "humidity": "55",
                        "cloudcover": "20",
                        "pressure": "1012",
                        "pressureInches": "30",
                        "visibility": "10",
                        "visibilityMiles": "6",
                        "uvIndex": "0",
                        "precipMM": "0.0",
                        "precipInches": "0.0",
                        "weatherCode": "113",
                        "weatherDesc": [{"value": "Clear"}],
                        "windspeedKmph": "10",
                        "windspeedMiles": "6",
                        "winddirDegree": "180",
                        "winddir16Point": "S",
                        "chanceofrain": "0",
                        "chanceofsnow": "0",
                        "chanceofthunder": "0",
                        "chanceoffog": "0",
                        "chanceoffrost": "0",
                        "chanceofhightemp": "0",
                        "chanceofovercast": "0",
                        "chanceofsunshine": "100",
                        "chanceofwindy": "0",
                        "DewPointC": "10",
                        "DewPointF": "50",
                        "HeatIndexC": "18",
                        "HeatIndexF": "64",
                        "WindChillC": "16",
                        "WindChillF": "61",
                        "WindGustKmph": "15",
                        "WindGustMiles": "9",
                        "shortRad": "0",
                        "diffRad": "0",
                    }
                ],
            }
        ],
    }
