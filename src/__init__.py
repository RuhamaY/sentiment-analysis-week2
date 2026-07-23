"""Nova Financial Solutions — sentiment and stock analysis package."""

from .correlation import align_sentiment_and_returns, pearson_correlation, summarize_correlations
from .data_loader import NewsDataLoader, StockDataLoader
from .indicators import TechnicalIndicatorCalculator
from .metrics import PerformanceMetrics
from .sentiment import aggregate_daily_sentiment, score_dataframe, score_headline
from .utils import TechnicalIndicatorPlotter

__all__ = [
    "NewsDataLoader",
    "StockDataLoader",
    "TechnicalIndicatorCalculator",
    "PerformanceMetrics",
    "TechnicalIndicatorPlotter",
    "score_headline",
    "score_dataframe",
    "aggregate_daily_sentiment",
    "align_sentiment_and_returns",
    "pearson_correlation",
    "summarize_correlations",
]
