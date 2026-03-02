import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Stock Price Analyzer Dashboard")

# User Input
ticker = st.text_input("Enter Stock Symbol (Example: AAPL)", "AAPL")
period = st.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "5y"])
ma_period = st.slider("Select Moving Average Period", 5, 100, 20)

# Fetch Data
data = yf.download(ticker, period=period)

if not data.empty:

    # Moving Average
    data["MA"] = data["Close"].rolling(ma_period).mean()

    # RSI Calculation
    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    # MACD Calculation
    exp1 = data["Close"].ewm(span=12, adjust=False).mean()
    exp2 = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD"] = exp1 - exp2

    # Plot Price + MA
    st.subheader("Stock Price with Moving Average")
    fig1, ax1 = plt.subplots()
    ax1.plot(data["Close"], label="Close Price")
    ax1.plot(data["MA"], label="Moving Average")
    ax1.legend()
    st.pyplot(fig1)

    # Plot RSI
    st.subheader("RSI Indicator")
    fig2, ax2 = plt.subplots()
    ax2.plot(data["RSI"], label="RSI")
    ax2.axhline(70)
    ax2.axhline(30)
    ax2.legend()
    st.pyplot(fig2)

    # Plot MACD
    st.subheader("MACD Indicator")
    fig3, ax3 = plt.subplots()
    ax3.plot(data["MACD"], label="MACD")
    ax3.legend()
    st.pyplot(fig3)

else:
    st.error("Invalid stock symbol or no data available.")