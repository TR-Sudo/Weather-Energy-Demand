#!/usr/bin/env python3
"""
Fetch one year of daily GTA weather data and save raw JSON files.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import requests

DEFAULT_START_DATE = "2025-04-01"
DEFAULT_END_DATE = "2026-03-31"
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
CITIES = {
    "toronto": {"lat": 43.65, "lon": -79.38},
    "oshawa": {"lat": 43.89, "lon": -79.05},
    "barrie": {"lat": 44.39, "lon": -79.69},
}
DAILY_VARIABLES = "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"


def ingest_weather() -> None:
    start_date = os.getenv("WEATHER_START_DATE", DEFAULT_START_DATE)
    end_date = os.getenv("WEATHER_END_DATE", DEFAULT_END_DATE)
    output_dir = Path("data/raw/weather")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    for city, coords in CITIES.items():
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "start_date": start_date,
            "end_date": end_date,
            "daily": DAILY_VARIABLES,
            "timezone": "auto",
        }
        response = requests.get(BASE_URL, params=params, timeout=60)
        response.raise_for_status()

        path = output_dir / f"{city}_weather_{timestamp}.json"
        path.write_text(json.dumps(response.json(), indent=2), encoding="utf-8")
        print("Saved", path)


if __name__ == "__main__":
    ingest_weather()
