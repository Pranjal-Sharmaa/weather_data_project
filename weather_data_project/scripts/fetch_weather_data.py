# scripts/fetch_weather_data.py

import requests
import os
from dotenv import load_dotenv
import pandas as pd

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('VISUAL_CROSSING_API_KEY')
print(f"🔑 Loaded API Key: {API_KEY}")


# Settings
location = "Jaipur"
start_date = "2023-01-01"
end_date = "2024-12-31"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# CSV output path
output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "jaipur_weather_hourly_2years.csv")

# Construct request URL
url = f"{base_url}/{location}/{start_date}/{end_date}?unitGroup=metric&include=hours&key={API_KEY}&contentType=csv"

print(f"\n📡 Fetching data from: {url}")

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise error if failed

    with open(output_file, 'wb') as f:
        f.write(response.content)
        print(f"\n✅ Data saved to: {output_file}")

    # Load preview
    df = pd.read_csv(output_file)
    print("\n📊 Sample data:")
    print(df.head())

except requests.exceptions.HTTPError as err:
    print(f"\n❌ HTTP error occurred: {err}")
except Exception as e:
    print(f"\n❌ Other error occurred: {e}")
