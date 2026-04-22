import yfinance as yf

def get_prices(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.columns = data.columns.droplevel(1)
    return data['Close']

prices = get_prices("AAPL", "2020-01-01", "2025-01-01")
print(prices)