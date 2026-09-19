import os
import requests
from typing import Any
from fastmcp import FastMCP

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

mcp = FastMCP("Weather MCP Server")


def _get_api_key() -> str:
    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is missing.")
    return OPENWEATHER_API_KEY


@mcp.tool()
def get_current_weather(city: str) -> dict[str, Any]:
    city = city.strip()

    if not city:
        raise ValueError("city cannot be empty")

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": _get_api_key(),
            "units": "metric",
        },
        timeout=20,
    )

    response.raise_for_status()
    data = response.json()

    return {
        "city": data["name"],
        "temperature_c": data["main"]["temp"],
        "feels_like_c": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }


@mcp.tool()
def get_forecast(city: str) -> dict[str, Any]:
    city = city.strip()

    if not city:
        raise ValueError("city cannot be empty")

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast",
        params={
            "q": city,
            "appid": _get_api_key(),
            "units": "metric",
        },
        timeout=20,
    )

    response.raise_for_status()
    data = response.json()

    return {
        "city": data.get("city", {}).get("name", city),
        "forecast": [
            {
                "datetime": item["dt_txt"],
                "temperature_c": item["main"]["temp"],
                "condition": item["weather"][0]["description"],
            }
            for item in data.get("list", [])[:5]
        ],
    }


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000,
    )