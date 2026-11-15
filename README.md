# Air Quality in Bishkek

Exploratory analysis of PM2.5 air pollution in Bishkek, Kyrgyzstan: how bad it is, when it peaks, and how it relates to the weather.

## Data
- **PM2.5:** real measurements from the US Embassy Bishkek monitor (site `417BI1010001`), published by [AirNow](https://www.airnow.gov). One reading per day at 21:00 local time (743 days, 2023-01-01 to 2025-03-03; the station stopped reporting after that).
- **Weather:** temperature, humidity and wind at the same hour from the [Open-Meteo](https://open-meteo.com) archive.

I first tried Open-Meteo's modelled air quality data, but it averaged only 14-16 µg/m³ in winter and missed the local heating pollution the real monitor shows, so I switched to station measurements.

## Key findings
- Heavily skewed: mean 28.5 µg/m³, median 9.0, peak 401 (2024-12-23).
- Strong seasonality: January averages 87.7 µg/m³ vs roughly 7-11 in April-October.
- Heating season (Nov-Mar): 66% of evenings exceed the WHO 24-hour guideline (15 µg/m³), vs 25% in the rest of the year.
- 100 days above 55.4 µg/m³ (unhealthy), 14 above 225.4 (hazardous).
- Colder and calmer evenings are more polluted: correlation with temperature -0.47, with wind speed -0.24.

## Limitations
One evening reading per day (not a 24-hour average), a single station, and correlation is not causation.

## Project structure

```
data/        bishkek_pm25.csv
notebooks/   01_eda.ipynb
src/         air.py (AirNow), weather.py (Open-Meteo), data.py (build the CSV)
```

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.data        # rebuild the dataset (about 10 minutes)
jupyter notebook notebooks/
```

## Possible next steps
- Forecast next-day PM2.5 from today's weather
- Add more stations or full hourly data
