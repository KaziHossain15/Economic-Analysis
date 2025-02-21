# Economic Data Analysis using World Bank API

## Overview
This project is a data visualization tool that analyzes and compares economic indicators for multiple countries using the **World Bank API**. Users can dynamically select countries and indicators to visualize trends in GDP, inflation, unemployment, money velocity, and more.

## Features
- **Fetch economic data** from the World Bank API for selected countries.
- **Calculate Money Velocity** using real GDP and M2 money supply.
- **Interactive user interface** to select and display economic indicators.
- **Visualize data** with graphs using Matplotlib and Seaborn.

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-username/economic-analysis.git
   cd economic-analysis
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
   python main.py
   ```
2. **Follow on-screen instructions** to select countries and indicators to visualize.
3. **View graphs** displaying economic trends.

## Indicators Available
- Real GDP (Current US$)
- Real GDP Growth (%)
- GDP per Capita (US$)
- Inflation Rate (%)
- Unemployment Rate (%)
- Money Velocity
- Imports
- Exports
- Net Exports
- Real Exchange Rates
- Investments
- Real Interest Rates

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
