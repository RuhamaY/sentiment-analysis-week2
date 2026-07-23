"""Correlation analysis between news sentiment and stock returns."""

from __future__ import annotations

import pandas as pd


def align_sentiment_and_returns(
    daily_sentiment: pd.DataFrame,
    stock_df: pd.DataFrame,
    sentiment_col: str = "avg_sentiment",
) -> pd.DataFrame:
    """Merge daily sentiment with same-day and next-day stock returns."""
    prices = stock_df.copy()
    prices.index = pd.to_datetime(prices.index).tz_localize(None)
    prices["daily_return"] = prices["Close"].pct_change()

    merged = daily_sentiment.join(prices[["Close", "daily_return"]], how="inner")
    merged["next_day_return"] = merged["daily_return"].shift(-1)
    return merged.dropna(subset=[sentiment_col, "daily_return"])


def pearson_correlation(series_a: pd.Series, series_b: pd.Series) -> float:
    aligned = pd.concat([series_a, series_b], axis=1).dropna()
    if aligned.empty:
        return float("nan")
    return float(aligned.iloc[:, 0].corr(aligned.iloc[:, 1], method="pearson"))


def summarize_correlations(merged: pd.DataFrame, sentiment_col: str = "avg_sentiment") -> dict[str, float]:
    """Pearson correlations for same-day and next-day returns."""
    return {
        "sentiment_vs_same_day_return": pearson_correlation(
            merged[sentiment_col], merged["daily_return"]
        ),
        "sentiment_vs_next_day_return": pearson_correlation(
            merged[sentiment_col], merged["next_day_return"]
        ),
        "lagged_sentiment_vs_return": pearson_correlation(
            merged[sentiment_col].shift(1), merged["daily_return"]
        ),
    }
