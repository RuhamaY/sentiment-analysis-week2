"""Download stock OHLCV data into data/stocks/."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_loader import StockDataLoader


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch stock data via yfinance")
    parser.add_argument("tickers", nargs="+", help="Ticker symbols, e.g. AAPL MSFT")
    parser.add_argument("--start", default="2020-01-01")
    parser.add_argument("--end", default=None)
    parser.add_argument(
        "--output-dir",
        default="data/stocks",
        help="Directory for CSV output",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    loader = StockDataLoader(output_dir)

    for ticker in args.tickers:
        df = loader.load(ticker, start=args.start, end=args.end)
        path = output_dir / f"{ticker.upper()}.csv"
        df.reset_index().to_csv(path, index=False)
        print(f"Saved {len(df)} rows to {path}")


if __name__ == "__main__":
    main()
