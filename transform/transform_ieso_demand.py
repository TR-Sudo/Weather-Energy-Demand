#!/usr/bin/env python3
"""
Transform raw IESO hourly demand data into silver-layer hourly and daily datasets.
"""

from __future__ import annotations

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
    df["source_file"] = path.name
    df["source_modified_at"] = pd.Timestamp(path.stat().st_mtime, unit="s")
    return df


def transform_ieso_demand() -> tuple[pd.DataFrame, pd.DataFrame]:
    bronze_dir = Path("data/bronze/ieso")
    silver_dir = Path("data/silver")
    silver_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(bronze_dir.glob("PUB_Demand_*.csv"))
    if not files:
        raise FileNotFoundError("No bronze IESO demand files found.")

    hourly = pd.concat((_read_report(path) for path in files), ignore_index=True)
    hourly = (
        hourly.sort_values(["date", "hour", "source_modified_at"])
        .drop_duplicates(subset=["date", "hour"], keep="last")
        .sort_values(["date", "hour"])
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
        .sort_values("date")
        .reset_index(drop=True)
    )

    peak_hour_idx = hourly.groupby("date")["ontario_demand"].idxmax()
    peak_hours = hourly.loc[peak_hour_idx, ["date", "hour"]].rename(
        columns={"hour": "ontario_peak_hour"}
    )
    daily = daily.merge(peak_hours, on="date", how="left")
    daily["demand_range_mw"] = daily["ontario_demand_peak_mw"] - daily["ontario_demand_min_mw"]

    hourly.to_csv(silver_dir / "ieso_demand_hourly_clean.csv", index=False)
    daily.to_csv(silver_dir / "ieso_demand_daily.csv", index=False)

    print("Saved data/silver/ieso_demand_hourly_clean.csv")
    print("Saved data/silver/ieso_demand_daily.csv")

    return hourly, daily


if __name__ == "__main__":
    transform_ieso_demand()
