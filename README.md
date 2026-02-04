# LSTM Stock Forecasting & Trading Simulation 🔧📈

A small research project that trains and uses LSTM models to predict the difference between a stock's price and its 50-day Simple Moving Average (SMA50). The repo also includes trading backtests that combine LSTM and Random Forest predictions with standard technical indicators to evaluate conservative and aggressive trading strategies.

---

## Features ✅

- LSTM model implementation for time-series forecasting (`model.py`).
- Inference pipeline to generate next-day SMA50-difference predictions (`inference.py`).
- Backtesting engine with two strategies: **Conservative** and **Aggressive** (`trading.py`).
- Utilities for fetching data and computing indicators (`utils.py`).
- Example notebooks for training and experiments (`train close.ipynb`, `train_sma50_diff.ipynb`).
- Pretrained models and example outputs in `models/`, `predictions/`, and `trading_results/`.

---

## Quickstart 🚀

1. Create environment and install dependencies:

```bash
conda create -n trading python=3.12 -y
conda activate trading
pip install torch yfinance pandas matplotlib ta scikit-learn ipykernel
```

2. Generate LSTM predictions for a ticker (example):

```bash
python inference.py --ticker 0005.HK --target_col SMA50_diff --start 2022-10-27 --end 2022-11-28
```

This writes a CSV to `predictions/{ticker}_predict.csv` and prints the test set with the predicted `next_day_SMA50_diff`.

3. Run a trading backtest using LSTM (and optional Random Forest predictions):

```bash
python trading.py --ticker 0005.HK --start 2022-10-01 --end 2022-12-01 --strategy both
```

Backtest summaries and trades are saved under `trading_results/`.


Run the full end-to-end pipeline (inference + trading) with a single command:

```bash
python run_pipeline.py --ticker 0005.HK --start 2022-10-01 --end 2022-12-01 --strategy both
```

This will:
- Run `inference.py` and save predictions to `predictions/{ticker}_predict.csv`.
- Run `trading.py` using the generated predictions and save results to `trading_results/{ticker}_{strategy}/`.

Useful options:
- `--no_inference` — skip inference (use an existing prediction CSV instead).
- `--no_trading` — run only inference (skip backtest).
- `--rf_path <path>` — provide a Random Forest CSV to include RF predictions in the backtest.


---

## Repository Structure 🗂️

- `inference.py` - Generate next-day SMA50-diff predictions using saved LSTM checkpoints.
- `model.py` - LSTM model definition (PyTorch).
- `trading.py` - Backtester with Conservative and Aggressive strategies that combine technicals + ML predictions.
- `utils.py` - Data fetching, indicator calculation and helper functions (sequence creation, plotting).
- `models/` - Pretrained model checkpoints (`{ticker}_lstm_{target}.pth`).
- `predictions/` - CSV outputs from `inference.py`.
- `trading_results/` - Backtest outputs, portfolios, and trades.
- `random_forest/` - Example RF prediction CSVs used by `trading.py`.
- `plots/` - Generated charts for predictions.
- `*.ipynb` - Notebooks used to train and explore the LSTM models.

---

## Implementation Details 🔧

- The LSTM predicts the difference between the price and moving averages (SMA50 diff). `utils.fetch_and_add_indicators` prepares SMAs and normalized features used for model input.
- `inference.py` loads a checkpoint containing `model_state_dict` and `scaler`, builds rolling windows, performs predictions, and inverse-transforms them to write into the test DataFrame.
- `trading.py` computes standard indicators (SMA, MACD, RSI, Bollinger Bands), merges ML predictions, and simulates buy/sell rules with configurable risk (position size, stop loss, trailing stops).

---

## Tips & Notes 💡

- Pretrained checkpoints are placed in `models/` and named like `{ticker}_lstm_SMA50_diff.pth`.
- `inference.py` automatically chooses CUDA / MPS / CPU when available.
- Random Forest predictions (optional) can be provided as CSVs in `random_forest/` with a `Date` column and columns `Random Forest` and `Next Price`.
- Plots are saved to `plots/` and predictions to `predictions/`.

---

## Reproducibility / Training

Training is performed in the provided notebooks. Open `train close.ipynb` or `train_sma50_diff.ipynb` to follow the data preprocessing, sequence creation, model training loop, and evaluation plots.

---

## License & Contact

This repository is intended for educational and research purposes. Open an issue for questions or improvements.

---

Happy experimenting! 🎯
