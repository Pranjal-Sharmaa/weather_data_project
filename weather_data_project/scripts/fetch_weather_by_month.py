import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('VISUAL_CROSSING_API_KEY')

# Output path
output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'jaipur_weather_hourly_2years.csv')

# Config
location = "Jaipur"
unit = "metric"
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# Collect all results in a list
all_data = []

# Step through month by month
current = start_date
while current <= end_date:
    # Define monthly range
    month_start = current
    next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
    month_end = min(end_date, next_month - timedelta(days=1))

    print(f"📆 Fetching {month_start.date()} to {month_end.date()}...")

    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{location}/{month_start.date()}/{month_end.date()}?unitGroup={unit}&include=hours&key={API_KEY}&contentType=json"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()

        # Extract hours
        for day in json_data.get("days", []):
            for hour in day.get("hours", []):
                hour["date"] = day["datetime"]
                all_data.append(hour)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {month_start.date()} - {e}")

    # Move to next month
    current = next_month

# Save combined data to CSV
df = pd.DataFrame(all_data)
df.to_csv(output_file, index=False)
print(f"\n✅ All data saved to: {output_file}")
print(df.head())
