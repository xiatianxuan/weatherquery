"""Command-line interface for weatherquery."""

import typer
from typing import Optional

from .client import WeatherClient
from .config import create_config
from .exceptions import WeatherQueryError
from .formatters import get_formatter, PlainTextFormatter

app = typer.Typer(
    name="weatherquery",
    help="Query weather data from wttr.in API",
    no_args_is_help=True,
)


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        typer.echo("weatherquery 0.1.0")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """Weather query tool using wttr.in API."""
    pass


@app.command()
def weather(
    location: Optional[str] = typer.Argument(
        None, help="Location to query (city name, coordinates, IP, etc.)"
    ),
    format: str = typer.Option(
        "text",
        "--format",
        "-f",
        help="Output format (json, text, plain, plaintext, custom)",
    ),
    lang: Optional[str] = typer.Option(
        None, "--lang", "-l", help="Language code (e.g., zh, en)"
    ),
    units: Optional[str] = typer.Option(
        None, "--units", "-u", help="Units system (metric, imperial)"
    ),
    custom_format: Optional[str] = typer.Option(
        None,
        "--custom-format",
        "-c",
        help="Custom format string for 'custom' format type",
    ),
):
    """Get current weather for a location."""
    try:
        config = create_config()

        with WeatherClient(config=config) as client:
            # For plaintext and plain formats, we need JSON data from API
            if format in ("plaintext", "plain"):
                data = client.get_weather(
                    location=location,
                    format="json",
                    lang=lang,
                    units=units,
                )
                formatter = PlainTextFormatter()
                typer.echo(formatter.format(data))
                return

            # For other non-JSON formats, the API returns text directly
            if format != "json" and format != "custom":
                data = client.get_weather(
                    location=location,
                    format=format,
                    lang=lang,
                    units=units,
                )
                typer.echo(data)
                return

            # For JSON and custom formats
            data = client.get_weather(
                location=location,
                format="json",
                lang=lang,
                units=units,
            )

            if format == "json":
                formatter = get_formatter("json")
            elif format == "custom":
                if not custom_format:
                    typer.echo(
                        "Error: --custom-format is required when using 'custom' format",
                        err=True,
                    )
                    raise typer.Exit(1)
                formatter = get_formatter("custom", format_string=custom_format)
            else:
                formatter = get_formatter(format)

            typer.echo(formatter.format(data))

    except WeatherQueryError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def forecast(
    location: Optional[str] = typer.Argument(None, help="Location to query"),
    days: int = typer.Option(
        3, "--days", "-d", min=1, max=3, help="Number of forecast days (1-3)"
    ),
    format: str = typer.Option(
        "text",
        "--format",
        "-f",
        help="Output format (json, text, plain, plaintext, custom)",
    ),
    lang: Optional[str] = typer.Option(
        None, "--lang", "-l", help="Language code (e.g., zh, en)"
    ),
    units: Optional[str] = typer.Option(
        None, "--units", "-u", help="Units system (metric, imperial)"
    ),
    custom_format: Optional[str] = typer.Option(
        None,
        "--custom-format",
        "-c",
        help="Custom format string for 'custom' format type",
    ),
):
    """Get weather forecast for a location."""
    try:
        config = create_config()

        with WeatherClient(config=config) as client:
            # For plaintext and plain formats, we need JSON data from API
            if format in ("plaintext", "plain"):
                data = client.get_forecast(
                    location=location,
                    days=days,
                    format="json",
                    lang=lang,
                    units=units,
                )
                formatter = PlainTextFormatter()
                typer.echo(formatter.format(data))
                return

            # For other non-JSON formats, the API returns text directly
            if format != "json" and format != "custom":
                data = client.get_forecast(
                    location=location,
                    days=days,
                    format=format,
                    lang=lang,
                    units=units,
                )
                typer.echo(data)
                return

            # For JSON and custom formats
            data = client.get_forecast(
                location=location,
                days=days,
                format="json",
                lang=lang,
                units=units,
            )

            if format == "json":
                formatter = get_formatter("json")
            elif format == "custom":
                if not custom_format:
                    typer.echo(
                        "Error: --custom-format is required when using 'custom' format",
                        err=True,
                    )
                    raise typer.Exit(1)
                formatter = get_formatter("custom", format_string=custom_format)
            else:
                formatter = get_formatter(format)

            typer.echo(formatter.format(data))

    except WeatherQueryError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Unexpected error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
