"""Download hourly Bishkek weather from Open-Meteo (free, no API key)."""
import json
import time
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd

URL = "https://archive-api.open-meteo.com/v1/archive"
PARAMS = {"latitude": 42.87, "longitude": 74.59, "start_date": "2023-01-01",
          "end_date": "2025-03-03", "timezone": "Asia/Bishkek",
          "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"}


def fetch_weather():
    for attempt in range(4):
        try:
            with urlopen(f"{URL}?{urlencode(PARAMS)}", timeout=120) as r:
                df = pd.DataFrame(json.load(r)["hourly"])
            break
        except OSError:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")


if __name__ == "__main__":
    print(fetch_weather().describe().round(1).T)
