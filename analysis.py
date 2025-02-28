import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Set Seaborn style for better visuals
sns.set_theme(style="darkgrid")

# Define API Endpoint
API_URL = "https://api.worldbank.org/v2/country/{}/indicator/{}?format=json&date=2000:2023&per_page=1000"

# Indicators and World Bank codes
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
    "Real Interest Rate (%)": "FR.INR.RINR",
    "Government Spending (% of GDP)": "NE.CON.GOVT.ZS",
    "Tax Revenue (% of GDP)": "GC.TAX.TOTL.GD.ZS"
}

# Default countries
default_countries = ["BGD", "IND", "PAK", "USA"]

# Allow user to select countries dynamically
user_input = input("Enter country codes separated by commas (default: BGD, IND, PAK, USA): ").strip().upper()
countries = [code.strip() for code in user_input.split(",")] if user_input else default_countries

# Function to fetch data from the World Bank API with error handling and retries
def fetch_data(country_list, indicator):
    url = API_URL.format(";".join(country_list), indicator)
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) > 1:
                return {
                    entry["country"]["id"]: [(int(entry["date"]), entry["value"]) for entry in data[1] if entry["value"] is not None]
                    for entry in data[1]
                }
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {indicator}: {e}. Retrying {2 - attempt} more times...")
            time.sleep(2)  # Wait before retrying
    return {}

# Store fetched data
data_dict = {country: {} for country in countries}
for name, code in indicators.items():
    fetched_data = fetch_data(countries, code)
    for country in countries:
        data_dict[country][name] = fetched_data.get(country, [])

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
        return pd.DataFrame()
    df = pd.merge(gdp, money_supply, on="Year", how="inner")
    df["Money Velocity"] = df["Real GDP (Current US$)"] / df["Money Supply (M2)"]
    return df[["Year", "Money Velocity"]]

# Add Money Velocity to data dictionary
for country in countries:
    money_velocity_df = calculate_money_velocity(country)
    if not money_velocity_df.empty:
        data_dict[country]["Money Velocity"] = list(money_velocity_df.itertuples(index=False, name=None))

# Function to plot indicator with save option
def plot_indicator(indicator_name, save=False):
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
    if save:
        plt.savefig(f"{indicator_name.replace(' ', '_')}.png")
        print(f"Saved as {indicator_name.replace(' ', '_')}.png")
    plt.show()

# Function to save data to CSV
def save_data_to_csv():
    for country in countries:
        df_list = []
        for name in indicators.keys():
            df = create_dataframe(country, name)
            if not df.empty:
                df_list.append(df.set_index("Year"))
        if df_list:
            final_df = pd.concat(df_list, axis=1).reset_index()
            final_df.to_csv(f"{country}_economic_data.csv", index=False)
            print(f"Saved {country}_economic_data.csv")

# User interface for selecting actions
while True:
    print("\nAvailable actions:")
    print("1. View available indicators")
    print("2. Plot an indicator")
    print("3. Save plots as images")
    print("4. Export data to CSV")
    print("5. Exit")
    choice = input("Select an option: ").strip()
    
    if choice == "1":
        print("\nAvailable indicators:")
        for key in indicators.keys():
            print(f"- {key}")
        print("- Money Velocity")
    elif choice == "2":
        selected_indicator = input("Enter the indicator name to plot: ").strip()
        if selected_indicator in indicators or selected_indicator == "Money Velocity":
            plot_indicator(selected_indicator)
        else:
            print("Invalid selection.")
    elif choice == "3":
        selected_indicator = input("Enter the indicator name to save: ").strip()
        if selected_indicator in indicators or selected_indicator == "Money Velocity":
            plot_indicator(selected_indicator, save=True)
        else:
            print("Invalid selection.")
    elif choice == "4":
        save_data_to_csv()
    elif choice == "5":
        break
    else:
        print("Invalid option. Try again.")
