import json
import os

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "best_result.json")

def get_best_result():
    if not os.path.exists(RESULTS_FILE):
        return None
    
    with open(RESULTS_FILE, 'r') as f:
        return json.load(f)

def save_result(strategy, parameters, ticker, total_return, sharpe=None, max_drawdown=None, score=None):
    result = {
        "strategy": strategy,
        "parameters": parameters,
        "ticker": ticker,
        "best_return": total_return,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "score": score,
    }
    
    with open(RESULTS_FILE, 'w') as f:
        json.dump(result, f, indent=4)