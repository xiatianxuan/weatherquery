"""Data models for weather data from wttr.in API."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Location:
    """Location information."""

    area_name: str
    country: str
    region: str
    latitude: float
    longitude: float
    population: Optional[int] = None
    weather_url: Optional[str] = None


@dataclass
class WeatherDescription:
    """Weather description with icon."""

    value: str
    icon_url: Optional[str] = None


@dataclass
class CurrentCondition:
    """Current weather conditions."""

    temp_c: float
    temp_f: float
    feels_like_c: float
    feels_like_f: float
    humidity: int
    cloud_cover: int
    pressure_mb: float
    pressure_in: float
    visibility_km: float
    visibility_miles: float
    uv_index: int
    precip_mm: float
    precip_in: float
    weather_code: int
    weather_desc: WeatherDescription
    wind_speed_kmph: float
    wind_speed_miles: float
    wind_dir_degree: int
    wind_dir_16_point: str
    observation_time: str
    local_obs_datetime: str


@dataclass
class HourlyForecast:
    """Hourly weather forecast."""

    time: int
    temp_c: float
    temp_f: float
    feels_like_c: float
    feels_like_f: float
    humidity: int
    cloud_cover: int
    pressure_mb: float
    pressure_in: float
    visibility_km: float
    visibility_miles: float
    uv_index: int
    precip_mm: float
    precip_in: float
    weather_code: int
    weather_desc: WeatherDescription
    wind_speed_kmph: float
    wind_speed_miles: float
    wind_dir_degree: int
    wind_dir_16_point: str
    chance_of_rain: int
    chance_of_snow: int
    chance_of_thunder: int
    chance_of_fog: int
    chance_of_frost: int
    chance_of_high_temp: int
    chance_of_overcast: int
    chance_of_sunshine: int
    chance_of_windy: int
    dew_point_c: float
    dew_point_f: float
    heat_index_c: float
    heat_index_f: float
    wind_chill_c: float
    wind_chill_f: float
    wind_gust_kmph: float
    wind_gust_miles: float
    short_rad: float
    diff_rad: float


@dataclass
class Astronomy:
    """Astronomical data."""

    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_illumination: int


@dataclass
class DailyForecast:
    """Daily weather forecast."""

    date: str
    date_epoch: int
    max_temp_c: float
    max_temp_f: float
    min_temp_c: float
    min_temp_f: float
    avg_temp_c: float
    avg_temp_f: float
    sun_hour: float
    total_snow_cm: float
    uv_index: int
    astronomy: Astronomy
    hourly: list[HourlyForecast] = field(default_factory=list)


@dataclass
class WeatherData:
    """Complete weather data response."""

    location: Location
    current_condition: CurrentCondition
    forecast: list[DailyForecast]
    request_query: str
    request_type: str
