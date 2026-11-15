"""Download hourly air quality and weather for Bishkek from Open-Meteo (free, no API key).

Note: air quality values are modelled (CAMS reanalysis), not readings from a physical station.
"""
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "bishkek_air_quality.csv"
COMMON = {"latitude": 42.87, "longitude": 74.59, "start_date": "2023-01-01",
          "end_date": "2025-12-31", "timezone": "Asia/Bishkek"}
AIR = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER = "https://archive-api.open-meteo.com/v1/archive"


def fetch(url, variables):
    query = urlencode({**COMMON, "hourly": ",".join(variables)})
    with urlopen(f"{url}?{query}", timeout=120) as r:
        hourly = json.load(r)["hourly"]
    return pd.DataFrame(hourly).set_index("time")


def download(path=CSV_PATH):
    air = fetch(AIR, ["pm2_5", "pm10", "nitrogen_dioxide"])
    weather = fetch(WEATHER, ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"])
    df = air.join(weather)
    df.index.name = "time"
    df.to_csv(path)
    return df


if __name__ == "__main__":
    df = download()
    print(f"Saved {len(df)} rows x {df.shape[1]} columns to {CSV_PATH}")
