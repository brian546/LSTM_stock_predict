#!/usr/bin/env python3
"""Run end-to-end: inference (LSTM) -> trading backtest

This script runs `inference.py` to generate LSTM predictions and then runs
`trading.py` to perform the backtest. It calls each script as a subprocess so
no heavy refactor is required.
"""

import argparse
import os
import sys
import subprocess


def run_cmd(cmd, env=None):
    print("\n$ " + " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        raise


def main():
    parser = argparse.ArgumentParser(description='Run inference then trading backtest end-to-end')
    parser.add_argument('--ticker', type=str, required=True, help='Ticker symbol (e.g., 0005.HK)')
    parser.add_argument('--start', type=str, required=True, help='Start date for inference/trading (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, required=True, help='End date for inference/trading (YYYY-MM-DD)')
    parser.add_argument('--strategy', type=str, choices=['conservative','aggressive','both'], default='both', help='Strategy to run')
    parser.add_argument('--capital', type=float, default=100000, help='Initial capital for backtest')
    parser.add_argument('--rf_path', type=str, default=None, help='Optional Random Forest CSV path for trading')
    parser.add_argument('--no_inference', action='store_true', help='Skip running inference (use existing predictions)')
    parser.add_argument('--no_trading', action='store_true', help='Skip running trading (only run inference)')
    parser.add_argument('--target_col', type=str, default='SMA50_diff', help='Target column for inference (default: SMA50_diff)')
    parser.add_argument('--output', type=str, default=None, help='Output path for inference CSV (default: predictions/{ticker}_predict.csv)')

    args = parser.parse_args()

    ticker = args.ticker
    start = args.start
    end = args.end

    # determine inference output path
    if args.output:
        lstm_output = args.output
        os.makedirs(os.path.dirname(lstm_output) or '.', exist_ok=True)
    else:
        os.makedirs('predictions', exist_ok=True)
        lstm_output = f'predictions/{ticker}_predict.csv'

    # Optionally check model presence
    model_path = f'models/{ticker}_lstm_{args.target_col}.pth'
    if not os.path.exists(model_path) and not args.no_inference:
        print(f"Warning: model checkpoint not found at {model_path}. Make sure you've trained or placed a checkpoint there.")

    # Run inference
    if not args.no_inference:
        print("\n=== Running inference ===")
        cmd = [sys.executable, 'inference.py', '--ticker', ticker, '--target_col', args.target_col, '--start', start, '--end', end, '--output', lstm_output]
        run_cmd(cmd)
    else:
        print("Skipping inference as requested (--no_inference)")

    # Run trading
    if not args.no_trading:
        print("\n=== Running trading backtest ===")
        cmd = [sys.executable, 'trading.py', '--ticker', ticker, '--start', start, '--end', end, '--strategy', args.strategy, '--capital', str(args.capital), '--lstm_path', lstm_output]
        if args.rf_path:
            cmd += ['--rf_path', args.rf_path]
        run_cmd(cmd)
    else:
        print("Skipping trading as requested (--no_trading)")

    print('\nPipeline completed. Check predictions in', lstm_output)


if __name__ == '__main__':
    main()
