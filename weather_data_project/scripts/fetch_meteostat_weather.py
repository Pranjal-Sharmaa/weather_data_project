# scripts/fetch_meteostat_weather.py

from meteostat import Hourly, Stations
from datetime import datetime, timedelta
import pandas as pd
import os

# 📍 Jaipur coordinates
latitude, longitude = 26.9124, 75.7873

# ⏳ Dynamically get today & 2 years ago
end = datetime.now()
start = end - timedelta(days=2*365)

# 🔍 Find nearest weather station to Jaipur
stations = Stations()
stations = stations.nearby(latitude, longitude)
station = stations.fetch(1)
station_id = station.index[0]

print(f"📡 Using station: {station_id} near Jaipur")
print(f"📅 Fetching data from {start.date()} to {end.date()}")

# 🕒 Fetch hourly data
data = Hourly(station_id, start, end)
df = data.fetch()

# 💾 Save to CSV
output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'jaipur_weather_last_2_years.csv')
df.to_csv(output_file)

print(f"\n✅ Data saved to: {output_file}")
print(df.head())
