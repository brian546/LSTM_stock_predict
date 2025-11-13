import yfinance as yf
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ================== INDICATORS ==================
def fetch_and_add_indicators(ticker, features, start, end):
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        print(f"No data for {ticker}")
        return None

    close = df['Close'].copy()

    # Force 1D Series (critical!)
    close = pd.Series(close.values.flatten(), index=close.index, name='Close')

    df['SMA10_diff'] = SMAIndicator(close, window=10).sma_indicator()
    df['SMA20_diff'] = SMAIndicator(close, window=20).sma_indicator()
    df['SMA50_diff'] = SMAIndicator(close, window=50).sma_indicator()
    df['SMA100_diff'] = SMAIndicator(close, window=100).sma_indicator()

    for diff in ['SMA50_diff','SMA20_diff','SMA10_diff','SMA100_diff']:
        df[diff] = (close - df[diff])/df[diff]

    df = df[features].astype('float32')
    return df


# ================== SEQUENCES ==================
def create_sequences(data, seq_len):
    X, y = [], []
    for i in range(seq_len, len(data)):
        X.append(data[i-seq_len:i])
        y.append(data[i, 0])  # Close

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

# Plot
def plot(ticker, df, preds, target_col, save_fig=True):
    """plot line plot and save it """
    dates = df.index
    actual_prices = df[target_col].values
    plt.figure(figsize=(12, 6))
    plt.plot(dates, actual_prices, label=f'Actual {target_col}', color='blue', linewidth=1, linestyle='--')
    plt.plot(dates, preds, label='LSTM Predicted', color='red', linewidth=1)
    plt.title(f'{ticker} - Test: {dates[0].strftime("%b %d, %Y")} to {dates[-1].strftime("%b %d, %Y")}', fontsize=16, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel(target_col)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=120))
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    if save_fig:
        plt.savefig(f"plots/{ticker}_{target_col}_test_plot.png", dpi=300, bbox_inches='tight')
    plt.show()