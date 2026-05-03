"""Basic usage example for weatherquery."""

from weatherquery import WeatherClient


def main():
    """Demonstrate basic usage of weatherquery."""

    # Create a client
    with WeatherClient() as client:
        # Get current weather in JSON format
        print("=== Current Weather (JSON) ===")
        weather = client.get_weather("Beijing", format="json")
        print(f"Location: {weather.location.area_name}, {weather.location.country}")
        print(f"Temperature: {weather.current_condition.temp_c}°C")
        print(f"Weather: {weather.current_condition.weather_desc.value}")
        print(f"Humidity: {weather.current_condition.humidity}%")
        print()

        # Get weather in plain text format (no emoji)
        print("=== Weather (Plain Text, No Emoji) ===")
        plain_weather = client.get_weather("Tokyo", format="plaintext")
        print(plain_weather)
        print()

        # Get forecast
        print("=== 3-Day Forecast ===")
        forecast = client.get_forecast("Paris", days=3, format="json")
        print(f"Location: {forecast.location.area_name}")
        for day in forecast.forecast:
            print(f"  {day.date}: {day.min_temp_c}°C - {day.max_temp_c}°C")
        print()

        # Get weather with custom format
        print("=== Custom Format ===")
        custom_weather = client.get_weather(
            "Berlin",
            format="custom",
            custom_format="{location}, {country}: {temp_c}°C, {weather_desc}",
        )
        print(custom_weather)
        print()

        # Get weather with language
        print("=== Weather in Chinese ===")
        chinese_weather = client.get_weather("Shanghai", format="json", lang="zh")
        print(f"Location: {chinese_weather.location.area_name}")
        print(f"Weather: {chinese_weather.current_condition.weather_desc.value}")
        print()

        # Get weather with imperial units
        print("=== Weather in Imperial Units ===")
        imperial_weather = client.get_weather(
            "New York", format="json", units="imperial"
        )
        print(f"Location: {imperial_weather.location.area_name}")
        print(f"Temperature: {imperial_weather.current_condition.temp_f}°F")
        print(f"Wind: {imperial_weather.current_condition.wind_speed_miles} mph")


if __name__ == "__main__":
    main()
