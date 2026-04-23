from itertools import product
from data import get_prices
from backtester import run_backtest
from results import get_best_result, save_result
from constants import w1, w2, w3
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

        _, _, _, sharpe, _ = run_backtest(
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

def optimise_weighted(strategy_name, param_ranges, ticker, start, end, strat):
    keys = list(param_ranges.keys())
    values = list(param_ranges.values())
    
    optimised_sharpe = None
    optimised_return = None
    optimised_drawdown = None
    best_params = None
    best_score = None
    
    for combo in product(*values):
        params = dict(zip(keys, combo))
        if params.get('fast') >= params.get('slow'):
            continue

        total_return, _, _, sharpe, max_drawdown = run_backtest(
            ticker, start, end, strat, **params
        )
        
        score = (w1 * sharpe) + (w2 * total_return) + (w3 * max_drawdown)  

        print(f"Params: {params} — Score: {score:.0f}")

        if best_score is None or score > best_score:
            best_params = params
            optimised_sharpe = sharpe 
            best_score = score
            optimised_drawdown = max_drawdown
            optimised_return = total_return

    print(f"\nBest: {best_params}: {best_score:.2f} = {w1} x {optimised_sharpe:.2f} + {w2} x {optimised_return:.0f}% + {w3} x {optimised_drawdown:.2f}%")
    save_result(strategy_name, best_params, ticker, optimised_sharpe, score, optimised_return, optimised_drawdown)
    return optimised_sharpe, best_params, score, optimised_return, optimised_drawdown

if __name__ == "__main__":
    optimise_weighted(
        strategy_name="SMA_crossover",
        param_ranges={"fast": range(1, 51), "slow": range(1, 41)},
        ticker="AAPL",
        start="2015-01-01",
        end="2025-01-01",
        strat=strategy.SMA_crossover,
    )