# Cryptocurrency Market Data Pipeline

An educational Python and SQLite pipeline originally developed for the Programming for Data Analysis module at Dublin Business School. The portfolio version was refactored with AI assistance from the original Colab notebook.

## Architecture

CoinGecko REST API → pandas transformations → SQLite → Matplotlib

- Fetch the top five cryptocurrencies by market capitalisation and request 30 days of historical data.
- Align prices, market capitalisation and volume by timestamp.
- Select the last available observation per UTC calendar day.
- Calculate indexed prices (base 100), daily returns, 7- and 30-day moving averages and 7-day rolling return volatility.
- Store historical observations and the latest record per coin in SQLite.
- Generate a comparative indexed-price chart.

## Setup

```bash
git clone https://github.com/Poongundrane/Crypto-data-Pipeline.git
cd Crypto-data-Pipeline
python -m pip install -r requirements.txt
python pipeline.py
```

Internet access is required. CoinGecko access policies and rate limits may affect execution. The script uses bounded retries and does not require a hardcoded credential.

## Repository structure

- `pipeline.py`: acquisition, transformation, storage and visualisation.
- `requirements.txt`: Python dependencies.
- `tests/test_pipeline.py`: offline feature and database checks.
- `.gitignore`: excludes generated databases, charts and local environment files.

## Outputs

- `crypto_data.db`: tables `crypto_prices` and `crypto_summary`.
- `indexed_prices.png`: comparative price chart.

Example SQL query:

```sql
SELECT coin, timestamp, price, ma7, ma30
FROM crypto_summary
ORDER BY coin;
```

## Testing

```bash
python -m unittest discover -s tests -v
```

Tests use synthetic observations rather than live market data. The refactored version has not yet been execution-verified.

## Limitations

Daily values represent the last available observation, not an official exchange closing price. The latest day may be incomplete. Moving averages use available observations within their windows; missing days are not forward-filled. API availability and coin selection can change. This is an educational project, not a trading system.

## Attribution

Market data: [CoinGecko API](https://www.coingecko.com/en/api). Original academic project by Poongundran Elanthiraiyan. ChatGPT was used as a learning co-pilot in the original coursework and to assist with the portfolio refactor and documentation.

See LICENSE for code licensing. Data remains subject to the provider's terms.
