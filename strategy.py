import vectorbt as vbt

# Download AAPL data
data = vbt.YFData.download('AAPL', start='2020-01-01', end='2025-01-01').get('Close')

# Calculate moving averages
fast_ma = vbt.MA.run(data, 10, short_name='fast')
slow_ma = vbt.MA.run(data, 50, short_name='slow')

# Generate buy/sell signals
entries = fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

# Run backtest
pf = vbt.Portfolio.from_signals(data, entries, exits, init_cash=10000)
print(pf.total_return())