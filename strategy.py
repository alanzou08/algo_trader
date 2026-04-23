import pandas as pd

def SMA_crossover(prices, fast=10, slow=50):
    fast_ma = prices.rolling(fast).mean()
    slow_ma = prices.rolling(slow).mean()

    signals = pd.Series(index=prices.index, dtype=str)
    signals[:] = 'hold'
    signals[fast_ma > slow_ma] = 'buy'
    signals[fast_ma < slow_ma] = 'sell'
    
    return signals

def EMA_crossover(prices, fast=10, slow=50):
    fast_ema = prices.ewm(span=fast, adjust=False).mean()
    slow_ema = prices.ewm(span=slow, adjust=False).mean()
    
    signals = pd.Series(index=prices.index, dtype=str)
    signals[:] = 'hold'
    signals[fast_ema > slow_ema] = 'buy'
    signals[fast_ema < slow_ema] = 'sell'
    return signals

def RSI(prices, period=14, oversold=30, overbought=70):
    delta = prices.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    signals = pd.Series(index=prices.index, dtype=str)
    signals[:] = 'hold'
    signals[rsi < oversold] = 'buy'
    signals[rsi > overbought] = 'sell'
    return signals