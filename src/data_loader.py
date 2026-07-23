"""Load financial news and stock price data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

STOCK_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


class StockDataLoader:
    """Load OHLCV stock data from CSV files or yfinance."""

    def __init__(self, data_dir: str | Path = "data/stocks"):
        self.data_dir = Path(data_dir)

    def load(self, ticker: str, start: str | None = None, end: str | None = None) -> pd.DataFrame:
        ticker = ticker.upper()
        csv_path = self.data_dir / f"{ticker}.csv"

        if csv_path.exists():
            df = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
        else:
            df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            if "Date" in df.columns:
                df = df.set_index("Date")

        df.index = pd.to_datetime(df.index).tz_localize(None)
        df = df.sort_index()
        return df[[col for col in STOCK_COLUMNS if col in df.columns]]


class NewsDataLoader:
    """Load and prepare FNSPID-style financial news data."""

    REQUIRED_COLUMNS = ("headline", "url", "publisher", "date", "stock")

    def __init__(self, data_path: str | Path = "data/raw/raw_analyst_ratings.csv"):
        self.data_path = Path(data_path)

    def load(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_path)
        missing = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"News dataset missing columns: {missing}")

        df = df.dropna(subset=list(self.REQUIRED_COLUMNS)).copy()
        df["date"] = pd.to_datetime(df["date"], format="mixed", utc=True)
        df["trading_date"] = df["date"].dt.tz_convert("America/New_York").dt.normalize()
        df["trading_date"] = df["trading_date"].dt.tz_localize(None)
        return df

    def filter_by_ticker(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        return df[df["stock"].str.upper() == ticker.upper()].copy()
