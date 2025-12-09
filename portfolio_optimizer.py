"""
Portfolio Optimizer - Find optimal portfolio combinations
Combines multiple strategies with different weights to maximize Sharpe ratio
"""

import argparse
import pandas as pd
import numpy as np
import os
from itertools import product


def load_portfolio_history(ticker, strategy_type, results_dir='trading_results'):
    """Load portfolio history for a specific strategy"""
    strategy_dir = os.path.join(results_dir, f"{ticker}_{strategy_type.lower()}")
    portfolio_file = os.path.join(strategy_dir, 'portfolio_history.csv')
    
    if not os.path.exists(portfolio_file):
        print(f"Warning: Portfolio history not found for {ticker} ({strategy_type})")
        return None
    
    df = pd.read_csv(portfolio_file)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    return df


def calculate_portfolio_metrics(combined_portfolio_value, initial_capital=20000):
    """Calculate performance metrics for a portfolio"""
    if len(combined_portfolio_value) == 0:
        return None
    
    final_value = combined_portfolio_value.iloc[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    
    # Calculate daily returns
    daily_returns = combined_portfolio_value.pct_change().dropna() * 100
    std_dev = daily_returns.std()
    
    # Calculate max drawdown
    peak = combined_portfolio_value.cummax()
    drawdown = (combined_portfolio_value - peak) / peak * 100
    max_drawdown = drawdown.min()
    
    # Calculate Sharpe ratio (annualized)
    if std_dev > 0:
        annualized_std = std_dev * np.sqrt(252)
        sharpe_ratio = (total_return - 2.0) / annualized_std  # Assuming 2% risk-free rate
    else:
        sharpe_ratio = 0
    
    return {
        'final_value': final_value,
        'total_return': total_return,
        'std_dev': std_dev,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'volatility': std_dev * np.sqrt(252)
    }


def combine_portfolios(strategies, weights, initial_capital=20000, results_dir='trading_results'):
    """
    Combine multiple strategies with given weights
    
    Args:
        strategies: List of tuples [(ticker, strategy_type), ...]
        weights: List of weights for each strategy (should sum to 1.0)
        initial_capital: Total initial capital
        results_dir: Directory containing trading results
    
    Returns:
        Combined portfolio metrics
    """
    if abs(sum(weights) - 1.0) > 0.01:
        print(f"Warning: Weights sum to {sum(weights):.2f}, not 1.0")
        return None
    
    # Load all portfolio histories
    portfolios = []
    for (ticker, strategy_type) in strategies:
        df = load_portfolio_history(ticker, strategy_type, results_dir)
        if df is None:
            return None
        portfolios.append(df)
    
    # Find common dates
    common_dates = portfolios[0].index
    for df in portfolios[1:]:
        common_dates = common_dates.intersection(df.index)
    
    if len(common_dates) == 0:
        print("Warning: No common dates found across portfolios")
        return None
    
    # Calculate combined portfolio value
    combined_value = pd.Series(0, index=common_dates)
    
    for i, df in enumerate(portfolios):
        # Get portfolio value for common dates
        strategy_values = df.loc[common_dates, 'Portfolio_Value']
        
        # Normalize to initial capital and apply weight
        normalized_values = (strategy_values / strategy_values.iloc[0]) * initial_capital
        combined_value += normalized_values * weights[i]
    
    # Calculate metrics
    metrics = calculate_portfolio_metrics(combined_value, initial_capital)
    
    if metrics:
        metrics['strategies'] = strategies
        metrics['weights'] = weights
        metrics['portfolio_series'] = combined_value
    
    return metrics


def optimize_portfolio(strategies, initial_capital=20000, results_dir='trading_results', 
                       weight_step=0.1, top_n=10):
    """
    Find optimal portfolio combinations
    
    Args:
        strategies: List of tuples [(ticker, strategy_type), ...]
        initial_capital: Total initial capital
        results_dir: Directory containing trading results
        weight_step: Step size for weight grid search (e.g., 0.1 for 10% increments)
        top_n: Number of top portfolios to return
    
    Returns:
        List of top portfolio combinations sorted by Sharpe ratio
    """
    n_strategies = len(strategies)
    
    # Generate all possible weight combinations
    weight_range = np.arange(0, 1.0 + weight_step, weight_step)
    weight_combinations = []
    
    # Generate all combinations that sum to approximately 1.0
    for weights in product(weight_range, repeat=n_strategies):
        if abs(sum(weights) - 1.0) < 0.01:  # Allow small rounding error
            # Normalize to exactly 1.0
            normalized = np.array(weights) / sum(weights)
            weight_combinations.append(tuple(normalized))
    
    print(f"Testing {len(weight_combinations)} weight combinations...")
    
    # Test all combinations
    results = []
    for i, weights in enumerate(weight_combinations):
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/{len(weight_combinations)}")
        
        metrics = combine_portfolios(strategies, weights, initial_capital, results_dir)
        if metrics:
            results.append(metrics)
    
    # Sort by Sharpe ratio
    results.sort(key=lambda x: x['sharpe_ratio'], reverse=True)
    
    return results[:top_n]


def main():
    parser = argparse.ArgumentParser(description='Portfolio Optimizer - Find optimal strategy combinations')
    parser.add_argument('--strategies', nargs='+', required=True,
                        help='List of strategies in format "ticker:type" (e.g., 0288.HK:Aggressive 0005.HK:Conservative)')
    parser.add_argument('--capital', type=float, default=20000,
                        help='Initial capital (default: 20000)')
    parser.add_argument('--results_dir', type=str, default='trading_results',
                        help='Directory containing trading results')
    parser.add_argument('--weight_step', type=float, default=0.1,
                        help='Weight step size for grid search (default: 0.1)')
    parser.add_argument('--top_n', type=int, default=10,
                        help='Number of top portfolios to display (default: 10)')
    parser.add_argument('--custom_weights', nargs='+', type=float, default=None,
                        help='Test specific weights (e.g., 0.5 0.3 0.2)')
    
    args = parser.parse_args()
    
    # Parse strategies
    strategies = []
    for s in args.strategies:
        parts = s.split(':')
        if len(parts) != 2:
            print(f"Error: Invalid strategy format '{s}'. Use 'ticker:type' (e.g., 0288.HK:Aggressive)")
            return
        ticker, strategy_type = parts
        strategies.append((ticker, strategy_type))
    
    print("="*100)
    print("PORTFOLIO OPTIMIZER")
    print("="*100)
    print(f"Strategies to combine: {len(strategies)}")
    for i, (ticker, stype) in enumerate(strategies, 1):
        print(f"  {i}. {ticker} ({stype})")
    print(f"Initial Capital: ${args.capital:,.2f}")
    print("="*100)
    
    # Test custom weights if provided
    if args.custom_weights:
        if len(args.custom_weights) != len(strategies):
            print(f"Error: Number of weights ({len(args.custom_weights)}) doesn't match strategies ({len(strategies)})")
            return
        
        print("\nTesting custom weights...")
        weights = args.custom_weights
        print(f"Weights: {' + '.join([f'{w:.1%}' for w in weights])}")
        
        metrics = combine_portfolios(strategies, weights, args.capital, args.results_dir)
        if metrics:
            print(f"\nCustom Portfolio Results:")
            print(f"  Final Value:      ${metrics['final_value']:,.2f}")
            print(f"  Total Return:     {metrics['total_return']:.2f}%")
            print(f"  Sharpe Ratio:     {metrics['sharpe_ratio']:.4f}")
            print(f"  Max Drawdown:     {metrics['max_drawdown']:.2f}%")
            print(f"  Volatility:       {metrics['volatility']:.2f}%")
        return
    
    # Optimize portfolio
    print(f"\nOptimizing portfolio with weight step: {args.weight_step}")
    top_portfolios = optimize_portfolio(strategies, args.capital, args.results_dir, 
                                       args.weight_step, args.top_n)
    
    if not top_portfolios:
        print("No valid portfolio combinations found.")
        return
    
    # Display results
    print("\n" + "="*100)
    print(f"TOP {len(top_portfolios)} PORTFOLIO COMBINATIONS (Ranked by Sharpe Ratio)")
    print("="*100)
    
    results_data = []
    
    for rank, portfolio in enumerate(top_portfolios, 1):
        print(f"\n#{rank}")
        print(f"  Sharpe Ratio:     {portfolio['sharpe_ratio']:.4f}")
        print(f"  Total Return:     {portfolio['total_return']:.2f}%")
        print(f"  Final Value:      ${portfolio['final_value']:,.2f}")
        print(f"  Max Drawdown:     {portfolio['max_drawdown']:.2f}%")
        print(f"  Std Dev (daily):  {portfolio['std_dev']:.2f}%")
        print(f"  Volatility:       {portfolio['volatility']:.2f}%")
        print(f"  Portfolio Composition:")
        
        portfolio_str = []
        for (ticker, stype), weight in zip(portfolio['strategies'], portfolio['weights']):
            print(f"    {weight:>6.1%} - {ticker} ({stype})")
            portfolio_str.append(f"{weight:.1%} {ticker} ({stype})")
        
        results_data.append({
            'Rank': rank,
            'Sharpe_Ratio': portfolio['sharpe_ratio'],
            'Total_Return_%': portfolio['total_return'],
            'Final_Value': portfolio['final_value'],
            'Max_Drawdown_%': portfolio['max_drawdown'],
            'Std_Dev_%': portfolio['std_dev'],
            'Volatility_%': portfolio['volatility'],
            'Portfolio': ' + '.join(portfolio_str)
        })
    
    # Save results
    output_file = os.path.join(args.results_dir, 'optimal_portfolios.csv')
    results_df = pd.DataFrame(results_data)
    results_df.to_csv(output_file, index=False)
    print(f"\n{'='*100}")
    print(f"Results saved to: {output_file}")
    
    # Save Excel version
    excel_file = os.path.join(args.results_dir, 'optimal_portfolios.xlsx')
    results_df.to_excel(excel_file, index=False, sheet_name='Optimal Portfolios')
    print(f"Excel file saved to: {excel_file}")
    
    print("="*100)


if __name__ == '__main__':
    main()
