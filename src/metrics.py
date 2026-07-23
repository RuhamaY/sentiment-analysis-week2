"""Financial performance metrics (PyNance-style)."""

from __future__ import annotations

import numpy as np
import pandas as pd


class PerformanceMetrics:
    """Daily returns, volatility, Sharpe ratio, and drawdown helpers."""

    TRADING_DAYS = 252

    @staticmethod
    def calculate_daily_returns(df: pd.DataFrame, price_col: str = "Close") -> pd.Series:
        return df[price_col].pct_change().dropna()

    @staticmethod
    def calculate_volatility(daily_returns: pd.Series) -> float:
        return float(daily_returns.std() * np.sqrt(PerformanceMetrics.TRADING_DAYS))

    @staticmethod
    def calculate_sharpe_ratio(
        daily_returns: pd.Series,
        risk_free_rate: float = 0.0,
    ) -> float:
        excess = daily_returns - (risk_free_rate / PerformanceMetrics.TRADING_DAYS)
        if excess.std() == 0:
            return 0.0
        return float(
            np.sqrt(PerformanceMetrics.TRADING_DAYS) * excess.mean() / excess.std()
        )

    @staticmethod
    def calculate_cumulative_returns(daily_returns: pd.Series) -> pd.Series:
        return (1 + daily_returns).cumprod() - 1

    @staticmethod
    def calculate_max_drawdown(daily_returns: pd.Series) -> float:
        cumulative = (1 + daily_returns).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        return float(drawdown.min())

    @staticmethod
    def calculate_rolling_volatility(df: pd.DataFrame, window: int = 30) -> pd.Series:
        returns = df["Close"].pct_change()
        return returns.rolling(window).std() * np.sqrt(PerformanceMetrics.TRADING_DAYS)

    @staticmethod
    def calculate_rolling_sharpe_ratio(
        df: pd.DataFrame,
        window: int = 30,
        risk_free_rate: float = 0.0,
    ) -> pd.Series:
        returns = df["Close"].pct_change()
        excess = returns - (risk_free_rate / PerformanceMetrics.TRADING_DAYS)
        rolling_mean = excess.rolling(window).mean()
        rolling_std = excess.rolling(window).std()
        return np.sqrt(PerformanceMetrics.TRADING_DAYS) * rolling_mean / rolling_std

    @staticmethod
    def summarize_metrics(df: pd.DataFrame) -> dict[str, float]:
        daily_returns = PerformanceMetrics.calculate_daily_returns(df)
        cumulative = PerformanceMetrics.calculate_cumulative_returns(daily_returns)
        return {
            "annualized_volatility": PerformanceMetrics.calculate_volatility(daily_returns),
            "sharpe_ratio": PerformanceMetrics.calculate_sharpe_ratio(daily_returns),
            "cumulative_return": float(cumulative.iloc[-1]),
            "max_drawdown": PerformanceMetrics.calculate_max_drawdown(daily_returns),
        }
