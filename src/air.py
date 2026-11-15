"""Download real PM2.5 measurements for the US Embassy Bishkek monitor from AirNow.

AirNow publishes one global file per hour (~0.7 MB). To keep the download small we take ONE file per day:
15:00 UTC = 21:00 Bishkek time, which falls in the evening heating-season peak.
"""
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from urllib.error import HTTPError
from urllib.request import urlopen

import pandas as pd

SITE = "417BI1010001"
URL = "https://files.airnowtech.org/airnow/{d:%Y}/{d:%Y%m%d}/HourlyData_{d:%Y%m%d}15.dat"
START, END = date(2023, 1, 1), date(2025, 12, 31)


def fetch_day(d, retries=4):
    """Return (date, pm25), or None when the file or the reading does not exist.

    Network errors are retried; a 404 means AirNow has no file for that hour, so we skip it.
    """
    for attempt in range(retries):
        try:
            with urlopen(URL.format(d=d), timeout=60) as r:
                for line in r.read().decode("latin1").splitlines():
                    f = line.split("|")
                    if f[2] == SITE and f[5] == "PM2.5":
                        return d, float(f[7])
            return None
        except HTTPError as e:
            if e.code == 404:
                return None
        except OSError:
            pass
        time.sleep(2 ** attempt)
    raise ConnectionError(d)


def _safe(d):
    try:
        return fetch_day(d)
    except ConnectionError:
        return "failed", d


def fetch_air():
    days = [START + timedelta(n) for n in range((END - START).days + 1)]
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(_safe, days))
    # second pass: retry the failed days one at a time, then give up loudly
    rows = [r for r in results if r and r[0] != "failed"]
    for r in results:
        if r and r[0] == "failed":
            res = fetch_day(r[1], retries=6)
            if res:
                rows.append(res)
    df = pd.DataFrame(rows, columns=["date", "pm25"]).set_index("date").sort_index()
    return df[df["pm25"] >= 0]  # AirNow uses -999 for invalid readings


if __name__ == "__main__":
    df = fetch_air()
    print(len(df), "days with a reading")
    print(df.describe().round(1).T)
