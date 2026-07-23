"""Visualization helpers for technical analysis."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


class TechnicalIndicatorPlotter:
    """Plot price, indicators, and cumulative returns."""

    def __init__(self, df: pd.DataFrame, ticker: str):
        self.df = df.copy()
        self.ticker = ticker

    def plot_price_and_indicators(self) -> None:
        fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

        axes[0].plot(self.df.index, self.df["Close"], label="Close", color="black")
        if "SMA_20" in self.df.columns:
            axes[0].plot(self.df.index, self.df["SMA_20"], label="SMA 20")
        if "SMA_50" in self.df.columns:
            axes[0].plot(self.df.index, self.df["SMA_50"], label="SMA 50")
        axes[0].set_title(f"{self.ticker} Price and Moving Averages")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        if "RSI" in self.df.columns:
            axes[1].plot(self.df.index, self.df["RSI"], label="RSI", color="purple")
            axes[1].axhline(70, color="r", linestyle="--", linewidth=0.8)
            axes[1].axhline(30, color="g", linestyle="--", linewidth=0.8)
            axes[1].set_title("RSI")
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)

        if "MACD" in self.df.columns:
            axes[2].plot(self.df.index, self.df["MACD"], label="MACD")
            axes[2].plot(self.df.index, self.df["MACD_signal"], label="Signal")
            axes[2].bar(self.df.index, self.df["MACD_hist"], label="Histogram", alpha=0.4)
            axes[2].set_title("MACD")
            axes[2].legend()
            axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_cumulative_returns(cumulative_returns: pd.Series, stock_name: str) -> None:
        plt.figure(figsize=(12, 4))
        plt.plot(cumulative_returns.index, cumulative_returns.values)
        plt.title(f"{stock_name} Cumulative Returns")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
