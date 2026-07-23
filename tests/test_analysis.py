"""Unit tests for core analysis modules."""

import pandas as pd

from sentiment import aggregate_daily_sentiment, score_headline
from metrics import PerformanceMetrics
from correlation import pearson_correlation, align_sentiment_and_returns


def test_score_headline_positive():
    assert score_headline("Stock hits record high and beats forecasts") >= 0


def test_score_headline_negative():
    assert score_headline("Stock crashes after disastrous earnings and massive layoffs") < 0


def test_aggregate_daily_sentiment():
    df = pd.DataFrame(
        {
            "trading_date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02"]),
            "sentiment": [0.5, 0.1, -0.2],
        }
    )
    daily = aggregate_daily_sentiment(df)
    assert len(daily) == 2
    assert daily.loc[pd.Timestamp("2024-01-01"), "article_count"] == 2


def test_calculate_daily_returns():
    prices = pd.DataFrame({"Close": [100.0, 110.0, 99.0]})
    returns = PerformanceMetrics.calculate_daily_returns(prices)
    assert len(returns) == 2
    assert abs(returns.iloc[0] - 0.1) < 1e-9


def test_pearson_correlation():
    a = pd.Series([1, 2, 3, 4, 5])
    b = pd.Series([2, 4, 6, 8, 10])
    assert abs(pearson_correlation(a, b) - 1.0) < 1e-9


def test_align_sentiment_and_returns():
    daily_sentiment = pd.DataFrame(
        {"avg_sentiment": [0.2, -0.1]},
        index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
    )
    stock_df = pd.DataFrame(
        {"Close": [100.0, 105.0, 103.0]},
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
    )
    merged = align_sentiment_and_returns(daily_sentiment, stock_df)
    assert "daily_return" in merged.columns
    assert len(merged) >= 1
