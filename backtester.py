from data import get_prices
from strategy import moving_average_crossover
import constants

def run_backtest(ticker, start, end, cash=10000):
    prices = get_prices(ticker, start, end)
    signals = moving_average_crossover(prices)

    shares = 0
    
    for date in prices.index:
        price = prices[date]
        signal = signals[date]
        if constants.debug_mode:
            print(date, signal, cash, shares)
        
        if signal == 'buy' and cash >= price:
            shares = int(cash / price)
            cash -= shares * price
        
        elif signal == 'sell' and shares > 0:
            cash += shares * price
            shares = 0

    final_value = cash + (shares * prices.iloc[-1])
    total_return = ((final_value - 10000) / 10000) * 100

    print(f"Final value: ${final_value:.2f}")
    print(f"Total return: {total_return:.2f}%")
    buy_and_hold = ((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100
    print(f"Buy and hold return: {buy_and_hold:.2f}%")
    print(f"Outperformed buy and hold: {total_return > buy_and_hold}")

run_backtest("AAPL", "2020-01-01", "2025-01-01")
