# Economic Data Analysis using World Bank API

## Overview

This project is a **data visualization tool** that analyzes and compares economic indicators for multiple countries using the **World Bank API**. Users can dynamically select countries and indicators, retrieve data, and visualize trends in GDP, inflation, unemployment, money velocity, and more.

## Features

- **Dynamic country selection:** Users can input country codes to customize their analysis.
- **Fetch economic data** from the World Bank API for multiple countries.
- **Calculate Money Velocity** using real GDP and M2 money supply.
- **Data filtering:** Filters out missing values to improve accuracy.
- **Visualize trends** with Matplotlib and Seaborn.
- **Interactive user interface:** Choose which economic indicators to plot.

## Installation

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/KaziHossain15/Economic-analysis.git
   cd Economic-analysis
   ```

2. **Create a Virtual Environment (Optional but Recommended):**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the script:**
   ```sh
   python analysis.py
   ```
2. **Enter country codes** (e.g., `BGD, IND, USA, PAK`) or press Enter to use default values.
3. **Select an economic indicator** from the available list.
4. **View graphs** displaying economic trends over time.
5. **Repeat selection** or type 'exit' to quit the program.

## Indicators Available

- **Macroeconomic Indicators**

  - Real GDP (Current US$)
  - Real GDP Growth (%)
  - GDP per Capita (US$)
  - Inflation Rate (%)
  - Unemployment Rate (%)

- **Trade & Financial Indicators**

  - Money Supply (M2)
  - Imports of Goods and Services (% of GDP)
  - Exports of Goods and Services (% of GDP)
  - Net Exports (% of GDP)
  - Real Exchange Rate

- **Investment & Fiscal Indicators**

  - Investments (% of GDP)
  - Real Interest Rate (%)
  - Government Spending (% of GDP)
  - Tax Revenue (% of GDP)

- **Derived Indicator:**

  - Money Velocity (calculated using GDP and M2)

## Dependencies

- Python 3.x
- `requests`
- `pandas`
- `matplotlib`
- `seaborn`

## Contributing

Feel free to open issues or submit pull requests to improve the project!

## Author

**Kazi Hossain**