import requests
import pandas as pd

def fetch_data(url):
    """
    Fetch data from the API endpoint
    """
    response = requests.get(url)
    if response.status_code!= 200:
        raise ValueError(f"Failed to fetch data from FRED API. HTTP Status: {response.status_code}")
    observations = response.json().get('observations', [])
    
    if not observations:
        raise ValueError("No observations found in the API response.")
    df = pd.DataFrame(observations)
    return df