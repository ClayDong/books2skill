# -*- coding: utf-8 -*-
"""
Market data layer: fetch A-share daily data via EastMoney API (zero dependency)
+ calculate all technical indicators needed by strategy.

Usage:
    from market_data import get_stock_data, get_index_data
    df = get_stock_data("600519", "20200101", "20251231")
"""
import json
import time
import requests
import pandas as pd
import numpy as np

# EastMoney API endpoint
_EM_KLINE_URL = "http://push2his.eastmoney.com/api/qt/stock/kline/get"


def _get_secid(code: str) -> str:
    """Convert stock code to EastMoney secid format."""
    if code.startswith('6') or code.startswith('9'):
        return f"1.{code}"   # Shanghai
    elif code.startswith('0') or code.startswith('2') or code.startswith('3'):
        return f"0.{code}"   # Shenzhen
    elif code.startswith('8') or code.startswith('4'):
        return f"0.{code}"   # Beijing (North Exchange)
    return f"1.{code}"


def _fetch_klines(code: str, start: str, end: str, is_index: bool = False) -> list:
    """Fetch daily kline data from EastMoney API."""
    secid = _get_secid(code) if not is_index else f"1.{code}"

    params = {
        'secid': secid,
        'fields1': 'f1,f2,f3,f4,f5,f6',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
        'klt': '101',      # daily
        'fqt': '1',         # front-adjusted
        'beg': start,
        'end': end,
    }

    try:
        resp = requests.get(_EM_KLINE_URL, params=params, timeout=15,
                            headers={'User-Agent': 'Mozilla/5.0'})
        data = resp.json()
        if not data or data.get('data') is None:
            print(f"[ERROR] {code}: API returned no data")
            return []
        klines = data['data'].get('klines', [])
        return klines
    except Exception as e:
        print(f"[ERROR] Failed to fetch {code}: {e}")
        return []


def _parse_klines(klines: list) -> pd.DataFrame:
    """Parse kline strings to DataFrame.
    Format: date,open,close,high,low,volume,amount,amplitude,pct_change,change,turnover
    """
    if not klines:
        return pd.DataFrame()

    records = []
    for line in klines:
        parts = line.split(',')
        records.append({
            'date': parts[0],
            'open': float(parts[1]),
            'close': float(parts[2]),
            'high': float(parts[3]),
            'low': float(parts[4]),
            'volume': float(parts[5]),
            'amount': float(parts[6]),
            'pct_change': float(parts[8]) if parts[8] else 0.0,
        })

    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()
    return df


def get_stock_data(code: str, start: str = "20200101", end: str = "20251231") -> pd.DataFrame:
    """Fetch A-share daily data (front-adjusted) and calculate all indicators."""
    klines = _fetch_klines(code, start, end)
    df = _parse_klines(klines)
    if df.empty:
        return df

    df = _calc_indicators(df)
    return df


def get_index_data(code: str = "000001", start: str = "20200101",
                   end: str = "20251231") -> pd.DataFrame:
    """Fetch index daily data (default: Shanghai Composite)."""
    klines = _fetch_klines(code, start, end, is_index=True)
    df = _parse_klines(klines)
    if df.empty:
        return df

    df['ma60'] = df['close'].rolling(60).mean()
    df['above_ma60'] = df['close'] > df['ma60']
    return df


def _calc_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all technical indicators needed by strategy."""
    # ── Moving averages ──
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()

    # ── Breakout levels (exclude today, use shift(1)) ──
    df['high_10d'] = df['high'].rolling(10).max().shift(1)
    df['high_20d'] = df['high'].rolling(20).max().shift(1)
    df['low_10d'] = df['close'].rolling(10).min().shift(1)

    # ── Volume ──
    df['vol_ma5'] = df['volume'].rolling(5).mean()
    df['vol_ratio'] = df['volume'] / df['vol_ma5']

    # ── ATR (14-day) ──
    df['prev_close'] = df['close'].shift(1)
    df['tr'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['prev_close']),
            abs(df['low'] - df['prev_close'])
        )
    )
    df['atr14'] = df['tr'].rolling(14).mean()

    # ── RSI (14-day) ──
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = (-delta).where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df['rsi14'] = 100 - (100 / (1 + rs))

    # ── Bollinger Bands (20, 2) ──
    df['bb_mid'] = df['close'].rolling(20).mean()
    df['bb_std'] = df['close'].rolling(20).std()
    df['bb_upper'] = df['bb_mid'] + 2 * df['bb_std']
    df['bb_lower'] = df['bb_mid'] - 2 * df['bb_std']

    # ── ATR as % of price ──
    df['atr_pct'] = df['atr14'] / df['close'] * 100

    return df


def get_stock_list_by_industry() -> dict:
    """Return representative stock list by industry (from 100-stock validation)."""
    return {
        "白酒": ["600519", "000858", "000568"],
        "食品饮料": ["600887", "002507"],
        "白电": ["000651", "000333"],
        "医药": ["600276", "300760"],
        "新能源": ["300750", "601012"],
        "银行": ["600036", "601398"],
        "消费电子": ["002475", "002415"],
        "化工": ["600309"],
        "传媒": ["002027"],
        "计算机": ["002410"],
    }


if __name__ == "__main__":
    print("Testing market_data (EastMoney API)...")
    df = get_stock_data("600519", "20240101", "20241231")
    if not df.empty:
        print(f"Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(df[['close', 'atr14', 'rsi14', 'bb_lower', 'high_10d', 'vol_ratio']].tail())
    else:
        print("Failed to fetch data")
