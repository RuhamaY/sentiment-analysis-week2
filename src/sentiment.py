"""Sentiment scoring for financial news headlines."""

from __future__ import annotations

import pandas as pd
from textblob import TextBlob


def score_headline(text: str) -> float:
    """Return TextBlob polarity in [-1, 1]."""
    if not isinstance(text, str) or not text.strip():
        return 0.0
    return float(TextBlob(text).sentiment.polarity)


def score_dataframe(df: pd.DataFrame, column: str = "headline") -> pd.DataFrame:
    """Add sentiment and sentiment_label columns."""
    result = df.copy()
    result["sentiment"] = result[column].apply(score_headline)
    result["sentiment_label"] = result["sentiment"].apply(_label_sentiment)
    return result


def aggregate_daily_sentiment(
    df: pd.DataFrame,
    date_col: str = "trading_date",
    sentiment_col: str = "sentiment",
) -> pd.DataFrame:
    """Average daily sentiment when multiple articles share a trading day."""
    daily = (
        df.groupby(date_col)[sentiment_col]
        .agg(avg_sentiment="mean", article_count="count")
        .reset_index()
        .rename(columns={date_col: "date"})
    )
    daily["date"] = pd.to_datetime(daily["date"])
    return daily.set_index("date").sort_index()


def _label_sentiment(score: float) -> str:
    if score > 0.05:
        return "positive"
    if score < -0.05:
        return "negative"
    return "neutral"
