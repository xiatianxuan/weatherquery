# WeatherQuery

A Python library and CLI tool for querying weather data from [wttr.in](https://wttr.in) API.

## Features

- **Multiple query methods**: City name, coordinates, IP address, airport code
- **Multiple output formats**: JSON, text, plain text (no emoji), custom format
- **Synchronous and asynchronous clients**
- **Configurable caching**: Memory cache, file cache, or no cache
- **Multiple configuration methods**: Code, config file, environment variables
- **CLI tool**: Command-line interface for quick weather queries
- **Type hints**: Full type annotation support
- **Error handling**: Comprehensive exception hierarchy

## Installation

```bash
# Using uv (recommended)
uv add weatherquery

# Using pip
pip install weatherquery
```

## Quick Start

### As a Library

```python
from weatherquery import WeatherClient

# Create a client
with WeatherClient() as client:
    # Get current weather
    weather = client.get_weather("Beijing", format="json")
    print(f"Temperature: {weather.current_condition.temp_c}°C")
    print(f"Weather: {weather.current_condition.weather_desc.value}")

    # Get forecast
    forecast = client.get_forecast("London", days=3, format="json")
    for day in forecast.forecast:
        print(f"{day.date}: {day.min_temp_c}°C - {day.max_temp_c}°C")
```

### Async Usage

```python
import asyncio
from weatherquery import AsyncWeatherClient

async def main():
    async with AsyncWeatherClient() as client:
        weather = await client.get_weather("Tokyo", format="json")
        print(f"Temperature: {weather.current_condition.temp_c}°C")

asyncio.run(main())
```

### CLI Usage

```bash
# Get current weather (plain text, no emoji)
weatherquery weather Beijing --format plaintext

# Get weather in JSON format
weatherquery weather Beijing --format json

# Get weather in Chinese
weatherquery weather Beijing --lang zh

# Get 3-day forecast
weatherquery forecast Beijing --days 3

# Get weather with custom format
weatherquery weather Beijing --format custom --custom-format "{location}: {temp_c}°C"

# Show help
weatherquery --help
```

## Configuration

### Configuration File

Create a `.weatherquery.toml` file in your home directory or project directory:

```toml
default_location = "Beijing"
default_language = "en"
default_units = "metric"

[cache]
enabled = true
cache_type = "memory"  # "memory", "file", or "none"
ttl_seconds = 300

[request]
timeout = 10
max_retries = 3
retry_delay = 1.0
```

### Environment Variables

```bash
export WEATHERQUERY_LOCATION="Beijing"
export WEATHERQUERY_LANGUAGE="zh"
export WEATHERQUERY_UNITS="metric"
export WEATHERQUERY_CACHE_ENABLED="true"
export WEATHERQUERY_CACHE_TYPE="memory"
export WEATHERQUERY_CACHE_TTL="300"
export WEATHERQUERY_TIMEOUT="10"
export WEATHERQUERY_MAX_RETRIES="3"
```

## Output Formats

### JSON Format

```python
weather = client.get_weather("Beijing", format="json")
# Returns WeatherData object with structured data
```

### Text Format

```python
text = client.get_weather("Beijing", format="text")
# Returns text weather report from API
```

### Plain Text Format (No Emoji)

```python
plain = client.get_weather("Beijing", format="plaintext")
# Returns simple one-line weather summary without emoji
# Example: "Beijing, China: Sunny, 19.0°C (feels like 19.0°C), Wind: 13.0 km/h N, Humidity: 19%"
```

### Custom Format

```python
custom = client.get_weather(
    "Beijing",
    format="custom",
    custom_format="{location}, {country}: {temp_c}°C, {weather_desc}"
)
# Returns formatted string using custom template
```

## Error Handling

```python
from weatherquery import WeatherClient, LocationNotFoundError, APIError

try:
    weather = client.get_weather("InvalidLocation", format="json")
except LocationNotFoundError:
    print("Location not found")
except APIError as e:
    print(f"API error: {e.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Caching

### Memory Cache

```python
from weatherquery import WeatherClient
from weatherquery.config import create_config

config = create_config(
    cache_enabled=True,
    cache_type="memory",
    cache_ttl=300
)

with WeatherClient(config=config) as client:
    # First request - hits API
    weather1 = client.get_weather("Beijing")
    
    # Second request - returns cached result
    weather2 = client.get_weather("Beijing")
```

### File Cache

```python
config = create_config(
    cache_enabled=True,
    cache_type="file",
    cache_ttl=3600,
    cache_dir="/tmp/weatherquery_cache"
)
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/weatherquery.git
cd weatherquery

# Install dependencies
uv install

# Run tests
uv run pytest

# Run linting
uv tool run ruff check .
uv tool run ruff format .
```

### Running Tests

```bash
# Unit tests
uv run pytest tests/ -v

# Integration tests (requires internet)
uv run pytest tests/ -v -m integration

# Async tests
uv run pytest tests/ -v -m asyncio
```

## API Reference

### WeatherClient

- `get_weather(location, format="json", lang=None, units=None, **kwargs)`
- `get_forecast(location, days=3, format="json", lang=None, units=None, **kwargs)`
- `close()`

### AsyncWeatherClient

- `get_weather(location, format="json", lang=None, units=None, **kwargs)`
- `get_forecast(location, days=3, format="json", lang=None, units=None, **kwargs)`
- `close()`

### Models

- `WeatherData`: Complete weather data response
- `CurrentCondition`: Current weather conditions
- `DailyForecast`: Daily weather forecast
- `HourlyForecast`: Hourly weather forecast
- `Location`: Location information
- `WeatherDescription`: Weather description with icon
- `Astronomy`: Astronomical data

### Formatters

- `Formatter`: Abstract base class for formatters
- `JsonFormatter`: Format weather data as JSON
- `TextFormatter`: Format weather data as text
- `PlainFormatter`: Format weather data as plain text
- `PlainTextFormatter`: Format weather data as plain text without emoji
- `CustomFormatter`: Format weather data using custom format string
- `get_formatter`: Get formatter instance by type

### Exceptions

- `WeatherQueryError`: Base exception
- `APIError`: API request error
- `LocationNotFoundError`: Location not found
- `RateLimitExceededError`: Rate limit exceeded
- `NetworkError`: Network connection error
- `TimeoutError`: Request timeout
- `ParseError`: Response parsing error
- `ConfigError`: Configuration error
- `CacheError`: Cache operation error

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run tests and linting
6. Submit a pull request

## Acknowledgments

- [wttr.in](https://wttr.in) for the weather API
- [httpx](https://github.com/encode/httpx) for HTTP client
- [typer](https://github.com/tiangolo/typer) for CLI framework
