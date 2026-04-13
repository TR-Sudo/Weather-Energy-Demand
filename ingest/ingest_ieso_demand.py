#!/usr/bin/env python3
"""
Fetch one year of Ontario IESO demand CSV files and save raw files.
"""

import os
from datetime import datetime
from pathlib import Path

import requests

DEFAULT_START_DATE = "2025-04-01"
DEFAULT_END_DATE = "2026-03-31"
BASE_URL = "https://reports-public.ieso.ca/public/Demand"


def ingest_ieso_demand() -> None:
    start_date = os.getenv("WEATHER_START_DATE", DEFAULT_START_DATE)
    end_date = os.getenv("WEATHER_END_DATE", DEFAULT_END_DATE)
    start_year = datetime.fromisoformat(start_date).year
    end_year = datetime.fromisoformat(end_date).year

    output_dir = Path("data/raw/ieso")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    session = requests.Session()
    for year in range(start_year, end_year + 1):
        url = f"{BASE_URL}/PUB_Demand_{year}.csv"
        response = session.get(url, timeout=60)
        response.raise_for_status()

        path = output_dir / f"PUB_Demand_{year}_{timestamp}.csv"
        path.write_bytes(response.content)
        print("Saved", path)


if __name__ == "__main__":
    ingest_ieso_demand()
    print("IESO demand ingestion complete.")
