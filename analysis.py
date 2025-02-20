import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better visuals
sns.set_theme(style="darkgrid")

# Define API Endpoint
API_URL = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json&date=2000:2023"

# Indicators and world bank codes
Indicators = {
    "Real GDP (Current US$)": "NY.GDP.MKTP.CD",
    "Real GDP Growth (%)": "NY.GDP.MKTP.KD.ZG",
    "GDP per Capita (US$)": "NY.GDP.PCAP.CD",
    "Inflation Rate (%)": "FP.CPI.TOTL.ZG",
    "Unemployment Rate (%)": "SL.UEM.TOTL.ZS",
    "Money Supply (M2)": "FM.LBL.BMNY.CN",  # Used for Money Velocity Calculation
    "National Savings (% of GDP)": "NY.GNS.ICTR.ZS"
}
