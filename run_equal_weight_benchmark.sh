#!/bin/bash

# Run benchmarks with equal-weight portfolio
# This script generates both the 2800.HK benchmark and the equal-weight 5-stock benchmark

conda run -n trading python benchmark.py \
  --ticker 2800.HK \
  --start 2022-10-27 \
  --end 2025-10-27 \
  --capital 100000 \
  --equal-weight 0002.HK 0005.HK 0288.HK 2318.HK 3690.HK \
  --compare 0002.HK 0005.HK 0288.HK 2318.HK 3690.HK

echo ""
echo "Now generating aggregated portfolio comparison chart..."
echo ""

# Generate aggregated comparison chart with both benchmarks
conda run -n trading python compare_portfolio_aggregated.py \
  --benchmark 2800.HK \
  --tickers 0002.HK 0005.HK 0288.HK 2318.HK 3690.HK \
  --capital-per-stock 20000

echo ""
echo "✅ Complete! Check trading_results/ for all results and charts."
