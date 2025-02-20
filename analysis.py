import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better visuals
sns.set_theme(style="darkgrid")

# Define API Endpoint
API_URL = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json&date=2000:2023"

# Indicators and world bank codes
indicators = {
    "Real GDP (Current US$)": "NY.GDP.MKTP.CD",
    "Real GDP Growth (%)": "NY.GDP.MKTP.KD.ZG",
    "GDP per Capita (US$)": "NY.GDP.PCAP.CD",
    "Inflation Rate (%)": "FP.CPI.TOTL.ZG",
    "Unemployment Rate (%)": "SL.UEM.TOTL.ZS",
    "Money Supply (M2)": "FM.LBL.BMNY.CN",  # Used for Money Velocity Calculation
    "National Savings (percent of GDP)": "NY.GNS.ICTR.ZS"
}

# Define countries as the codes on the world bank API
countries = ["BGD", "IND", "PAK", "USA"]  # We are analyzing the selected countries: Bangladesh, India, Pakistan, USA by default

# Allow user to select countries dynamically
user_input = input("Enter country codes separated by commas (default: BGD, IND, PAK, USA): ").strip().upper()

# Use default countries if input is empty
countries = [code.strip() for code in user_input.split(",")] if user_input else ["BGD", "IND", "PAK", "USA"]

# This function will fetch the data from the World Bank API
def fetch_data(country, indicator):
    url = API_URL.format(country, indicator)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if len(data) > 1 and "date" in data[1][0]:  # Ensure data format is correct
            return [(int(entry["date"]), entry["value"]) for entry in data[1] if entry["value"] is not None]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {country} - {indicator}: {e}")
    return []  # Return empty list if no data found

# Store fetched data
data_dict = {}

# Fetches data for every country using the indicators
for country in countries:
    data_dict[country] = {}
    for name, code in indicators.items():
        data_dict[country][name] = fetch_data(country, code)