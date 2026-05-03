"""Formatters for weather data output."""

import re
from abc import ABC, abstractmethod

from .models import WeatherData


def remove_emoji(text: str) -> str:
    """Remove emoji characters from text."""
    # Unicode ranges for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # flags (iOS)
        "\U00002702-\U000027b0"
        "\U000024c2-\U0001f251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2b55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text).strip()


class Formatter(ABC):
    """Abstract base class for formatters."""

    @abstractmethod
    def format(self, data: WeatherData) -> str:
        """Format weather data to string."""
        pass


class JsonFormatter(Formatter):
    """Format weather data as JSON."""

    def format(self, data: WeatherData) -> str:
        """Format weather data as JSON string."""
        import json
        from dataclasses import asdict

        return json.dumps(asdict(data), ensure_ascii=False, indent=2)


class TextFormatter(Formatter):
    """Format weather data as text (similar to wttr.in ASCII art)."""

    def format(self, data: WeatherData) -> str:
        """Format weather data as text with ASCII art."""
        lines = []

        # Header
        lines.append(
            f"Weather report: {data.location.area_name}, {data.location.country}"
        )
        lines.append("")

        # Current conditions
        current = data.current_condition
        lines.append("Current weather:")
        lines.append(f"  Temperature: {current.temp_c}°C ({current.temp_f}°F)")
        lines.append(
            f"  Feels like: {current.feels_like_c}°C ({current.feels_like_f}°F)"
        )
        lines.append(f"  Weather: {current.weather_desc.value}")
        lines.append(
            f"  Wind: {current.wind_speed_kmph} km/h {current.wind_dir_16_point}"
        )
        lines.append(f"  Humidity: {current.humidity}%")
        lines.append(f"  Pressure: {current.pressure_mb} mb")
        lines.append(f"  Visibility: {current.visibility_km} km")
        lines.append(f"  UV Index: {current.uv_index}")
        lines.append("")

        # Forecast
        if data.forecast:
            lines.append("Forecast:")
            for day in data.forecast:
                lines.append(f"  {day.date}:")
                lines.append(f"    Max: {day.max_temp_c}°C ({day.max_temp_f}°F)")
                lines.append(f"    Min: {day.min_temp_c}°C ({day.min_temp_f}°F)")
                lines.append(f"    Avg: {day.avg_temp_c}°C ({day.avg_temp_f}°F)")
                lines.append(f"    UV Index: {day.uv_index}")
                lines.append("")

        return "\n".join(lines)


class PlainFormatter(Formatter):
    """Format weather data as plain text (simplified)."""

    def format(self, data: WeatherData) -> str:
        """Format weather data as plain text."""
        current = data.current_condition
        location = data.location

        return (
            f"{location.area_name}, {location.country}: "
            f"{current.weather_desc.value}, "
            f"{current.temp_c}°C (feels like {current.feels_like_c}°C), "
            f"Wind: {current.wind_speed_kmph} km/h {current.wind_dir_16_point}, "
            f"Humidity: {current.humidity}%"
        )


class CustomFormatter(Formatter):
    """Format weather data using custom format string."""

    def __init__(self, format_string: str):
        self.format_string = format_string

    def format(self, data: WeatherData) -> str:
        """Format weather data using custom format string."""
        # Create a dictionary of available variables
        variables = {
            "location": data.location.area_name,
            "country": data.location.country,
            "region": data.location.region,
            "latitude": data.location.latitude,
            "longitude": data.location.longitude,
            "temp_c": data.current_condition.temp_c,
            "temp_f": data.current_condition.temp_f,
            "feels_like_c": data.current_condition.feels_like_c,
            "feels_like_f": data.current_condition.feels_like_f,
            "humidity": data.current_condition.humidity,
            "cloud_cover": data.current_condition.cloud_cover,
            "pressure_mb": data.current_condition.pressure_mb,
            "pressure_in": data.current_condition.pressure_in,
            "visibility_km": data.current_condition.visibility_km,
            "visibility_miles": data.current_condition.visibility_miles,
            "uv_index": data.current_condition.uv_index,
            "precip_mm": data.current_condition.precip_mm,
            "precip_in": data.current_condition.precip_in,
            "weather_desc": data.current_condition.weather_desc.value,
            "weather_code": data.current_condition.weather_code,
            "wind_speed_kmph": data.current_condition.wind_speed_kmph,
            "wind_speed_miles": data.current_condition.wind_speed_miles,
            "wind_dir_degree": data.current_condition.wind_dir_degree,
            "wind_dir_16_point": data.current_condition.wind_dir_16_point,
            "observation_time": data.current_condition.observation_time,
            "local_obs_datetime": data.current_condition.local_obs_datetime,
        }

        # Add forecast variables if available
        if data.forecast:
            today = data.forecast[0]
            variables.update(
                {
                    "max_temp_c": today.max_temp_c,
                    "max_temp_f": today.max_temp_f,
                    "min_temp_c": today.min_temp_c,
                    "min_temp_f": today.min_temp_f,
                    "avg_temp_c": today.avg_temp_c,
                    "avg_temp_f": today.avg_temp_f,
                    "sun_hour": today.sun_hour,
                    "total_snow_cm": today.total_snow_cm,
                    "forecast_uv_index": today.uv_index,
                    "sunrise": today.astronomy.sunrise,
                    "sunset": today.astronomy.sunset,
                    "moonrise": today.astronomy.moonrise,
                    "moonset": today.astronomy.moonset,
                    "moon_phase": today.astronomy.moon_phase,
                    "moon_illumination": today.astronomy.moon_illumination,
                }
            )

        # Replace variables in format string
        try:
            return self.format_string.format(**variables)
        except KeyError as e:
            raise ValueError(f"Unknown variable in format string: {e}") from e


class PlainTextFormatter(Formatter):
    """Format weather data as plain text without emoji."""

    def format(self, data: WeatherData) -> str:
        """Format weather data as plain text without emoji."""
        current = data.current_condition
        location = data.location

        # Create a plain text summary
        text = (
            f"{location.area_name}, {location.country}: "
            f"{current.weather_desc.value}, "
            f"{current.temp_c}°C (feels like {current.feels_like_c}°C), "
            f"Wind: {current.wind_speed_kmph} km/h {current.wind_dir_16_point}, "
            f"Humidity: {current.humidity}%"
        )

        return text


def get_formatter(format_type: str, **kwargs) -> Formatter:
    """Get formatter instance by type."""
    formatters = {
        "json": JsonFormatter,
        "text": TextFormatter,
        "plain": PlainFormatter,
        "plaintext": PlainTextFormatter,
    }

    if format_type in formatters:
        return formatters[format_type]()
    elif format_type == "custom":
        format_string = kwargs.get("format_string")
        if not format_string:
            raise ValueError("Custom format requires 'format_string' parameter")
        return CustomFormatter(format_string)
    else:
        raise ValueError(f"Unknown format type: {format_type}")
