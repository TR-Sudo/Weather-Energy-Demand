#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


bronze_dir = Path("data/bronze/weather")
silver_dir = Path("data/silver")
silver_dir.mkdir(parents=True, exist_ok=True)

rows = []
for path in sorted(bronze_dir.glob("*.json")):
    city = path.stem.split("_weather_")[0]
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)

    daily = raw.get("daily", {})
    for index, date in enumerate(daily.get("time", [])):
        rows.append(
            {
                "date": date,
                "city": city,
                "latitude": raw.get("latitude"),
                "longitude": raw.get("longitude"),
                "timezone": raw.get("timezone"),
                "temp_max_celsius": daily.get("temperature_2m_max", [None])[index],
                "temp_min_celsius": daily.get("temperature_2m_min", [None])[index],
                "precipitation_mm": daily.get("precipitation_sum", [None])[index],
                "wind_speed_max_kmh": daily.get("wind_speed_10m_max", [None])[index],
                "source_file": path.name,
            }
        )

df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"]).dt.date

for column in [
    "temp_max_celsius",
    "temp_min_celsius",
    "precipitation_mm",
    "wind_speed_max_kmh",
]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df["temp_range_celsius"] = df["temp_max_celsius"] - df["temp_min_celsius"]
df = df.sort_values(["date", "city"]).reset_index(drop=True)

df.to_csv(silver_dir / "weather_daily_clean.csv", index=False)
print("Saved data/silver/weather_daily_clean.csv")
