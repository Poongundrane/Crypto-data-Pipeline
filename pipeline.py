"""Educational cryptocurrency market-data pipeline, adapted from the original Colab project."""
import os
import sqlite3
import time

import matplotlib.pyplot as plt
import pandas as pd
import requests

BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_json(path, params, retries=5):
    headers = {}
    api_key = os.getenv("COINGECKO_DEMO_API_KEY")
    if api_key:
        headers["x-cg-demo-api-key"] = api_key
    for attempt in range(retries):
        response = requests.get(BASE_URL + path, params=params,
                                headers=headers, timeout=30)
        if response.status_code != 429:
            response.raise_for_status()
            return response.json()
        if attempt == retries - 1:
            raise RuntimeError(f"CoinGecko HTTP 429 for {path}: retry limit reached")
        delay = min(60 * 2 ** attempt, 240)
        retry_after = response.headers.get("Retry-After", "")
        if retry_after.isdigit():
            delay = max(delay, int(retry_after))
        print(f"HTTP 429 for {path}; retrying in {delay}s", flush=True)
        time.sleep(delay)


def fetch_top_coins(n=5):
    data = fetch_json("/coins/markets", {
        "vs_currency": "usd", "order": "market_cap_desc",
        "per_page": n, "page": 1,
    })
    return [coin["id"] for coin in data]


def fetch_coin_data(coin, days=30):
    data = fetch_json(f"/coins/{coin}/market_chart",
                      {"vs_currency": "usd", "days": days})
    frames = []
    for key, column in [("prices", "price"), ("market_caps", "market_cap"),
                        ("total_volumes", "volume")]:
        frame = pd.DataFrame(data.get(key, []), columns=["timestamp", column])
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
        frames.append(frame.drop_duplicates("timestamp"))
    frame = frames[0].merge(frames[1], on="timestamp", how="left")
    frame = frame.merge(frames[2], on="timestamp", how="left")
    frame["coin"] = coin
    return frame


def engineer_features(data):
    if data.empty:
        raise ValueError("No market data received")
    data = data.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
    data = data.dropna(subset=["price"]).sort_values(["coin", "timestamp"])
    if data.empty or (data["price"] <= 0).any():
        raise ValueError("Valid positive prices are required")
    data["timestamp"] = data["timestamp"].dt.floor("D")
    data = data.drop_duplicates(["coin", "timestamp"], keep="last")
    # Reindex to calendar days; missing observations remain missing.
    daily = []
    for coin, group in data.groupby("coin"):
        group = group.set_index("timestamp").asfreq("D")
        group["coin"] = coin
        daily.append(group.reset_index())
    data = pd.concat(daily, ignore_index=True)
    prices = data.groupby("coin")["price"]
    data["price_indexed"] = prices.transform(lambda x: x / x.iloc[0] * 100)
    data["return"] = prices.pct_change(fill_method=None)
    data["ma7"] = prices.transform(lambda x: x.rolling(7, min_periods=1).mean())
    data["ma30"] = prices.transform(lambda x: x.rolling(30, min_periods=1).mean())
    data["volatility7"] = data.groupby("coin")["return"].transform(
        lambda x: x.rolling(7, min_periods=2).std())
    return data


def save_data(data, db_path="crypto_data.db"):
    with sqlite3.connect(db_path) as conn:
        data.to_sql("crypto_prices", conn, if_exists="replace", index=False)
        data.groupby("coin").tail(1).to_sql(
            "crypto_summary", conn, if_exists="replace", index=False)


def plot_prices(data):
    for coin, group in data.groupby("coin"):
        plt.plot(group["timestamp"], group["price_indexed"], label=coin)
    plt.title("Indexed Cryptocurrency Price Trends (Base = 100)")
    plt.xlabel("Date")
    plt.ylabel("Indexed Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("indexed_prices.png")
    plt.close()


def main():
    coins = fetch_top_coins()
    if not coins:
        raise RuntimeError("No coins returned")
    frames = []
    for coin in coins:
        time.sleep(25)
        print(f"Fetching {coin}...", flush=True)
        frame = fetch_coin_data(coin)
        if frame.empty:
            raise RuntimeError(f"No price data for {coin}")
        frames.append(frame)
    data = engineer_features(pd.concat(frames, ignore_index=True))
    save_data(data)
    plot_prices(data)
    print(f"Saved {len(data)} daily records for {len(coins)} coins")


if __name__ == "__main__":
    main()
