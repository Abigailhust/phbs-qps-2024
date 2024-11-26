import sys
print(f"Current Python executable: {sys.executable}")
import pandas as pd
import requests
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fetch import fetch_data

# API configuration
API_KEY = "9a821ee9ee2f578569ab5788b184bd41"
SERIES_ID = 'CPILFESL'
FRED_API_URL = f'https://api.stlouisfed.org/fred/series/observations?series_id={SERIES_ID}&api_key={API_KEY}&file_type=json'

# Fetch data from API
df = fetch_data(FRED_API_URL)
df['date'] = pd.to_datetime(df['date'])
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df = df.dropna()  # Drop rows with NaN values
df.set_index('date', inplace=True)
df = df['value']

# Ensure output directory exists
output_dir = "data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save raw CPI data
df.to_csv(f"{output_dir}/CPI.csv")

# Resample to quarterly and calculate inflation rate
quarterly_df = df.resample('Q').mean()
quarterly_df = pd.DataFrame(quarterly_df)
quarterly_df['inflation_rate'] = quarterly_df['value'].pct_change()

# Save last four quarters' data
last_four_quarters = quarterly_df.tail(4)
last_four_quarters.to_csv(f"{output_dir}/Inflation_last_four_quarters.csv")

print("CPI data and inflation rates have been saved.")
