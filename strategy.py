import pandas as pd

def SMA_crossover(prices, fast=10, slow=50):
    fast_ma = prices.rolling(fast).mean()
    slow_ma = prices.rolling(slow).mean()

    signals = pd.Series(index=prices.index, dtype=str)
    signals[:] = 'hold'
    signals[fast_ma > slow_ma] = 'buy'
    signals[fast_ma < slow_ma] = 'sell'
    
    return signals