import pandas as pd

def moving_average_crossover(prices, fast=10, slow=50):
    fast_ma = prices.rolling(fast).mean()
    slow_ma = prices.rolling(slow).mean()

    signals = pd.Series(index=prices.index, dtype=str)
    signals[:] = 'hold'
    signals[fast_ma > slow_ma] = 'buy'
    signals[fast_ma < slow_ma] = 'sell'
    
    return signals

from data import get_prices

prices = get_prices("AAPL", "2020-01-01", "2025-01-01")
signals = moving_average_crossover(prices)
print(signals)