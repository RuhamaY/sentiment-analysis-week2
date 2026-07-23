"""Technical indicators using TA-Lib."""

from __future__ import annotations

import pandas as pd

try:
    import talib
except ImportError:  # pragma: no cover - optional in CI without TA-Lib binary
    talib = None


class TechnicalIndicatorCalculator:
    """Compute moving averages, RSI, and MACD for OHLCV data."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        if "Close" not in self.df.columns:
            raise ValueError("DataFrame must include a Close column")

    def add_indicators(self) -> pd.DataFrame:
        if talib is None:
            raise ImportError("TA-Lib is required. Install with: pip install TA-Lib")

        close = self.df["Close"].astype(float)
        self.df["SMA_20"] = talib.SMA(close, timeperiod=20)
        self.df["SMA_50"] = talib.SMA(close, timeperiod=50)
        self.df["EMA_10"] = talib.EMA(close, timeperiod=10)
        self.df["RSI"] = talib.RSI(close, timeperiod=14)

        macd, signal, hist = talib.MACD(close)
        self.df["MACD"] = macd
        self.df["MACD_signal"] = signal
        self.df["MACD_hist"] = hist
        return self.df
