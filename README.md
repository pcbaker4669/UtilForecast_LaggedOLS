# UtilForecast_LaggedOLS
[![DOI](https://zenodo.org/badge/985492220.svg)](https://doi.org/10.5281/zenodo.15460078)

**Exploratory Regression Framework for Lag-Sensitive Forecasting of U.S. Utility Stocks**

This repository supports an academic investigation into how macroeconomic indicators, when lagged appropriately, can explain short-term movements in regulated utility stocks. Using Duke Energy (DUK) as a representative case, the model performs a systematic lag sweep across multiple macroeconomic signals to identify optimal lead-lag relationships.

---

## Project Overview

Utility companies are sensitive to broader macroeconomic forces due to their capital-intensive and regulated nature. This project asks:

**"How much predictive value do macroeconomic variables like interest rates, CPI, and natural gas prices hold when used with different time lags?"**

This code:
- Collects and processes weekly data for:
  - Consumer Price Index (CPI)
  - 10-Year Treasury Yield
  - Henry Hub Natural Gas Price
- Computes weekly returns for Duke Energy (DUK)
- Runs a **lag sweep** from 0 to 12 weeks for each variable independently
- Evaluates **Adjusted R²** and **p-values** to assess statistical significance
- Outputs structured tables and plots for analysis

---

## Repository Contents

```
.
├── main.py                          # Main script to run lag sweep and regression
├── macro_data_lagged.csv           # Weekly CPI, Treasury, NatGas (FRED)
├── stock_returns_lagged.csv        # Weekly returns for DUK (Polygon.io)
├── independent_lag_sweep.csv       # Output table of lag sweep results
├── independent_lag_sweep.png       # Plot of Adjusted R² vs lag
├── regression_summary.txt          # Baseline regression output (screen + file)
├── README.md                       # This file
```

---

## Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/pcbaker4669/UtilForecast_LaggedOLS.git
cd UtilForecast_LaggedOLS
```

2. **Install dependencies:**

```bash
pip install pandas numpy matplotlib seaborn statsmodels requests fredapi
```

3. **Set your API keys:**

You can either:
- Add them directly in `main.py`, or
- Use environment variables (recommended for security)

```python
FRED_API_KEY = "your_fred_api_key"
POLYGON_API_KEY = "your_polygon_api_key"
```

4. **Run the model:**

```bash
python main.py
```

This will:
- Fetch or load data
- Perform the lag sweep analysis
- Save output to `.csv` and `.png`

---

## Output Files

- `independent_lag_sweep.csv`: Contains one row per lag per variable with:
  - Adjusted R²
  - R²
  - p-values for delta_yield, CPI, and NatGas

- `independent_lag_sweep.png`: Visualization showing lag effectiveness for each variable.

- `regression_summary.txt`: Console-formatted OLS summary output for the default lag setup.

---

## Research Context

This repository supports a working paper titled:  
**"Lagged Macroeconomic Signal Forecasting for U.S. Utility Stocks: A Linear Regression Sweep Approach"**

The findings help build a foundation for more advanced forecasting approaches such as:
- Agent-based market simulations
- Regime-switching models
- Time-varying coefficient models

The best-lag model built from these results is continued in:  
[UtilitiesBestLagPredictor](https://github.com/pcbaker4669/UtilitiesBestLagPredictor)

---

## Citation

If you use this repository or reproduce any results, please cite:

> Baker, Peter. *UtilForecast_LaggedOLS: An Exploratory Framework for Lag-Sensitive Forecasting of Regulated Utility Stocks*. Zenodo. DOI: [10.5281/zenodo.15453469](https://doi.org/10.5281/zenodo.15453469)

[![DOI](https://zenodo.org/badge/981723841.svg)](https://doi.org/10.5281/zenodo.15453469)

---

## Contact

**Peter C. Baker**  
PhD Student, Computational Social Science  
George Mason University  
📧 pcbaker1969@gmail.com  
🔗 [github.com/pcbaker4669](https://github.com/pcbaker4669)

---
