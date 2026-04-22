from itertools import product
from data import get_prices
from backtester import run_backtest
from results import get_best_result, save_result

def optimise(strategy_name, param_ranges, ticker, start, end):
    keys = list(param_ranges.keys())
    values = list(param_ranges.values())
    
    best_return = None
    best_params = None
    
    for combo in product(*values):
        params = dict(zip(keys, combo))
        if params.get('fast') >= params.get('slow'):
            continue
        else:
            total_return, buy_and_hold, _ = run_backtest(
            ticker, start, end, **params
        )
        
        print(f"Params: {params} — Return: {total_return:.2f}%")
        
        if best_return is None or total_return > best_return:
            best_return = total_return
            best_params = params
    return best_return, best_params

    print(f"\nBest: {best_params} — {best_return:.2f}%")
    save_result(strategy_name, best_params, ticker, best_return)
    

def out_of_sample_test(strategy_name, param_ranges, ticker, train_start, train_end, test_start, test_end):
    print("--- Training phase ---")
    best_return, best_params = optimise(strategy_name, param_ranges, ticker, train_start, train_end)
    
    print(f"\n--- Test phase ---")
    print(f"Testing best params {best_params} on unseen data ({test_start} to {test_end})")
    
    total_return, buy_and_hold, _ = run_backtest(ticker, test_start, test_end, **best_params)
    
    print(f"Out-of-sample return: {total_return:.2f}%")
    print(f"Buy and hold return: {buy_and_hold:.2f}%")
    print(f"Outperformed buy and hold: {total_return > buy_and_hold}")

out_of_sample_test(
    strategy_name="moving_average_crossover",
    param_ranges={"fast": range(1, 51), "slow": range(1, 51)},
    ticker="AAPL",
    train_start="2020-01-01",
    train_end="2022-12-31",
    test_start="2023-01-01",
    test_end="2025-01-01"
)