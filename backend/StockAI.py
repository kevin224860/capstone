import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
import os
import psycopg2

# Config
START_DATE = "2014-01-01"
END_DATE = "2024-01-01"

DB_HOST = os.getenv('HOST')  
DB_NAME = os.getenv('DATABASE')
DB_USER = os.getenv('USER')
DB_PASSWORD = os.getenv('PASSWORD')

def get_stock_tickers_from_db():
    """Fetch all stock tickers from the StockPool table in the PostgreSQL database."""
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT stock_ID, ticker_symbol FROM StockPool;")
        tickers = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()
        return tickers

    except Exception as e:
        print(f"Failed to fetch tickers from DB: {e}")
        return []

def fetch_stock_data(ticker, start=START_DATE, end=END_DATE):
    """Fetch stock data for a single ticker."""
    print(f"Fetching stock data for {ticker} from Yahoo Finance...")

    try:
        data = yf.download(ticker, start=start, end=end)

        if data.empty:
            print(f"No data for {ticker}, skipping.")
            return None

        data["Ticker"] = ticker
        return data

    except Exception as e:
        print(f"Failed to download {ticker}: {e}")
        return None


def prepare_data(df, ticker):
    """Transform raw stock data into model-ready format for a single stock."""
    df = df.copy()

    # Check if the index is already 'Date', if so, no need to set it
    if df.index.name != 'Date':
        df.set_index(["Date", "Ticker"], inplace=True)

    # Feature engineering: Future high prices (predicting the high in 5 days)
    df[("Future_High", ticker)] = df["High"].shift(-5)  # Shift to future high for this stock (5 days ahead)
    df[("MA5", ticker)] = df["High"].rolling(window=5).mean()

    df.ffill(inplace=True)
    df.dropna(inplace=True)

    return df


def train_model(df, ticker, predicted_gains):
    """Train and evaluate the XGBoost model for a single stock's future high price."""
    X = df[[("MA5", ticker)]]
    y = df[("Future_High", ticker)]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    print(f"Training XGBoost model for {ticker}...")
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.05,
        max_depth=3,
        subsample=0.7,
        colsample_bytree=0.8,
        reg_lambda=2,
        reg_alpha=1
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Evaluate the model's performance
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    accuracy = np.mean((np.abs((y_test - y_pred) / y_test) * 100) <= 5)

    print(f"{ticker} - Mean Absolute Error: {mae:.2f}")
    print(f"{ticker} - Mean Squared Error: {mse:.2f}")
    print(f"{ticker} - Accuracy within 5% error margin: {accuracy * 100:.2f}%")

    # Calculate predicted gain
    current_price = df["Close"].iloc[-1]  # Use the last closing price as the current price
    if isinstance(current_price, pd.Series):
        current_price = current_price.iloc[0]

    predicted_high = float(y_pred[-1])  # Ensure it's a scalar
    predicted_gain = (predicted_high - current_price) / current_price * 100  # Percentage gain

    print(f"Predicted Gain for {ticker}: {predicted_gain:.2f}%")

    # Store the predicted gain in the list
    predicted_gains[ticker] = predicted_gain

    return predicted_gain


def update_ai_suggestions(stock_id, predicted_gain, industry_id=1):  # Default Industry_ID = 1
    """Update AISuggestions table with stock ratings."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Normalize gain between 0 and 5
        score = 5 * (gain - min_gain) / (max_gain - min_gain)

        # Insert the suggestion into AISuggestions table
        cursor.execute("""
            INSERT INTO AISuggestions (Industry_ID, stock_ID, Rating)
            VALUES (%s, %s, %s)
            ON CONFLICT (stock_ID) DO UPDATE
            SET Rating = EXCLUDED.Rating;
        """, (industry_id, stock_id, score))

        conn.commit()
        cursor.close()
        conn.close()

        print(f"Updated AISuggestions for stock ID {stock_id} with rating {score:.2f}.")

    except Exception as e:
        print(f"Failed to update AISuggestions for stock ID {stock_id}: {e}")

def main_ai():
    # Fetch stock IDs and tickers from the StockPool table
    tickers = get_stock_tickers_from_db()
    print(tickers)
    if not tickers:
        print(" No tickers found in the database. Exiting.")
        return
    predicted_gains = {}
    for stock_id, ticker in tickers:
        print("Stock_ID", stock_id)
        print("Ticker", ticker)
        print(f"Processing {ticker}...\n")
        raw_data = fetch_stock_data(ticker)

        if raw_data is None:
            continue

        df = prepare_data(raw_data, ticker)
        predicted_gain = train_model(df, ticker, predicted_gains)

        # Update the AISuggestions table with the predicted rating
        update_ai_suggestions(stock_id, predicted_gain)

    print("All models completed and AISuggestions table updated!")

