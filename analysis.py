import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

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
    "Real Interest Rate (%)": "FR.INR.RINR",
    "Government Spending (% of GDP)": "NE.CON.GOVT.ZS",
    "Tax Revenue (% of GDP)": "GC.TAX.TOTL.GD.ZS"
}

# Define countries as the codes on the World Bank API
countries = ["BGD", "IND", "PAK", "USA"]

# Allow user to select countries dynamically
user_input = input("Enter country codes separated by commas (default: BGD, IND, PAK, USA): ").strip().upper()
countries = [code.strip() for code in user_input.split(",")] if user_input else ["BGD", "IND", "PAK", "USA"]

# Function to fetch data from the World Bank API
def fetch_data(country, indicator):
    url = API_URL.format(country, indicator)
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if len(data) > 1 and "date" in data[1][0]:
                return [(int(entry["date"]), entry["value"]) for entry in data[1] if entry["value"] is not None]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {country} - {indicator}: {e}. Retrying...")
    print(f"Failed to fetch data for {country} - {indicator} after multiple attempts.")
    return []

# Store fetched data
data_dict = {}
for country in countries:
    data_dict[country] = {}
    for name, code in indicators.items():
        data_dict[country][name] = fetch_data(country, code)

# Function to create DataFrame for an indicator
def create_dataframe(country, indicator_name):
    data = data_dict[country].get(indicator_name, [])
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
        return []
    df = pd.merge(gdp, money_supply, on="Year", how="inner")
    df["Money Velocity"] = df["Real GDP (Current US$)"] / df["Money Supply (M2)"]
    return [(row["Year"], row["Money Velocity"]) for _, row in df.iterrows()]

# Add Money Velocity to data dictionary
for country in countries:
    data_dict[country]["Money Velocity"] = calculate_money_velocity(country)

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

# Function to generate a heatmap of all indicators and top correlations
def plot_correlation_heatmap():
    combined_data = []
    for country in countries:
        country_data = pd.DataFrame()
        for indicator in indicators.keys():
            df = create_dataframe(country, indicator)
            if not df.empty:
                df.set_index("Year", inplace=True)
                country_data = pd.concat([country_data, df], axis=1)
        if not country_data.empty:
            combined_data.append(country_data)
    
    if combined_data:
        final_df = pd.concat(combined_data, axis=0).dropna()
        correlation_matrix = final_df.corr()
        
        # Plot heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap of Economic Indicators")
        plt.show()
        
        # Find top correlated indicator pairs
        correlation_pairs = correlation_matrix.unstack().reset_index()
        correlation_pairs.columns = ["Indicator 1", "Indicator 2", "Correlation"]
        correlation_pairs = correlation_pairs[correlation_pairs["Indicator 1"] != correlation_pairs["Indicator 2"]]
        correlation_pairs["Correlation"] = correlation_pairs["Correlation"].abs()
        top_correlations = correlation_pairs.sort_values(by="Correlation", ascending=False).head(10)
        
        # Save top correlations to a file
        top_correlations.to_csv("top_correlations.txt", index=False, sep="\t")
        print("Top correlations saved to 'top_correlations.txt'")
    else:
        print("Not enough data available for correlation analysis.")

# User Interface to Choose Graph Type
while True:
    print("\nChoose an option:")
    print("1 - Plot an indicator over the years")
    print("2 - Generate correlation heatmap and top correlations")
    print("3 - Exit")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        print("\nAvailable Indicators:")
        for i, indicator in enumerate(indicators.keys(), 1):
            print(f"{i}. {indicator}")
        
        indicator_choice = input("Enter the indicator name exactly as shown above: ").strip()
        
        if indicator_choice in indicators.keys() or indicator_choice == "Money Velocity":
            plot_indicator(indicator_choice)
        else:
            print("Invalid indicator name. Please try again.")
    elif choice == "2":
        plot_correlation_heatmap()
    elif choice == "3":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
