# UtilForecast_LaggedOLS
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15511239.svg)](https://doi.org/10.5281/zenodo.15511239)

**Exploratory Regression Framework for Lag-Sensitive Forecasting of U.S. Utility Stocks**

This repository supports an academic investigation into how macroeconomic indicators, when lagged appropriately, can explain short-term movements in regulated utility stocks. Using Duke Energy (DUK) as a representative case, the model performs a systematic lag sweep across multiple macroeconomic signals to identify optimal lead-lag relationships.

---

## Project Overview

This codebase builds a forecasting model for weekly utility stock returns using lagged macroeconomic signals. After conducting a systematic lag sweep across CPI, interest rates, and natural gas prices, it applies the best lags directly within the same script to generate a final regression model. No external scripts are required — the full analysis is reproducible from a single run.

---

## Repository Contents

```
.
├── main.py                          # Unified script for lag sweep + final model
├── macro_data_lagged.csv           # Weekly CPI, Treasury, NatGas (FRED)
├── stock_returns_lagged.csv        # Weekly returns for DUK (Polygon.io)
├── independent_lag_sweep.csv       # Output table of lag sweep results
├── Figure1_AdjustedR2_LagSweep.png # Final R² plot
├── regression_summary.txt          # Baseline regression output (lag=2)
├── final_best_lag_model_summary.txt # Final model using best lags from sweep
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

- `independent_lag_sweep.csv`: One row per lag per variable with adjusted R² and p-values.
- `Figure1_AdjustedR2_LagSweep.png`: Visualization showing adjusted R² across lags.
- `regression_summary.txt`: Baseline model using fixed 2-week lag for all variables.
- `final_best_lag_model_summary.txt`: OLS output using optimal lags (CPI=0, Yield=2, NatGas=0).

---

## Research Context

This repository supports a working paper titled:  
**"Lagged Macroeconomic Signal Forecasting for U.S. Utility Stocks: A Linear Regression Sweep Approach"**

The findings help build a foundation for more advanced forecasting approaches such as:
- Agent-based market simulations
- Regime-switching models
- Time-varying coefficient models

The best-lag model is now integrated directly into `main.py` and runs automatically at the end of the script.

---

## Citation

If you use this repository or reproduce any results, please cite:

> Baker, Peter. *UtilForecast_LaggedOLS: An Exploratory Framework for Lag-Sensitive Forecasting of Regulated Utility Stocks*. Zenodo. https://doi.org/10.5281/zenodo.15511239

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15511239.svg)](https://doi.org/10.5281/zenodo.15511239)

---

## Contact

**Peter C. Baker**  
PhD Student, Computational Social Science  
George Mason University  
📧 pcbaker1969@gmail.com  
🔗 [github.com/pcbaker4669](https://github.com/pcbaker4669)

---
