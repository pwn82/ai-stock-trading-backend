import pandas as pd
import numpy as np


def find_column(df, candidates):

    normalized = {
        str(c).lower().strip(): c
        for c in df.columns
    }

    for candidate in candidates:

        candidate = candidate.lower()

        if candidate in normalized:
            return normalized[candidate]

    for column in df.columns:

        col = str(column).lower()

        for candidate in candidates:

            if candidate.lower() in col:
                return column

    return None


def calculate_indicators(df: pd.DataFrame):

    if df.empty:
        return {
            "rows": 0,
            "message": "No market data available"
        }

    close_column = find_column(
        df,
        [
            "close",
            "closing_price",
            "price",
            "adj_close"
        ]
    )

    volume_column = find_column(
        df,
        [
            "volume",
            "traded_volume"
        ]
    )

    if close_column is None:

        return {
            "rows": len(df),
            "message": "Close/price column not found",
            "columns": list(df.columns)
        }

    data = df.copy()

    data[close_column] = pd.to_numeric(
        data[close_column],
        errors="coerce"
    )

    data = data.dropna(
        subset=[close_column]
    )

    close = data[close_column]

    result = {
        "rows": len(data),
        "close_column": close_column,
        "latest_price": float(close.iloc[-1]),
        "first_price": float(close.iloc[0]),
    }

    if len(close) >= 2:

        result["price_change"] = float(
            close.iloc[-1] - close.iloc[0]
        )

        result["price_change_percent"] = float(
            ((close.iloc[-1] - close.iloc[0])
             / close.iloc[0]) * 100
        )

    if len(close) >= 5:
        result["sma_5"] = float(
            close.rolling(5).mean().iloc[-1]
        )

    if len(close) >= 20:
        result["sma_20"] = float(
            close.rolling(20).mean().iloc[-1]
        )

    if len(close) >= 50:
        result["sma_50"] = float(
            close.rolling(50).mean().iloc[-1]
        )

    if len(close) >= 14:

        delta = close.diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss.replace(0, np.nan)

        rsi = 100 - (100 / (1 + rs))

        result["rsi_14"] = float(
            rsi.iloc[-1]
        )

    if volume_column:

        data[volume_column] = pd.to_numeric(
            data[volume_column],
            errors="coerce"
        )

        result["latest_volume"] = float(
            data[volume_column].iloc[-1]
        )

        result["average_volume"] = float(
            data[volume_column].tail(20).mean()
        )

    return result