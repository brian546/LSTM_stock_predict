# Equal-Weight Benchmark Guide

## Overview

An equal-weight benchmark has been added to compare against the 2800.HK (Hang Seng Index ETF) benchmark. This benchmark invests equally in the same 5 stocks used in the trading strategies:

- **0002.HK** - CLP Holdings
- **0005.HK** - HSBC Holdings  
- **0288.HK** - WH Group
- **2318.HK** - Ping An Insurance
- **3690.HK** - Meituan

## Key Features

- **Equal allocation**: $20,000 per stock (20% each) = $100,000 total
- **50% position size**: Like the conservative strategy, only 50% of allocation is invested per stock
- **Buy and hold**: No active trading, just buy at start and hold
- **Diversification**: Spreads risk across 5 different stocks

## Usage

### Quick Start

Run the convenience script:
```bash
./run_equal_weight_benchmark.sh
```

This will:
1. Generate 2800.HK benchmark
2. Generate equal-weight 5-stock benchmark
3. Create comparison chart with both benchmarks

### Manual Usage

Create both benchmarks:
```bash
python benchmark.py \
  --ticker 2800.HK \
  --start 2022-10-27 \
  --end 2025-10-27 \
  --capital 100000 \
  --equal-weight 0002.HK 0005.HK 0288.HK 2318.HK 3690.HK \
  --compare 0002.HK 0005.HK 0288.HK 2318.HK 3690.HK
```

Generate aggregated comparison chart:
```bash
python compare_portfolio_aggregated.py \
  --benchmark 2800.HK \
  --tickers 0002.HK 0005.HK 0288.HK 2318.HK 3690.HK \
  --capital-per-stock 20000
```

## Output

### Benchmark Results

**2800.HK Benchmark**
Saved to `trading_results/2800.HK_benchmark/`:
- `portfolio_history.csv` - Daily portfolio values
- `summary.csv` - Performance summary

**Equal-Weight 5-Stock Benchmark**
Saved to `trading_results/equal_weight_benchmark/`:
- `portfolio_history.csv` - Daily portfolio values
- `summary.csv` - Performance summary

### Comparison Charts (2 Separate Charts)

The script now generates **two separate comparison charts**:

#### Chart 1: vs 2800.HK Benchmark
File: `trading_results/aggregated_portfolio_comparison_2800HK.png`

1. **Benchmark (2800.HK)** - Black line (thickest)
2. **Conservative Portfolio** - Blue line (medium)
3. **Aggressive Portfolio** - Red dashed line (medium)

#### Chart 2: vs Equal-Weight Benchmark
File: `trading_results/aggregated_portfolio_comparison_equal_weight.png`

1. **Equal-Weight Benchmark (5 stocks)** - Dark green line (thickest)
2. **Conservative Portfolio** - Blue line (medium)
3. **Aggressive Portfolio** - Red dashed line (medium)

### Statistics (2 Separate CSV Files)

#### Statistics 1: vs 2800.HK Benchmark
File: `trading_results/aggregated_portfolio_stats_2800HK.csv`

#### Statistics 2: vs Equal-Weight Benchmark
File: `trading_results/aggregated_portfolio_stats_equal_weight.csv`

Both include:
- Total return %
- Annualized return %
- Max drawdown %
- Standard deviation
- Sharpe ratio
- Volatility

## Comparison: 2800.HK vs Equal-Weight

### 2800.HK Benchmark
- Tracks overall Hang Seng Index performance
- Single ETF, simpler
- Lower risk (market-cap weighted)

### Equal-Weight 5-Stock Benchmark
- Equal exposure to each stock
- More diversified by company
- Higher risk (individual stock volatility)
- Better comparison for active strategies using the same stocks

## Example Output

```
Equal-Weight Portfolio Results:
--------------------------------------------------
Stocks:               0002.HK, 0005.HK, 0288.HK, 2318.HK, 3690.HK
Number of Stocks:     5
Trading Period:       2022-10-27 to 2025-10-27
Initial Capital:      $100,000.00
Capital per Stock:    $20,000.00
Position Size:        50.0% per stock

Stock Positions:
    0002.HK:   150.37 shares @ $   66.45 ($10,000.00 invested, $10,000.00 cash)
    0005.HK:   189.75 shares @ $   52.75 ($10,000.00 invested, $10,000.00 cash)
    0288.HK:  2083.33 shares @ $    4.80 ($10,000.00 invested, $10,000.00 cash)
    2318.HK:   231.48 shares @ $   43.20 ($10,000.00 invested, $10,000.00 cash)
    3690.HK:    82.37 shares @ $  121.50 ($10,000.00 invested, $10,000.00 cash)

Final Value:          $105,234.56
Total Return:         5.23%
Annualized Return:    2.58%
Max Drawdown:         -12.45%
Std Dev (daily):      1.23%
Trading Days:         489
```

## Notes

- The equal-weight benchmark uses the same 50% position sizing as conservative strategies for fair comparison
- Remaining cash (50% per stock) stays as cash throughout the period
- No rebalancing occurs - initial weights drift over time
- All 5 stocks must have data available for the specified date range
