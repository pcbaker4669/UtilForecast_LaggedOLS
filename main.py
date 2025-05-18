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
FRED_API_KEY = "YOUR_FRED_API_KEY_HERE"
POLYGON_API_KEY = "YOUR_POLYGON_API_KEY_HERE"

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
def run_regression(data):
    X = data[['delta_yield', 'cpi', 'natgas']]
    X = sm.add_constant(X)
    y = data['weekly_return']

    model = sm.OLS(y, X).fit()
    print(model.summary())
    return model

# === VARIABLE LAG SWEEP ===
def variable_lag_sweep(macro_df, stock_df, max_lag=12):
    results = []
    variables = ['cpi', '10yr_yield', 'natgas']
    for var in variables:
        for lag in range(max_lag + 1):
            lagged_macro = macro_df.copy()
            lagged_macro[var] = lagged_macro[var].shift(lag)
            lagged_macro['delta_yield'] = lagged_macro['10yr_yield'].diff()

            merged = pd.concat([stock_df, lagged_macro], axis=1).dropna()
            if len(merged) < 30:
                continue

            X = merged[['delta_yield', 'cpi', 'natgas']]
            X = sm.add_constant(X)
            y = merged['weekly_return']

            model = sm.OLS(y, X).fit()

            results.append({
                'variable': var,
                'lag': lag,
                'r_squared': round(model.rsquared, 4),
                'adj_r_squared': round(model.rsquared_adj, 4),
                'p_delta_yield': round(model.pvalues.get('delta_yield', np.nan), 4),
                'p_cpi': round(model.pvalues.get('cpi', np.nan), 4),
                'p_natgas': round(model.pvalues.get('natgas', np.nan), 4)
            })

    result_df = pd.DataFrame(results)
    result_df.to_csv("independent_lag_sweep.csv", index=False)
    print("Saved independent lag sweep results to independent_lag_sweep.csv")
    return result_df

# === PLOT LAG SWEEP RESULTS ===
def plot_variable_lag_sweep(df):
    plt.figure(figsize=(10, 6))
    for var in df['variable'].unique():
        subset = df[df['variable'] == var]
        plt.plot(subset['lag'], subset['adj_r_squared'], label=f"{var} lag sweep")
    plt.xlabel("Lag (Weeks)")
    plt.ylabel("Adjusted R²")
    plt.title("Adjusted R² by Lag for Individual Variables")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("independent_lag_sweep.png")
    plt.show()

def save_lag_sweep_summary(result_df, filename="independent_lag_sweep_summary.txt"):
    with open(filename, "w") as f:
        for var in result_df['variable'].unique():
            f.write(f"\n=== Lag Sweep Summary for {var.upper()} ===\n")
            df_var = result_df[result_df['variable'] == var]
            for _, row in df_var.iterrows():
                f.write(
                    f"Lag {int(row['lag'])}: adj_R²={row['adj_r_squared']:.3f}, "
                    f"p_delta_yield={row['p_delta_yield']:.3f}, "
                    f"p_cpi={row['p_cpi']:.3f}, "
                    f"p_natgas={row['p_natgas']:.3f}\n"
                )
    print(f"Saved lag sweep summary to {filename}")

if __name__ == "__main__":
    macro = get_macro_data()
    stock = get_stock_returns()
    full_data = align_and_lag_data(macro, stock, LAG_WEEKS)
    print("Final sample size:", len(full_data))
    model = run_regression(full_data)

    # Run independent variable lag sweep
    indep_results = variable_lag_sweep(macro, stock, max_lag=12)
    plot_variable_lag_sweep(indep_results)
    save_lag_sweep_summary(indep_results)
