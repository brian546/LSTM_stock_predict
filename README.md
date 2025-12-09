# LSTM MODEL FOR STOCK FORCASTING

This reponsitpry trains LSTM to predict difference between stock price and its simple 50-day moving average.

### Set Up Conda Environment
```bash
conda create -n trading python=3.12
pip install torch yfinance pandas matplotlib ta scikit-learn ipykernel openpyxl
```

### Load Environment
```bash
conda activate trading
```

### Calculate Best Portolio
```bash
conda activate trading
python find_best_sharpe.py --risk_free_rate 0.02  # 2% Risk Free Rate
python portfolio_optimizer.py --strategies 0288.HK:Aggressive 0005.HK:Conservative 2318.HK:Conservative --capital 20000 --weight_step 0.1 --top_n 15 --risk_free_rate 0.02
```