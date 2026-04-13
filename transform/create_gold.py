#!/usr/bin/env python3
"""
Build the clean gold datasets used by the Streamlit app.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEASON_MAP = {
    12: "Winter",
    1: "Winter",
    2: "Winter",
    3: "Spring",
    4: "Spring",
    5: "Spring",
    6: "Summer",
    7: "Summer",
    8: "Summer",
    9: "Fall",
    10: "Fall",
    11: "Fall",
}


def create_gold_layer() -> None:
    clean_dir = Path("data/clean")
    gold_dir = Path("data/gold")
    gold_dir.mkdir(parents=True, exist_ok=True)

    weather = pd.read_csv(clean_dir / "weather_daily_clean.csv", parse_dates=["date"])
    demand = pd.read_csv(clean_dir / "ieso_demand_daily.csv", parse_dates=["date"])

    weather = (
        weather.sort_values(["date", "city", "source_file"])
        .drop_duplicates(subset=["date", "city"], keep="last")
        .reset_index(drop=True)
    )

    weather["temp_mean_celsius"] = (weather["temp_max_celsius"] + weather["temp_min_celsius"]) / 2
    weather["is_cold_day"] = (weather["temp_min_celsius"] <= 0).astype(int)
    weather["is_hot_day"] = (weather["temp_max_celsius"] >= 25).astype(int)
    weather["is_rainy_day"] = (weather["precipitation_mm"] > 0).astype(int)
    weather["is_windy_day"] = (weather["wind_speed_max_kmh"] >= 30).astype(int)
    weather["day_of_week"] = weather["date"].dt.day_name()
    weather["is_weekend"] = (weather["date"].dt.weekday >= 5).astype(int)
    weather["month"] = weather["date"].dt.month
    weather["season"] = weather["month"].map(SEASON_MAP)

    city_gold = weather[
        [
            "date",
            "city",
            "latitude",
            "longitude",
            "temp_max_celsius",
            "temp_min_celsius",
            "temp_mean_celsius",
            "temp_range_celsius",
            "precipitation_mm",
            "wind_speed_max_kmh",
            "is_cold_day",
            "is_hot_day",
            "is_rainy_day",
            "is_windy_day",
            "day_of_week",
            "is_weekend",
            "month",
            "season",
        ]
    ].copy()
    city_gold.to_csv(gold_dir / "weather_analysis_ready.csv", index=False)

    daily_weather = city_gold.groupby("date", as_index=False).agg(
        avg_temp_max_celsius=("temp_max_celsius", "mean"),
        avg_temp_min_celsius=("temp_min_celsius", "mean"),
        avg_temp_mean_celsius=("temp_mean_celsius", "mean"),
        avg_temp_range_celsius=("temp_range_celsius", "mean"),
        total_precipitation_mm=("precipitation_mm", "sum"),
        avg_precipitation_mm=("precipitation_mm", "mean"),
        max_wind_speed_kmh=("wind_speed_max_kmh", "max"),
        avg_wind_speed_kmh=("wind_speed_max_kmh", "mean"),
        rainy_city_count=("is_rainy_day", "sum"),
        hot_city_count=("is_hot_day", "sum"),
        cold_city_count=("is_cold_day", "sum"),
    )

    daily_weather["day_of_week"] = daily_weather["date"].dt.day_name()
    daily_weather["is_weekend"] = (daily_weather["date"].dt.weekday >= 5).astype(int)
    daily_weather["month"] = daily_weather["date"].dt.month
    daily_weather["season"] = daily_weather["month"].map(SEASON_MAP)
    daily_weather["temp_extreme_flag"] = (
        (daily_weather["avg_temp_max_celsius"] >= 25)
        | (daily_weather["avg_temp_min_celsius"] <= 0)
    ).astype(int)
    daily_weather["temp_deviation_from_18"] = (daily_weather["avg_temp_mean_celsius"] - 18).abs()
    daily_weather["comfort_gap_celsius"] = daily_weather["avg_temp_mean_celsius"] - 18
    daily_weather["wet_day_flag"] = (daily_weather["total_precipitation_mm"] > 0).astype(int)

    final_df = daily_weather.merge(demand, on="date", how="inner")
    demand_threshold = final_df["ontario_demand_peak_mw"].quantile(0.75)
    final_df["high_demand_day"] = (final_df["ontario_demand_peak_mw"] >= demand_threshold).astype(int)
    final_df["demand_change_mw"] = final_df["ontario_demand_peak_mw"].diff()
    final_df["demand_direction"] = final_df["demand_change_mw"].apply(
        lambda x: "Up" if x > 0 else "Down" if x < 0 else "Flat"
    )

    daily_weather.to_csv(gold_dir / "weather_daily_summary.csv", index=False)
    final_df.to_csv(gold_dir / "final_dataset.csv", index=False)

    print("Saved", gold_dir / "weather_analysis_ready.csv")
    print("Saved", gold_dir / "weather_daily_summary.csv")
    print("Saved", gold_dir / "final_dataset.csv")


if __name__ == "__main__":
    create_gold_layer()
