"""Build data/bishkek_pm25.csv: daily evening PM2.5 (AirNow) joined with weather at the same hour (Open-Meteo)."""
from pathlib import Path

import pandas as pd

from src.air import fetch_air
from src.weather import fetch_weather

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "bishkek_pm25.csv"


def download(path=CSV_PATH):
    air = fetch_air()
    weather = fetch_weather()
    evening = weather[weather.index.hour == 21]  # 21:00 Bishkek time, matches the 15:00 UTC AirNow file
    evening = evening.set_index(evening.index.date)
    df = air.join(evening, how="left")
    df.index.name = "date"
    df.to_csv(path)
    return df


if __name__ == "__main__":
    df = download()
    print(f"Saved {len(df)} rows x {df.shape[1]} columns to {CSV_PATH}")
