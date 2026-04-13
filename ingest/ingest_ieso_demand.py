#!/usr/bin/env python3
"""
Ontario electricity demand ingestion for Assignment 4.
Downloads annual IESO hourly demand CSV files that overlap the project date window.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import requests


DEFAULT_START_DATE = "2025-04-01"
DEFAULT_END_DATE = "2026-03-31"
BASE_URL = "https://reports-public.ieso.ca/public/Demand"


def iter_years(start_date: str, end_date: str) -> range:
    start_year = datetime.fromisoformat(start_date).year
    end_year = datetime.fromisoformat(end_date).year
    return range(start_year, end_year + 1)


def ingest_ieso_demand() -> None:
    """Download yearly demand reports into the bronze layer."""

    start_date = os.getenv("WEATHER_START_DATE", DEFAULT_START_DATE)
    end_date = os.getenv("WEATHER_END_DATE", DEFAULT_END_DATE)

    session = requests.Session()
    session.trust_env = False

    bronze_dir = Path("data/bronze/ieso")
    bronze_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    for year in iter_years(start_date, end_date):
        url = f"{BASE_URL}/PUB_Demand_{year}.csv"
        output_path = bronze_dir / f"PUB_Demand_{year}_{timestamp}.csv"

        try:
            response = session.get(url, timeout=60)
            response.raise_for_status()
            output_path.write_bytes(response.content)
            print(f"Saved {output_path}")
        except Exception as exc:
            print(f"Failed to fetch IESO demand for {year}: {exc}")


if __name__ == "__main__":
    ingest_ieso_demand()
    print("IESO demand ingestion complete.")
