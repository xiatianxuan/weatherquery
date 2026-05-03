"""Async usage example for weatherquery."""

import asyncio
from weatherquery import AsyncWeatherClient


async def main():
    """Demonstrate async usage of weatherquery."""

    # Create an async client
    async with AsyncWeatherClient() as client:
        # Get current weather in JSON format
        print("=== Current Weather (JSON) ===")
        weather = await client.get_weather("Beijing", format="json")
        print(f"Location: {weather.location.area_name}, {weather.location.country}")
        print(f"Temperature: {weather.current_condition.temp_c}°C")
        print(f"Weather: {weather.current_condition.weather_desc.value}")
        print(f"Humidity: {weather.current_condition.humidity}%")
        print()

        # Get weather in plain text format (no emoji)
        print("=== Weather (Plain Text, No Emoji) ===")
        plain_weather = await client.get_weather("London", format="plaintext")
        print(plain_weather)
        print()

        # Get forecast
        print("=== 3-Day Forecast ===")
        forecast = await client.get_forecast("Paris", days=3, format="json")
        print(f"Location: {forecast.location.area_name}")
        for day in forecast.forecast:
            print(f"  {day.date}: {day.min_temp_c}°C - {day.max_temp_c}°C")
        print()

        # Concurrent requests
        print("=== Concurrent Requests ===")
        cities = ["Tokyo", "Berlin", "New York", "Sydney"]
        tasks = [client.get_weather(city, format="json") for city in cities]
        results = await asyncio.gather(*tasks)

        for city, result in zip(cities, results):
            print(
                f"{city}: {result.current_condition.temp_c}°C, {result.current_condition.weather_desc.value}"
            )


if __name__ == "__main__":
    asyncio.run(main())
