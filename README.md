# Crypto-data-Pipeline
End-to-end Python pipeline for fetching, analyzing, and visualizing top cryptocurrency data.


# Cryptocurrency Data Pipeline in Python

🚀 **End-to-End Python Pipeline for Fetching, Analyzing, and Visualizing Cryptocurrency Market Data**

This project demonstrates a complete **data analytics workflow**: fetching data from the CoinGecko API, processing it, storing it in SQLite, performing feature engineering, and visualizing trends.

---

## **Project Overview**
- Dynamically fetches the **top 5 cryptocurrencies** by market cap.
- Handles **API rate limits** and network errors gracefully.
- Computes key metrics:
  - Daily returns
  - 7-day and 30-day moving averages
  - 7-day rolling volatility
- Saves processed data in **SQLite** (`crypto_prices` full table + `crypto_summary` latest record table).
- Includes **unit and integration tests** for data reliability.
- Visualizes **indexed price trends** to compare coin performance.

---

## **Installation & Setup**
1. Clone the repository:
```bash
git clone https://github.com/<your-username>/crypto-data-pipeline.git
cd crypto-data-pipeline


Tech Stack

Python – Core language for data processing

Pandas & NumPy – Data manipulation and calculations

Matplotlib & Seaborn – Visualization

SQLite – Local database storage

Requests – API calls to CoinGecko

Sample Output
Indexed Price Trends
| Coin     | Price (USD) | 7-Day Return | 7-Day Volatility |
| -------- | ----------- | ------------ | ---------------- |
| bitcoin  | 25000.00    | 0.0123       | 0.0245           |
| ethereum | 1800.00     | 0.0210       | 0.0321           |
| ...      | ...         | ...          | ...              |


Insights

Bitcoin shows lower short-term volatility compared to altcoins.

Rolling averages highlight clear short-term trends.

Indexed prices make performance comparison across coins easy.

Next Steps

Add interactive dashboards using Plotly or Streamlit

Automate daily data fetches and alerts on unusual volatility

Explore correlations between cryptocurrencies for portfolio or trading insights

License

This project is licensed under the MIT License
.

Acknowledgements

CoinGecko API
 – For free cryptocurrency data




