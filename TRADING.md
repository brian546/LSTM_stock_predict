### Trading Strategies

## Conservative
# Entry Indicators (Buy/Long):
Trend confirmation: Price > 200-day SMA and Price > 50-day SMA
Momentum: MACD crosses below the zero line first (confirming oversold), then crosses above the signal line with a positive histogram.
Oversold: RSI < 40 or price touches the lower Bollinger Band.
ML model predicts a price increase for the next day/week, aligning with the signal. Use as the final filter—only enter if all prior indicators align and ML confirms.
Require at least 3 indicators/ML aligning (up from 2) to maintain conservatism.
# Exit Indicators (Sell/Close Long):
Take profits when RSI >70 and price hits the upper Bollinger Band, or MACD crosses below the signal line.
Accelerate exit if ML predicts a price decrease (bearish signal) even if indicators are mixed.
Stop-loss: 5% below entry
Trailing stop: Use the 50-period SMA.
# Risk Management:
Position size: 1% of portfolio

## Aggressive
Here, the ML model enables more proactive entries, using its predictions for timing or overriding minor indicator weaknesses in strong trends.
# Entry Rules (Buy/Long):
Trend confirmation: Price > 200-day SMA and Price > 50-day SMA
Momentum: MACD crosses below the zero line first (confirming oversold), then crosses above the signal line with a positive histogram.
Oversold: RSI < 40 or price touches the lower Bollinger Band.
ML model predicts a price increase for the next day/week, aligning with the signal. Use as the final filter—only enter if all prior indicators align and ML confirms.
Require at least 2 indicators/ML aligning (up from 1) to maintain conservatism.
# Exit Rules (Sell/Close Long):
Take profits on RSI >70 or MACD bearish crossover, or when price closes below the middle Bollinger Band.
Accelerate exit if ML predicts a price decrease (bearish signal) even if indicators are mixed.
Stop-loss: 3% below entry 
Trailing stop: Use the 20-period SMA.
# Risk Management:
Position size: 3% of portfolio
