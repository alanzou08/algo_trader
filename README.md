# IBKR Algo Trading

A Python backtesting framework for systematic trading strategies. Currently focused on
evaluating moving-average crossover signals on historical equity data, with utilities for
parameter optimisation and out-of-sample validation.

## Project layout

| File | Purpose |
| --- | --- |
| [data.py](data.py) | Downloads daily close prices from Yahoo Finance via `yfinance`. |
| [strategy.py](strategy.py) | Strategy definitions. Currently implements `SMA_crossover`. |
| [backtester.py](backtester.py) | Runs a strategy over a price series, tracking cash, shares, and portfolio value. Reports total return, buy-and-hold return, and Sharpe ratio. |
| [optimiser.py](optimiser.py) | Grid-search over parameter ranges, optimising for either total return or Sharpe. Includes `out_of_sample_test` for train/test splits. |
| [results.py](results.py) | Persists the best run's strategy, parameters, ticker, and return to [best_result.json](best_result.json). |
| [constants.py](constants.py) | Global flags (e.g. `debug_mode`). |

## Requirements

- Python 3.10+
- `pandas`, `numpy`, `yfinance`

```bash
pip install pandas numpy yfinance
```

## Usage

### Run a single backtest

```python
from backtester import run_and_display
import strategy

run_and_display("AAPL", "2020-01-01", "2025-01-01", strat=strategy.SMA_crossover)
```

### Optimise parameters

```python
from optimiser import optimise_sharpe
import strategy

optimise_sharpe(
    strategy_name="SMA_crossover",
    param_ranges={"fast": range(1, 51), "slow": range(1, 51)},
    ticker="AAPL",
    start="2020-01-01",
    end="2025-01-01",
    strat=strategy.SMA_crossover,
)
```

Use `optimise` to maximise total return instead of Sharpe.

### Out-of-sample test

```python
from optimiser import out_of_sample_test
import strategy

out_of_sample_test(
    strategy_name="SMA_crossover",
    param_ranges={"fast": range(1, 51), "slow": range(1, 51)},
    ticker="AAPL",
    train_start="2015-01-01",
    train_end="2020-01-01",
    test_start="2020-01-01",
    test_end="2025-01-01",
    strat=strategy.SMA_crossover,
)
```

Fits parameters on the training window, then reports performance on the held-out window.

## Notes on overfitting

Grid-searching `fast`/`slow` over a single price series tends to find parameter pairs that
look excellent in-sample but generalise poorly. Prefer `out_of_sample_test` for an honest
read, and treat the in-sample optimiser's "best" result as an upper bound, not an expectation.

## Roadmap

- Live execution against Interactive Brokers (IBKR) via the TWS API.
- Additional strategies beyond SMA crossover.
- Transaction costs and slippage in the backtester.
