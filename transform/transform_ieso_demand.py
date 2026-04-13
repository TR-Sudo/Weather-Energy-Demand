#!/usr/bin/env python3
"""
Transform raw IESO hourly demand CSV files into clean hourly and daily datasets.
"""

from io import StringIO
from pathlib import Path

import pandas as pd


def _read_report(path: Path) -> pd.DataFrame:
    lines = path.read_text(encoding="utf-8").splitlines()
    header_index = next(i for i, line in enumerate(lines) if line.startswith("Date,Hour"))
    csv_text = "\n".join(lines[header_index:])

    df = pd.read_csv(StringIO(csv_text))
    df.columns = [column.strip().lower().replace(" ", "_") for column in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
    df["market_demand"] = pd.to_numeric(df["market_demand"], errors="coerce")
    df["ontario_demand"] = pd.to_numeric(df["ontario_demand"], errors="coerce")
    return df


def transform_ieso_demand() -> None:
    raw_dir = Path("data/raw/ieso")
    clean_dir = Path("data/clean")
    clean_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(raw_dir.glob("PUB_Demand_*.csv"))
    if not files:
        raise FileNotFoundError("No raw IESO demand files found.")

    hourly = pd.concat((_read_report(path) for path in files), ignore_index=True)
    hourly = (
        hourly.sort_values(["date", "hour"])
        .drop_duplicates(subset=["date", "hour"], keep="last")
        .reset_index(drop=True)
    )

    daily = (
        hourly.groupby("date", as_index=False)
        .agg(
            ontario_demand_avg_mw=("ontario_demand", "mean"),
            ontario_demand_peak_mw=("ontario_demand", "max"),
            ontario_demand_min_mw=("ontario_demand", "min"),
            ontario_demand_std_mw=("ontario_demand", "std"),
            market_demand_avg_mw=("market_demand", "mean"),
        )
    )

    peak_hours = hourly.loc[hourly.groupby("date")["ontario_demand"].idxmax(), ["date", "hour"]].rename(
        columns={"hour": "ontario_peak_hour"}
    )
    daily = daily.merge(peak_hours, on="date", how="left")
    daily["demand_range_mw"] = daily["ontario_demand_peak_mw"] - daily["ontario_demand_min_mw"]

    hourly.to_csv(clean_dir / "ieso_demand_hourly_clean.csv", index=False)
    daily.to_csv(clean_dir / "ieso_demand_daily.csv", index=False)

    print("Saved", clean_dir / "ieso_demand_hourly_clean.csv")
    print("Saved", clean_dir / "ieso_demand_daily.csv")


if __name__ == "__main__":
    transform_ieso_demand()
