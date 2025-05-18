# UtilForecast_LaggedOLS
# A macroeconomic-lag-aware forecasting model for U.S. utility stock returns

import pandas as pd
import numpy as np
import requests
from fredapi import Fred
import statsmodels.api as sm
import os
import matplotlib.pyplot as plt
import seaborn as sns

# === API KEYS ===
FRED_API_KEY = ""
POLYGON_API_KEY = ""

# === USER CONFIG ===
STOCK_SYMBOL = "DUK"  # Duke Energy as the representative utility stock
START_DATE = "2020-05-01"
END_DATE = "2025-05-01"
LAG_WEEKS = 2  # Number of weeks to lag macro variables

# === DATASET FILE NAMES ===
MACRO_CSV = "macro_data_lagged.csv"
STOCK_CSV = "stock_returns_lagged.csv"

# === GET MACRO DATA ===
def get_macro_data():
    fred = Fred(api_key=FRED_API_KEY)

    if os.path.exists(MACRO_CSV):
        df = pd.read_csv(MACRO_CSV, index_col=0, parse_dates=True)
        print("Loaded macro data from file.")
    else:
        print("Fetching macro data from FRED...")
        cpi = fred.get_series("CPIAUCSL", observation_start=START_DATE, observation_end=END_DATE)
        treasury = fred.get_series("DGS10", observation_start=START_DATE, observation_end=END_DATE)
        natgas = fred.get_series("DHHNGSP", observation_start=START_DATE, observation_end=END_DATE)

        df = pd.concat([cpi, treasury, natgas], axis=1)
        df.columns = ["cpi", "10yr_yield", "natgas"]
        df = df.resample("W").mean()
        df.to_csv(MACRO_CSV)

    return df

# === GET STOCK RETURNS ===
def get_stock_returns():
    if os.path.exists(STOCK_CSV):
        df = pd.read_csv(STOCK_CSV, index_col=0, parse_dates=True)
        print("Loaded stock returns from file.")
    else:
        print("Fetching stock price data from Polygon.io...")
        url = f"https://api.polygon.io/v2/aggs/ticker/{STOCK_SYMBOL}/range/1/day/{START_DATE}/{END_DATE}"
        params = {"adjusted": "true", "sort": "asc", "apiKey": POLYGON_API_KEY}
        response = requests.get(url, params=params).json()

        prices = pd.DataFrame(response['results'])
        prices['t'] = pd.to_datetime(prices['t'], unit='ms')
        prices.set_index('t', inplace=True)
        df = prices['c'].resample('W').last().pct_change().dropna()
        df.name = "weekly_return"
        df.to_csv(STOCK_CSV)

    return df

# === ALIGN AND LAG DATA ===
def align_and_lag_data(macro_df, stock_df, lag_weeks):
    lagged_macro = macro_df.shift(lag_weeks)
    merged = pd.concat([stock_df, lagged_macro], axis=1).dropna()
    merged['delta_yield'] = merged['10yr_yield'].diff()
    return merged.dropna()

# === REGRESSION ===
def run_regression(data, output_file="regression_summary.txt"):
    X = data[['delta_yield', 'cpi', 'natgas']]
    X = sm.add_constant(X)
    y = data['weekly_return']

    model = sm.OLS(y, X).fit()

    # Save summary to file
    with open(output_file, "w") as f:
        f.write(model.summary().as_text())

    print("Regression results saved to", output_file)
    return model

if __name__ == "__main__":
    macro = get_macro_data()
    stock = get_stock_returns()
    full_data = align_and_lag_data(macro, stock, LAG_WEEKS)

    print("Final sample size:", len(full_data))

    # Round and save
    full_data_rounded = full_data.round(5)
    full_data_rounded.to_csv("regression_input_data.csv")
    print("Regression input data saved to regression_input_data.csv (rounded to 5 decimals)")

    # Run and save regression
    model = run_regression(full_data, output_file="regression_summary.txt")