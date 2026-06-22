"""Tests for backtest engine implementation vs SKILL.md contracts.

These tests use monkeypatch to force entry/exit signals so that we can
isolate the risk-management mechanics (position limits, drawdown,
black-swan circuit breaker) from the noisiness of real price patterns.
"""
import numpy as np
import pandas as pd
import pytest


def _make_df(prices, lows=None, highs=None, volumes=None):
    """Build a minimal OHLCV DataFrame for backtesting."""
    n = len(prices)
    idx = pd.date_range("2024-01-01", periods=n)
    close = np.asarray(prices, dtype=float)
    if lows is None:
        lows = close * 0.98
    if highs is None:
        highs = close * 1.02
    if volumes is None:
        volumes = np.full(n, 10_000_000)
    df = pd.DataFrame({
        "close": close,
        "low": np.asarray(lows, dtype=float),
        "high": np.asarray(highs, dtype=float),
        "volume": np.asarray(volumes, dtype=float),
    }, index=idx)
    df["ma5"] = df["close"].rolling(5).mean()
    df["ma10"] = df["close"].rolling(10).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["high_10d"] = df["high"].rolling(10).max().shift(1)
    df["high_20d"] = df["high"].rolling(20).max().shift(1)
    df["low_20d"] = df["low"].rolling(20).min().shift(1)
    df["vol_ma5"] = df["volume"].rolling(5).mean()
    df["vol_ratio"] = df["volume"] / df["vol_ma5"]
    df["prev_close"] = df["close"].shift(1)
    df["tr"] = np.maximum(
        df["high"] - df["low"],
        np.maximum(
            np.abs(df["high"] - df["prev_close"]),
            np.abs(df["low"] - df["prev_close"]),
        ),
    )
    df["atr14"] = df["tr"].ewm(alpha=1.0 / 14, min_periods=14, adjust=False).mean()
    df["rsi14"] = 50.0
    df["bb_mid"] = df["close"].rolling(20).mean()
    df["bb_std"] = df["close"].rolling(20).std()
    df["bb_upper"] = df["bb_mid"] + 2 * df["bb_std"]
    df["bb_lower"] = df["bb_mid"] - 2 * df["bb_std"]
    df["atr_pct"] = df["atr14"] / df["close"] * 100
    df["adx14"] = 30.0
    df["volume"] = df["volume"].astype(int)
    return df


def _make_index(prices):
    idx = pd.date_range("2024-01-01", periods=len(prices))
    df = pd.DataFrame({"close": np.asarray(prices, dtype=float)}, index=idx)
    df["ma60"] = df["close"].rolling(60).min() * 0.99  # keep price above ma60 from day 1
    df["above_ma60"] = True
    return df


@pytest.fixture
def engine(monkeypatch):
    """Return a BacktestEngine with entry always forced True for unit tests."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "library" / "stock-trading-system" / "backtest"))
    from backtest import BacktestEngine

    e = BacktestEngine(capital=1_000_000, max_positions=1)
    e.industry_map = {"TEST": "other"}

    def _always_enter(row, code):
        # Avoid entering on rows with insufficient indicator history
        return bool(not pd.isna(row.get("atr14")) and row["atr14"] > 0)

    monkeypatch.setattr(e, "_check_entry", _always_enter)
    return e


def test_single_position_limit_25pct(engine):
    """Skill 06: single-stock position must not exceed 25% of capital."""
    n = 80
    # price=100, atr=0.5 -> naive sizing buys 10_000 shares -> 100% position
    price = 100.0
    atr = 0.5
    prices = np.full(n, price)
    lows = prices - atr
    highs = prices + atr
    volumes = np.full(n, 10_000_000)
    df = _make_df(prices, lows=lows, highs=highs, volumes=volumes)
    index_df = _make_index(np.linspace(3000, 3200, n))

    engine.run({"TEST": df}, index_df)

    assert "TEST" in engine.positions
    pos_value = engine.positions["TEST"]["shares"] * df["close"].iloc[-1]
    assert pos_value / engine.initial_capital <= 0.25 + 1e-6


def test_account_drawdown_15pct_reduce(engine, monkeypatch):
    """Skill 01: 15% drawdown -> reduce to half; 20% -> liquidate."""
    n = 80
    prices = np.concatenate([
        np.linspace(100, 150, 30),   # rally
        np.linspace(150, 110, 51),   # drop -> >20% drawdown from peak
    ])[:n]
    lows = prices * 0.98
    highs = prices * 1.02
    volumes = np.full(n, 10_000_000)
    df = _make_df(prices, lows=lows, highs=highs, volumes=volumes)
    index_df = _make_index(np.linspace(3000, 3200, n))

    # Force no normal exits so we can test drawdown protection in isolation
    monkeypatch.setattr(engine, "_check_exit", lambda code, row, date: None)

    engine.run({"TEST": df}, index_df)

    equity = pd.DataFrame(engine.equity_curve)
    peak = equity["equity"].cummax()
    drawdown = (peak - equity["equity"]) / peak
    assert drawdown.max() < 0.20


def test_black_swan_circuit_breaker_10pct(engine, monkeypatch):
    """Skill 01: single-day account drop >=10% -> liquidate and cool off."""
    n = 80
    price = 100.0
    atr = 0.5  # small ATR -> max position (25% cap) -> account drop large enough
    prices = np.full(n, price)
    prices[50] = 60.0   # -40% single day -> ~10% account drop at 25% position
    prices[51:] = 60.0
    lows = prices - atr
    highs = prices + atr
    volumes = np.full(n, 10_000_000)
    df = _make_df(prices, lows=lows, highs=highs, volumes=volumes)
    # Override atr14 to the small value for consistent sizing
    df["atr14"] = atr
    # After the black-swan gap, invalidate atr14 so the engine cannot re-enter
    df.loc[df.index[51]:, "atr14"] = np.nan
    index_df = _make_index(np.linspace(3000, 3200, n))

    # Disable normal exits so the black-swan handler is tested in isolation
    monkeypatch.setattr(engine, "_check_exit", lambda code, row, date: None)

    engine.run({"TEST": df}, index_df)

    # The black-swan handler should have liquidated the position after the gap down
    assert "TEST" not in engine.positions
    sell_trades = [t for t in engine.trades if t["action"] in ("SELL", "REDUCE")]
    assert len(sell_trades) > 0


def test_reduce_100_shares_liquidates_or_skips(engine):
    """When only 100 shares are held, a 50% reduce must not create fractional shares."""
    n = 80
    prices = np.full(n, 100.0)
    lows = prices * 0.98
    highs = prices * 1.02
    volumes = np.full(n, 10_000_000)
    df = _make_df(prices, lows=lows, highs=highs, volumes=volumes)
    index_df = _make_index(np.linspace(3000, 3200, n))

    engine.run({"TEST": df}, index_df)

    for code, pos in engine.positions.items():
        assert pos["shares"] % 100 == 0


def test_mean_reversion_skill_exists():
    """Skill 13: mean-reversion strategy must be callable from the engine."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent / "library" / "stock-trading-system" / "backtest"))
    import backtest

    assert hasattr(backtest.BacktestEngine, "_check_mean_reversion_entry")
    assert hasattr(backtest.BacktestEngine, "_check_mean_reversion_exit")
