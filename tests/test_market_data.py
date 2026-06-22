"""Tests for backtest/market_data indicator calculations."""
import numpy as np
import pandas as pd
import pytest


def _wilder_ema(series: pd.Series, period: int) -> pd.Series:
    """Wilder's exponential moving average (alpha = 1/period)."""
    return series.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()


def _calc_rsi_wilder(close: pd.Series, period: int = 14) -> pd.Series:
    """RSI using Wilder's smoothing (the standard definition)."""
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = _wilder_ema(gain, period)
    avg_loss = _wilder_ema(loss, period)
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def _calc_adx_wilder(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """ADX using Wilder's smoothing (the standard definition)."""
    high = df["high"]
    low = df["low"]
    close = df["close"]

    up_move = high - high.shift(1)
    down_move = low.shift(1) - low
    plus_dm = pd.Series(
        np.where((up_move > down_move) & (up_move > 0), up_move, 0.0),
        index=df.index,
    )
    minus_dm = pd.Series(
        np.where((down_move > up_move) & (down_move > 0), down_move, 0.0),
        index=df.index,
    )

    prev_close = close.shift(1)
    tr = pd.Series(
        np.maximum(
            high - low,
            np.maximum(
                np.abs(high - prev_close),
                np.abs(low - prev_close),
            ),
        ),
        index=df.index,
    )

    tr_s = _wilder_ema(tr, period)
    plus_dm_s = _wilder_ema(plus_dm, period)
    minus_dm_s = _wilder_ema(minus_dm, period)

    plus_di = 100 * plus_dm_s / tr_s.replace(0, np.nan)
    minus_di = 100 * minus_dm_s / tr_s.replace(0, np.nan)
    dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di).replace(0, np.nan)
    return _wilder_ema(dx, period)


def test_adx_uses_wilder_smoothing():
    """ADX must use Wilder EMA, not simple rolling mean."""
    np.random.seed(42)
    n = 60
    idx = pd.date_range("2024-01-01", periods=n)
    # Generate a synthetic trending series with some noise
    close = 100 + np.cumsum(np.random.randn(n) * 0.5 + 0.1)
    high = close + np.abs(np.random.randn(n)) * 1.5
    low = close - np.abs(np.random.randn(n)) * 1.5
    df = pd.DataFrame({"high": high, "low": low, "close": close}, index=idx)

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "library" / "stock-trading-system" / "backtest"))
    from market_data import _calc_adx

    adx_impl = _calc_adx(df, period=14)
    adx_expected = _calc_adx_wilder(df, period=14)

    # Compare only where both are valid
    valid = adx_impl.notna() & adx_expected.notna()
    assert valid.sum() > 0
    np.testing.assert_allclose(
        adx_impl[valid].values,
        adx_expected[valid].values,
        rtol=1e-5,
        atol=1e-5,
    )


def test_rsi_uses_wilder_smoothing():
    """RSI must use Wilder's smoothing, not simple rolling mean."""
    np.random.seed(7)
    n = 60
    idx = pd.date_range("2024-01-01", periods=n)
    close = 100 + np.cumsum(np.random.randn(n) * 0.8)
    low = close - np.abs(np.random.randn(n)) * 1.5
    high = close + np.abs(np.random.randn(n)) * 1.5
    volume = pd.Series(np.random.randint(1_000_000, 10_000_000, size=n), index=idx)
    df = pd.DataFrame({"close": close, "low": low, "high": high, "volume": volume}, index=idx)

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "library" / "stock-trading-system" / "backtest"))
    from market_data import _calc_indicators

    df_out = _calc_indicators(df.copy())
    rsi_impl = df_out["rsi14"]
    rsi_expected = _calc_rsi_wilder(df["close"], period=14)

    valid = rsi_impl.notna() & rsi_expected.notna()
    assert valid.sum() > 0
    np.testing.assert_allclose(
        rsi_impl[valid].values,
        rsi_expected[valid].values,
        rtol=1e-5,
        atol=1e-5,
    )


def test_low_20d_uses_low_price():
    """20-day low for exit signals should use lowest low, not lowest close."""
    idx = pd.date_range("2024-01-01", periods=25)
    # Construct a series where the lowest close and lowest low differ
    close = pd.Series([100.0 + i * 0.1 for i in range(25)], index=idx)
    low = close.copy()
    high = close + 2.0
    volume = pd.Series([1_000_000] * 25, index=idx)
    # On day 20, push the low well below the close (long shadow)
    low.iloc[20] = 90.0
    close.iloc[20] = 99.0

    df = pd.DataFrame({"close": close, "low": low, "high": high, "volume": volume}, index=idx)

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "library" / "stock-trading-system" / "backtest"))
    from market_data import _calc_indicators

    df_out = _calc_indicators(df.copy())
    # The 20-day low should include the shadow low from day 20
    expected_low_20d = low.rolling(20).min().shift(1).iloc[-1]
    assert df_out["low_20d"].iloc[-1] == pytest.approx(expected_low_20d)
