from data import get_prices
from results import get_best_result, save_result
import pandas as pd
import numpy as np
import strategy as st
import constants as cn

def run_backtest(ticker, start, end, strat, fast=10, slow=50, cash=10000, period=14, oversold=30, overbought=70):
    prices = get_prices(ticker, start, end)
    if strat == st.SMA_crossover or strat == st.EMA_crossover:
        signals = strat(prices, fast=fast, slow=slow)
    elif strat == st.RSI:
        signals = strat(prices, period=period, oversold=oversold, overbought=overbought)

    shares = 0

    portfolio_values = []
    
    for date in prices.index:
        price = prices[date]
        signal = signals[date]
        if cn.debug_mode:
            print(date, signal, cash, shares)
        
        if signal == 'buy' and cash >= price:
            shares = int(cash / price)
            cash -= shares * price
        
        elif signal == 'sell' and shares > 0:
            cash += shares * price
            shares = 0    
        portfolio_values.append(cash + shares * price)

    portfolio_series = pd.Series(portfolio_values)
    rolling_max = portfolio_series.cummax()
    drawdown = (portfolio_series - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    daily_returns = portfolio_series.pct_change().dropna()
    sharpe = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)

    final_value = cash + (shares * prices.iloc[-1])
    total_return = ((final_value - 10000) / 10000) * 100
    buy_and_hold = ((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100

    return total_return, buy_and_hold, prices, sharpe, max_drawdown

def run_and_display(ticker, start, end, strat, fast=10, slow=50, cash=10000, period=14, oversold=30, overbought=70):
    total_return, buy_and_hold, prices, sharpe, max_drawdown = run_backtest(
        ticker, start, end, strat,
        fast=fast, slow=slow, cash=cash,
        period=period, oversold=oversold, overbought=overbought,
    )

    print(f"Final value: ${(10000 * (1 + total_return/100)):.2f}")
    print(f"Total return: {total_return:.2f}%")
    print(f"Buy and hold return: {buy_and_hold:.2f}%")
    print(f"Outperformed buy and hold: {total_return > buy_and_hold}")

    best = get_best_result()
    if best is None or total_return > best['best_return']:
        if strat == st.SMA_crossover or strat == st.EMA_crossover:
            save_result(f"{strat}", {"fast": fast, "slow": slow}, ticker, total_return)
        elif strat == st.RSI:
            save_result(f"{strat}", {"period": period, "oversold": oversold, "overbought": overbought}, ticker, total_return)
        print("New best result saved!")
    else:
        print(f"Current best: {best['strategy']} with {best['parameters']} — {best['best_return']:.2f}%")
    print(f"Sharpe ratio: {sharpe:.2f}")
    print(f"Max drawdown: {max_drawdown*100:.0f}%")

if __name__ == "__main__":
    run_and_display("AAPL", "2020-01-01", "2025-01-01", strat=st.RSI)