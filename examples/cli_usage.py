"""CLI usage example for weatherquery.

This example demonstrates how to use the weatherquery CLI tool.

Usage:
    # Get current weather (plain text, no emoji)
    weatherquery weather Beijing --format plaintext

    # Get weather in JSON format
    weatherquery weather Beijing --format json

    # Get weather in Chinese
    weatherquery weather Beijing --lang zh

    # Get weather in imperial units
    weatherquery weather Beijing --units imperial

    # Get 3-day forecast
    weatherquery forecast Beijing --days 3

    # Get forecast in JSON format
    weatherquery forecast Beijing --days 3 --format json

    # Get weather with custom format
    weatherquery weather Beijing --format custom --custom-format "{location}: {temp_c}°C"

    # Show version
    weatherquery --version

    # Show help
    weatherquery --help
    weatherquery weather --help
    weatherquery forecast --help
"""

import subprocess


def run_command(cmd: list[str]) -> str:
    """Run a command and return output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


def main():
    """Demonstrate CLI usage."""

    print("=== WeatherQuery CLI Examples ===\n")

    # Example 1: Plain text format (no emoji)
    print("1. Plain text format (no emoji):")
    print("   Command: weatherquery weather Beijing --format plaintext")
    output = run_command(
        ["weatherquery", "weather", "Beijing", "--format", "plaintext"]
    )
    print(f"   Output:\n{output}")

    # Example 2: JSON format
    print("\n2. JSON format:")
    print("   Command: weatherquery weather London --format json")
    output = run_command(["weatherquery", "weather", "London", "--format", "json"])
    print(f"   Output (first 500 chars):\n{output[:500]}...")

    # Example 3: Forecast
    print("\n3. 3-day forecast:")
    print("   Command: weatherquery forecast Tokyo --days 3")
    output = run_command(["weatherquery", "forecast", "Tokyo", "--days", "3"])
    print(f"   Output:\n{output}")

    # Example 4: Chinese language
    print("\n4. Chinese language:")
    print("   Command: weatherquery weather Shanghai --lang zh")
    output = run_command(["weatherquery", "weather", "Shanghai", "--lang", "zh"])
    print(f"   Output:\n{output}")

    # Example 5: Imperial units
    print("\n5. Imperial units:")
    print("   Command: weatherquery weather 'New York' --units imperial")
    output = run_command(["weatherquery", "weather", "New York", "--units", "imperial"])
    print(f"   Output:\n{output}")

    # Example 6: Custom format
    print("\n6. Custom format:")
    print(
        '   Command: weatherquery weather Berlin --format custom --custom-format "{location}: {temp_c}°C"'
    )
    output = run_command(
        [
            "weatherquery",
            "weather",
            "Berlin",
            "--format",
            "custom",
            "--custom-format",
            "{location}: {temp_c}°C",
        ]
    )
    print(f"   Output:\n{output}")

    # Example 7: Version
    print("\n7. Version:")
    print("   Command: weatherquery --version")
    output = run_command(["weatherquery", "--version"])
    print(f"   Output: {output}")


if __name__ == "__main__":
    main()
