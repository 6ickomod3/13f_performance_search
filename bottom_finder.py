import yfinance as yf
import pandas as pd
import numpy as np

def calculate_rsi(data, period=14):
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

def calculate_moving_averages(data, short_window=50, long_window=200):
    short_ma = data['Close'].rolling(window=short_window).mean()
    long_ma = data['Close'].rolling(window=long_window).mean()
    return short_ma, long_ma

def check_buy_signal(stock_ticker, start_date, end_date):
    data = yf.download(stock_ticker, start=start_date, end=end_date)
    
    # Calculate indicators
    data['RSI'] = calculate_rsi(data)
    data['MACD'], data['Signal'] = calculate_macd(data)
    data['Short_MA'], data['Long_MA'] = calculate_moving_averages(data)

    # Define buy signals
    latest_data = data.iloc[-1]
    rsi_buy = latest_data['RSI'] < 100  # RSI below 30 indicates oversold conditions
    macd_buy = latest_data['MACD'] > latest_data['Signal'] and latest_data['MACD'] < 0  # MACD bullish crossover
    ma_buy = latest_data['Short_MA'] > latest_data['Long_MA']  # Golden cross

    buy_signal = rsi_buy and macd_buy and ma_buy

    return buy_signal, data.tail(10)  # Return signal and last 10 rows for context

# Example usage
stock_ticker = 'QQQ'
start_date = '2016-01-01'
end_date = '2024-11-20'

buy_signal, recent_data = check_buy_signal(stock_ticker, start_date, end_date)

if buy_signal:
    print(f"{stock_ticker} shows a buy signal based on the analysis.")
else:
    print(f"{stock_ticker} does not show a buy signal based on the analysis.")

print(recent_data)
