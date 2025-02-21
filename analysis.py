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
    "Money Supply (M2)": "FM.LBL.BMNY.CN",
    "National Savings (percent of GDP)": "NY.GNS.ICTR.ZS",
    "Imports of Goods and Services (% of GDP)": "NE.IMP.GNFS.ZS",
    "Exports of Goods and Services (% of GDP)": "NE.EXP.GNFS.ZS",
    "Net Exports (% of GDP)": "NE.RSB.GNFS.ZS",
    "Real Exchange Rate": "PX.REX.REER",
    "Investments (% of GDP)": "NE.GDI.TOTL.ZS",
    "Real Interest Rate (%)": "FR.INR.RINR"
}

# Define countries as the codes on the world bank API
countries = ["BGD", "IND", "PAK", "USA"]

# Allow user to select countries dynamically
user_input = input("Enter country codes separated by commas (default: BGD, IND, PAK, USA): ").strip().upper()
countries = [code.strip() for code in user_input.split(",")] if user_input else ["BGD", "IND", "PAK", "USA"]

# Function to fetch data from the World Bank API
def fetch_data(country, indicator):
    url = API_URL.format(country, indicator)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if len(data) > 1 and "date" in data[1][0]:
            return [(int(entry["date"]), entry["value"]) for entry in data[1] if entry["value"] is not None]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {country} - {indicator}: {e}")
    return []

# Store fetched data
data_dict = {}
for country in countries:
    data_dict[country] = {}
    for name, code in indicators.items():
        data_dict[country][name] = fetch_data(country, code)

# Function to create DataFrame for an indicator
def create_dataframe(country, indicator_name):
    data = data_dict[country][indicator_name]
    if data:
        df = pd.DataFrame(data, columns=["Year", indicator_name])
        df = df[df["Year"].between(2000, 2023)]
        return df
    return pd.DataFrame()

# Function to calculate Money Velocity
def calculate_money_velocity(country):
    money_supply = create_dataframe(country, "Money Supply (M2)")
    gdp = create_dataframe(country, "Real GDP (Current US$)")
    if gdp.empty or money_supply.empty:
        print(f"Insufficient data for {country} to calculate Money Velocity.")
        return pd.DataFrame()
    df = pd.merge(gdp, money_supply, on="Year", how="inner")
    df["Money Velocity"] = df["Real GDP (Current US$)"] / df["Money Supply (M2)"]
    return df[["Year", "Money Velocity"]]

# Add Money Velocity to data dictionary
for country in countries:
    money_velocity_df = calculate_money_velocity(country)
    if not money_velocity_df.empty:
        data_dict[country]["Money Velocity"] = list(money_velocity_df.itertuples(index=False, name=None))

# Function to plot indicator
def plot_indicator(indicator_name):
    plt.figure(figsize=(10, 5))
    for country in countries:
        df = create_dataframe(country, indicator_name)
        if not df.empty:
            plt.plot(df["Year"], df[indicator_name], marker="o", label=country)
    plt.xlabel("Year")
    plt.ylabel(indicator_name)
    plt.title(f"{indicator_name} Over the Years")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# User interface for selecting which graph to display
while True:
    print("\nAvailable indicators:")
    for key in indicators.keys():
        print(f"- {key}")
    print("- Money Velocity")
    print("Type 'exit' to quit.")
    
    selected_indicator = input("Enter the indicator name to plot: ").strip()
    if selected_indicator.lower() == "exit":
        break
    elif selected_indicator in indicators or selected_indicator == "Money Velocity":
        plot_indicator(selected_indicator)
    else:
        print("Invalid selection. Please choose a valid indicator.")