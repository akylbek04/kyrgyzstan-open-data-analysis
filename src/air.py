"""Download real PM2.5 measurements for the US Embassy Bishkek monitor from AirNow.

AirNow publishes one global file per hour (~0.7 MB). To keep the download small we take ONE file per day:
15:00 UTC = 21:00 Bishkek time, which falls in the evening heating-season peak.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from urllib.request import urlopen

import pandas as pd

SITE = "417BI1010001"
URL = "https://files.airnowtech.org/airnow/{d:%Y}/{d:%Y%m%d}/HourlyData_{d:%Y%m%d}15.dat"
START, END = date(2023, 1, 1), date(2025, 12, 31)


def fetch_day(d):
    """Return (date, pm25) or None when the file or the reading is missing."""
    try:
        with urlopen(URL.format(d=d), timeout=60) as r:
            for line in r.read().decode("latin1").splitlines():
                f = line.split("|")
                if f[2] == SITE and f[5] == "PM2.5":
                    return d, float(f[7])
    except Exception:
        pass
    return None


def fetch_air():
    days = [START + timedelta(n) for n in range((END - START).days + 1)]
    with ThreadPoolExecutor(8) as pool:
        rows = [r for r in pool.map(fetch_day, days) if r]
    df = pd.DataFrame(rows, columns=["date", "pm25"]).set_index("date")
    return df[df["pm25"] >= 0]  # AirNow uses -999 for invalid readings


if __name__ == "__main__":
    df = fetch_air()
    print(len(df), "days with a reading")
    print(df.describe().round(1).T)
