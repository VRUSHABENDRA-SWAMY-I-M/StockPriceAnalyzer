import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def calculate_moving_averages(data):
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    return data

def generate_signals(data):
    data["Signal"] = 0
    data.loc[data["MA20"] > data["MA50"], "Signal"] = 1
    data.loc[data["MA20"] < data["MA50"], "Signal"] = -1
    return data

def plot_data(data, ticker):
    plt.figure(figsize=(12,6))
    plt.plot(data["Close"], label="Close Price")
    plt.plot(data["MA20"], label="20-Day MA")
    plt.plot(data["MA50"], label="50-Day MA")

    plt.title(f"{ticker} Stock Price Analysis")
    plt.legend()
    plt.show()

def main():
    ticker = input("Enter stock ticker (Example: TCS.NS): ")
    data = fetch_stock_data(ticker)
    data = calculate_moving_averages(data)
    data = generate_signals(data)
    plot_data(data, ticker)

    print("\nLatest Signals:")
    print(data[["Close", "MA20", "MA50", "Signal"]].tail())

if __name__ == "__main__":
    main()