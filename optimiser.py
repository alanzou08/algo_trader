from itertools import product
from data import get_prices
from backtester import run_backtest
from results import get_best_result, save_result
import strategy

def optimise(strategy_name, param_ranges, ticker, start, end, strat):
    keys = list(param_ranges.keys())
    values = list(param_ranges.values())
    
    best_return = None
    best_params = None
    
    for combo in product(*values):
        params = dict(zip(keys, combo))
        if params.get('fast') >= params.get('slow'):
            continue

        total_return, _ = run_backtest(
            ticker, start, end, strat, **params
        )

        print(f"Params: {params} — Return: {total_return:.2f}%")

        if best_return is None or total_return > best_return:
            best_return = total_return
            best_params = params

    print(f"\nBest: {best_params} — {best_return:.2f}%")
    save_result(strategy_name, best_params, ticker, best_return)
    return best_return, best_params

def optimise_sharpe(strategy_name, param_ranges, ticker, start, end, strat):
    keys = list(param_ranges.keys())
    values = list(param_ranges.values())
    
    best_sharpe = None
    best_params = None
    
    for combo in product(*values):
        params = dict(zip(keys, combo))
        if params.get('fast') >= params.get('slow'):
            continue

        _, _, _, sharpe = run_backtest(
            ticker, start, end, strat, **params
        )

        print(f"Params: {params} — Sharpe: {sharpe:.2f}")

        if best_sharpe is None or sharpe > best_sharpe:
            best_params = params
            best_sharpe = sharpe 

    print(f"\nBest: {best_params} — {best_sharpe:.2f}")
    save_result(strategy_name, best_params, ticker, best_sharpe)
    return best_sharpe, best_params

def out_of_sample_test(strategy_name, param_ranges, ticker, train_start, train_end, test_start, test_end, strat):
    print("--- Training phase ---")
    best_return, best_params = optimise(strategy_name, param_ranges, ticker, train_start, train_end, strat)

    print(f"\n--- Test phase ---")
    print(f"Testing best params {best_params} on unseen data ({test_start} to {test_end})")

    total_return, buy_and_hold, _, _= run_backtest(ticker, test_start, test_end, strat, **best_params)
    
    print(f"Out-of-sample return: {total_return:.2f}%")
    print(f"Buy and hold return: {buy_and_hold:.2f}%")
    print(f"Outperformed buy and hold: {total_return > buy_and_hold}")

# out_of_sample_test(
#     strategy_name="SMA_crossover",
#     param_ranges={"fast": range(1, 51), "slow": range(1, 51)},
#     ticker="AAPL",
#     train_start="2020-01-01",
#     train_end="2022-12-31",
#     test_start="2023-01-01",
#     test_end="2025-01-01",
#     strat=strategy.SMA_crossover,
# )

optimise_sharpe(
    strategy_name="SMA_crossover",
    param_ranges={"fast": range(1, 51), "slow": range(1, 51)},
    ticker="AAPL",
    start="2020-01-01",
    end="2025-01-01",
    strat=strategy.SMA_crossover,
)