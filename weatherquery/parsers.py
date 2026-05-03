"""Parsers for wttr.in API responses."""

from typing import Any

from .models import (
    Astronomy,
    CurrentCondition,
    DailyForecast,
    HourlyForecast,
    Location,
    WeatherData,
    WeatherDescription,
)


def parse_weather_description(data: list[dict[str, Any]]) -> WeatherDescription:
    """Parse weather description from API response."""
    if not data:
        return WeatherDescription(value="Unknown")
    desc = data[0]
    return WeatherDescription(
        value=desc.get("value", "Unknown"),
        icon_url=desc.get("value"),  # wttr.in doesn't provide separate icon URL in JSON
    )


def parse_location(data: list[dict[str, Any]]) -> Location:
    """Parse location from API response."""
    if not data:
        raise ValueError("No location data")

    loc = data[0]
    area_name = loc.get("areaName", [{}])[0].get("value", "")
    country = loc.get("country", [{}])[0].get("value", "")
    region = loc.get("region", [{}])[0].get("value", "")
    latitude = float(loc.get("latitude", 0))
    longitude = float(loc.get("longitude", 0))
    population = int(loc.get("population", 0)) if loc.get("population") else None
    weather_url = (
        loc.get("weatherUrl", [{}])[0].get("value") if loc.get("weatherUrl") else None
    )

    return Location(
        area_name=area_name,
        country=country,
        region=region,
        latitude=latitude,
        longitude=longitude,
        population=population,
        weather_url=weather_url,
    )


def parse_current_condition(data: list[dict[str, Any]]) -> CurrentCondition:
    """Parse current condition from API response."""
    if not data:
        raise ValueError("No current condition data")

    cond = data[0]
    return CurrentCondition(
        temp_c=float(cond.get("temp_C", 0)),
        temp_f=float(cond.get("temp_F", 0)),
        feels_like_c=float(cond.get("FeelsLikeC", 0)),
        feels_like_f=float(cond.get("FeelsLikeF", 0)),
        humidity=int(cond.get("humidity", 0)),
        cloud_cover=int(cond.get("cloudcover", 0)),
        pressure_mb=float(cond.get("pressure", 0)),
        pressure_in=float(cond.get("pressureInches", 0)),
        visibility_km=float(cond.get("visibility", 0)),
        visibility_miles=float(cond.get("visibilityMiles", 0)),
        uv_index=int(cond.get("uvIndex", 0)),
        precip_mm=float(cond.get("precipMM", 0)),
        precip_in=float(cond.get("precipInches", 0)),
        weather_code=int(cond.get("weatherCode", 0)),
        weather_desc=parse_weather_description(cond.get("weatherDesc", [])),
        wind_speed_kmph=float(cond.get("windspeedKmph", 0)),
        wind_speed_miles=float(cond.get("windspeedMiles", 0)),
        wind_dir_degree=int(cond.get("winddirDegree", 0)),
        wind_dir_16_point=cond.get("winddir16Point", ""),
        observation_time=cond.get("observation_time", ""),
        local_obs_datetime=cond.get("localObsDateTime", ""),
    )


def parse_hourly_forecast(data: list[dict[str, Any]]) -> list[HourlyForecast]:
    """Parse hourly forecast from API response."""
    forecasts = []
    for hour in data:
        forecast = HourlyForecast(
            time=int(hour.get("time", 0)),
            temp_c=float(hour.get("tempC", 0)),
            temp_f=float(hour.get("tempF", 0)),
            feels_like_c=float(hour.get("FeelsLikeC", 0)),
            feels_like_f=float(hour.get("FeelsLikeF", 0)),
            humidity=int(hour.get("humidity", 0)),
            cloud_cover=int(hour.get("cloudcover", 0)),
            pressure_mb=float(hour.get("pressure", 0)),
            pressure_in=float(hour.get("pressureInches", 0)),
            visibility_km=float(hour.get("visibility", 0)),
            visibility_miles=float(hour.get("visibilityMiles", 0)),
            uv_index=int(hour.get("uvIndex", 0)),
            precip_mm=float(hour.get("precipMM", 0)),
            precip_in=float(hour.get("precipInches", 0)),
            weather_code=int(hour.get("weatherCode", 0)),
            weather_desc=parse_weather_description(hour.get("weatherDesc", [])),
            wind_speed_kmph=float(hour.get("windspeedKmph", 0)),
            wind_speed_miles=float(hour.get("windspeedMiles", 0)),
            wind_dir_degree=int(hour.get("winddirDegree", 0)),
            wind_dir_16_point=hour.get("winddir16Point", ""),
            chance_of_rain=int(hour.get("chanceofrain", 0)),
            chance_of_snow=int(hour.get("chanceofsnow", 0)),
            chance_of_thunder=int(hour.get("chanceofthunder", 0)),
            chance_of_fog=int(hour.get("chanceoffog", 0)),
            chance_of_frost=int(hour.get("chanceoffrost", 0)),
            chance_of_high_temp=int(hour.get("chanceofhightemp", 0)),
            chance_of_overcast=int(hour.get("chanceofovercast", 0)),
            chance_of_sunshine=int(hour.get("chanceofsunshine", 0)),
            chance_of_windy=int(hour.get("chanceofwindy", 0)),
            dew_point_c=float(hour.get("DewPointC", 0)),
            dew_point_f=float(hour.get("DewPointF", 0)),
            heat_index_c=float(hour.get("HeatIndexC", 0)),
            heat_index_f=float(hour.get("HeatIndexF", 0)),
            wind_chill_c=float(hour.get("WindChillC", 0)),
            wind_chill_f=float(hour.get("WindChillF", 0)),
            wind_gust_kmph=float(hour.get("WindGustKmph", 0)),
            wind_gust_miles=float(hour.get("WindGustMiles", 0)),
            short_rad=float(hour.get("shortRad", 0)),
            diff_rad=float(hour.get("diffRad", 0)),
        )
        forecasts.append(forecast)
    return forecasts


def parse_astronomy(data: list[dict[str, Any]]) -> Astronomy:
    """Parse astronomy data from API response."""
    if not data:
        raise ValueError("No astronomy data")

    astro = data[0]
    return Astronomy(
        sunrise=astro.get("sunrise", ""),
        sunset=astro.get("sunset", ""),
        moonrise=astro.get("moonrise", ""),
        moonset=astro.get("moonset", ""),
        moon_phase=astro.get("moon_phase", ""),
        moon_illumination=int(astro.get("moon_illumination", 0)),
    )


def parse_daily_forecast(data: list[dict[str, Any]]) -> list[DailyForecast]:
    """Parse daily forecast from API response."""
    forecasts = []
    for day in data:
        forecast = DailyForecast(
            date=day.get("date", ""),
            date_epoch=int(day.get("date_epoch", 0)),
            max_temp_c=float(day.get("maxtempC", 0)),
            max_temp_f=float(day.get("maxtempF", 0)),
            min_temp_c=float(day.get("mintempC", 0)),
            min_temp_f=float(day.get("mintempF", 0)),
            avg_temp_c=float(day.get("avgtempC", 0)),
            avg_temp_f=float(day.get("avgtempF", 0)),
            sun_hour=float(day.get("sunHour", 0)),
            total_snow_cm=float(day.get("totalSnow_cm", 0)),
            uv_index=int(day.get("uvIndex", 0)),
            astronomy=parse_astronomy(day.get("astronomy", [])),
            hourly=parse_hourly_forecast(day.get("hourly", [])),
        )
        forecasts.append(forecast)
    return forecasts


def parse_weather_data(data: dict[str, Any]) -> WeatherData:
    """Parse complete weather data from API response."""
    return WeatherData(
        location=parse_location(data.get("nearest_area", [])),
        current_condition=parse_current_condition(data.get("current_condition", [])),
        forecast=parse_daily_forecast(data.get("weather", [])),
        request_query=data.get("request", [{}])[0].get("query", ""),
        request_type=data.get("request", [{}])[0].get("type", ""),
    )
