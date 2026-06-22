# -*- coding: utf-8 -*-
"""
Backtest engine: encode skill 02/05/06/07/08 logic into Python, run 5-year backtest.

Usage:
    python backtest.py                    # run with default 10 stocks
    python backtest.py --stocks 600519 000858  # run with custom stocks
    python backtest.py --start 20200101 --end 20251231  # custom date range

Output:
    - Console: performance summary
    - backtest_report.json: detailed trades + equity curve + metrics
    - backtest_equity_curve.png: equity curve chart
"""
import argparse
import json
import os
from datetime import datetime
from collections import defaultdict

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from market_data import get_stock_data, get_index_data, get_stock_list_by_industry

# ═══════════════════════════════════════════════════════════════
# Constants (from skill 10-system-optimization, verified 2026-06-19)
# ═══════════════════════════════════════════════════════════════
COMMISSION_RATE = 0.00025    # 佣金 0.025% (双边)
STAMP_TAX_RATE = 0.0005      # 印花税 0.05% (仅卖出)
SLIPPAGE_RATE = 0.001        # 滑点 0.1% (双边)
BUY_COST = COMMISSION_RATE + SLIPPAGE_RATE          # 0.125%
SELL_COST = COMMISSION_RATE + STAMP_TAX_RATE + SLIPPAGE_RATE  # 0.175%

RISK_PER_TRADE = 0.01        # 单笔风险 1% (from skill 01/06)
MAX_POSITION_PCT = 0.25      # 单一股票 ≤25% (from skill 06)
MAX_TOTAL_PCT = 0.80         # 总仓位 ≤80% (from skill 06)
MAX_INDUSTRY_PCT = 0.20      # 单一行业 ≤20% (from skill 01/06)
MAX_POSITIONS = 5            # 最大持仓数
INITIAL_CAPITAL = 1_000_000  # 初始资金 100万

# 涨跌停限制
def get_limit_pct(code: str) -> float:
    """Return limit-up/down percentage for a stock code."""
    if code.startswith(('300', '688')):
        return 0.20  # 创业板/科创板 20%
    return 0.10      # 主板 10%


# ═══════════════════════════════════════════════════════════════
# Backtest Engine
# ═══════════════════════════════════════════════════════════════
class BacktestEngine:
    def __init__(self, capital=INITIAL_CAPITAL, max_positions=MAX_POSITIONS):
        self.initial_capital = capital
        self.cash = capital
        self.max_positions = max_positions
        self.positions = {}   # {code: position_dict}
        self.trades = []      # trade records
        self.equity_curve = []
        self.industry_map = {}
        # Skill 01: account-level risk controls
        self.peak_equity = capital
        self.drawdown_cooldown_until = None  # date string, no new entries
        self.black_swan_cooldown_until = None  # date string, liquidation + 3-day cool-off
        self.high_risk_mark = False  # single-day drop >=5% flag

    def run(self, stock_data: dict, index_data: pd.DataFrame):
        """Run backtest across all dates."""
        # Build unified date index
        all_dates = sorted(set().union(*[set(df.index) for df in stock_data.values()]))
        index_dates = set(index_data.index)

        print(f"Backtest period: {all_dates[0].date()} ~ {all_dates[-1].date()}")
        print(f"Trading days: {len(all_dates)}")
        print(f"Stocks: {len(stock_data)}")
        print("-" * 70)

        for idx, date in enumerate(all_dates):
            date_str = date.strftime('%Y-%m-%d')

            # ── 0. Skill 01: account-level drawdown / black-swan circuit breaker ──
            self._update_peak_and_drawdown(date_str, stock_data, date)
            self._apply_circuit_breakers(date_str, stock_data, date, idx, all_dates)

            # Cool-off period: no new entries after black-swan liquidation
            in_cooloff = (
                self.black_swan_cooldown_until is not None
                and date_str <= self.black_swan_cooldown_until
            )

            # ── 1. Market filter (skill 05: 大盘60日线) ──
            if date not in index_dates:
                continue
            market_ok = bool(index_data.loc[date, 'above_ma60'])

            # ── 2. Check exits for existing positions (skill 08 / skill 13) ──
            for code in list(self.positions.keys()):
                if code not in stock_data or date not in stock_data[code].index:
                    continue
                row = stock_data[code].loc[date]
                pos = self.positions.get(code)
                if pos and pos.get('strategy') == 'mean_reversion':
                    self._check_mean_reversion_exit(code, row, date)
                else:
                    self._check_exit(code, row, date)

            # ── 3. Check entries (skill 05 / skill 13) ──
            if (
                market_ok
                and not in_cooloff
                and len(self.positions) < self.max_positions
            ):
                for code, df in stock_data.items():
                    if code in self.positions:
                        continue
                    if date not in df.index:
                        continue
                    row = df.loc[date]
                    # Skill 05: breakout entry (trending market)
                    if self._check_entry(row, code):
                        if self._check_position_limits(code):
                            self._enter_position(code, row, date, strategy='breakout')
                    # Skill 13: mean reversion entry (ranging market, mutually exclusive with 05)
                    elif self._check_mean_reversion_entry(row, code):
                        if self._check_position_limits(code):
                            self._enter_position(code, row, date, strategy='mean_reversion')

            # ── 4. Record daily equity ──
            total_equity = self.cash + sum(
                p['shares'] * stock_data[c].loc[date, 'close']
                if c in stock_data and date in stock_data[c].index
                else p['shares'] * p['entry_price']
                for c, p in self.positions.items()
            )
            self.equity_curve.append({
                'date': date_str,
                'equity': round(total_equity, 2),
                'cash': round(self.cash, 2),
                'positions': len(self.positions),
                'market_ok': market_ok,
            })

        return self._generate_report()

    # ─────────────────────────────────────────────
    # Skill 01: Risk Control Baseline
    # ─────────────────────────────────────────────
    def _update_peak_and_drawdown(self, date_str: str, stock_data: dict = None, date=None):
        """Update peak equity and enforce drawdown / black-swan rules."""
        current_equity = (
            self.cash
            + sum(
                p['shares'] * (
                    stock_data[c].loc[date, 'close']
                    if stock_data and date and c in stock_data and date in stock_data[c].index
                    else p['entry_price']
                )
                for c, p in self.positions.items()
            )
        )
        if current_equity > self.peak_equity:
            self.peak_equity = current_equity

    def _apply_circuit_breakers(self, date_str: str, stock_data: dict, date, idx: int, all_dates: list):
        """Apply account-level drawdown and black-swan circuit breakers."""
        if not self.equity_curve:
            return
        yesterday_equity = self.equity_curve[-1]['equity']

        # Current equity uses today's close price for held positions
        current_equity = self.cash + sum(
            p['shares'] * stock_data[c].loc[date, 'close']
            if c in stock_data and date in stock_data[c].index
            else p['shares'] * p['entry_price']
            for c, p in self.positions.items()
        )

        # Drawdown from peak
        drawdown = (self.peak_equity - current_equity) / self.peak_equity

        # Single-day drop
        single_day_drop = (yesterday_equity - current_equity) / yesterday_equity

        # Skill 01 black-swan thresholds (account-level, single-day)
        if single_day_drop >= 0.10:
            # Liquidate all positions and cool off 3 trading days
            self._liquidate_all(date_str, 'black_swan_10pct', stock_data, date)
            self.black_swan_cooldown_until = self._add_trading_days(idx, 3, all_dates)
            self.high_risk_mark = False
            return
        elif single_day_drop >= 0.08:
            self._reduce_all(date_str, 'black_swan_8pct', 0.5, stock_data, date)
            self.high_risk_mark = True
        elif single_day_drop >= 0.05:
            self.high_risk_mark = True
        else:
            self.high_risk_mark = False

        # Skill 01 account drawdown thresholds (only if not already handled)
        if drawdown >= 0.20:
            self._liquidate_all(date_str, 'drawdown_20pct', stock_data, date)
            self.drawdown_cooldown_until = date_str
        elif drawdown >= 0.15:
            self._reduce_all(date_str, 'drawdown_15pct', 0.5, stock_data, date)

    def _add_trading_days(self, idx: int, days: int, all_dates: list) -> str:
        """Add N trading days to the current date index."""
        target_idx = min(idx + days, len(all_dates) - 1)
        return all_dates[target_idx].strftime('%Y-%m-%d')

    def _liquidate_all(self, date_str: str, reason: str, stock_data: dict = None, date=None):
        """Liquidate all positions at current market prices."""
        for code in list(self.positions.keys()):
            # Use today's close price if available, fall back to entry price
            if stock_data and date and code in stock_data and date in stock_data[code].index:
                price = stock_data[code].loc[date, 'close']
            else:
                price = self.positions[code]['entry_price']
            self._exit(code, price, datetime.strptime(date_str, '%Y-%m-%d'), reason)

    def _reduce_all(self, date_str: str, reason: str, ratio: float, stock_data: dict = None, date=None):
        """Reduce all positions by ratio at current market prices."""
        for code in list(self.positions.keys()):
            # Use today's close price if available, fall back to entry price
            if stock_data and date and code in stock_data and date in stock_data[code].index:
                price = stock_data[code].loc[date, 'close']
            else:
                price = self.positions[code]['entry_price']
            self._reduce(code, price, datetime.strptime(date_str, '%Y-%m-%d'), reason, ratio)

    # ─────────────────────────────────────────────
    # Skill 05: Breakout Entry
    # ─────────────────────────────────────────────
    def _check_entry(self, row: pd.Series, code: str) -> bool:
        """Check breakout entry signal (skill 05)."""
        # Skip if data incomplete
        if pd.isna(row.get('high_10d')) or pd.isna(row.get('atr14')):
            return False

        # 1. Breakout: close > 10-day high or 20-day high
        breakout_10 = row['close'] > row['high_10d']
        breakout_20 = row['close'] > row['high_20d'] if not pd.isna(row.get('high_20d')) else False
        if not (breakout_10 or breakout_20):
            return False

        # 2. Volume confirmation: vol_ratio >= 1.5
        if pd.isna(row.get('vol_ratio')) or row['vol_ratio'] < 1.5:
            return False

        # 3. Limit-up filter: don't chase if limit-up
        limit_pct = get_limit_pct(code)
        if 'pct_change' in row and not pd.isna(row['pct_change']):
            if row['pct_change'] >= limit_pct * 100 * 0.99:
                return False  # 涨停封板，不追单

        # 4. ATR sanity check
        if pd.isna(row['atr14']) or row['atr14'] <= 0:
            return False

        # 5. 20-day MA filter (优化新增：收盘价>20日线才入场，减少逆势)
        if not pd.isna(row.get('ma20')) and row['close'] < row['ma20']:
            return False

        # 6. ADX filter (辅助判据：只过滤极端无趋势，避免误杀盈利交易)
        # ADX>25=强趋势，ADX<20=无趋势，20-25=模糊区
        # 回测验证：ADX<20硬过滤导致年化5.18%→4.05%（-22%），故调整为ADX<15才拒绝
        # ADX<15=极端无趋势（震荡市假突破概率极高），15-25=模糊区（允许入场），>25=强趋势
        if not pd.isna(row.get('adx14')) and row['adx14'] < 15:
            return False  # ADX<15，极端无趋势，假突破概率极高

        return True

    # ─────────────────────────────────────────────
    # Skill 06: Position Sizing
    # ─────────────────────────────────────────────
    def _calc_shares(self, atr: float, price: float, code: str = None) -> int:
        """Calculate position size (skill 06: 股数=资金×1%/(2×ATR))."""
        risk_amount = self.initial_capital * RISK_PER_TRADE
        shares = risk_amount / (2 * atr)
        shares = int(shares // 100) * 100  # 向下取整到100股
        shares = max(shares, 0)

        if code is None or shares == 0:
            return shares

        # Skill 06: single-stock position cap at 25% of capital
        max_shares_by_cap = int((self.initial_capital * MAX_POSITION_PCT) / price // 100) * 100
        return min(shares, max_shares_by_cap)

    def _check_position_limits(self, code: str) -> bool:
        """Check position limits (skill 06)."""
        # Total position limit
        total_position_value = sum(p['shares'] * p['entry_price'] for p in self.positions.values())
        if total_position_value / self.initial_capital >= MAX_TOTAL_PCT:
            return False

        # Industry concentration limit
        industry = self.industry_map.get(code, 'unknown')
        industry_value = sum(
            p['shares'] * p['entry_price']
            for c, p in self.positions.items()
            if self.industry_map.get(c, 'unknown') == industry
        )
        if industry_value / self.initial_capital >= MAX_INDUSTRY_PCT:
            return False

        return True

    def _enter_position(self, code: str, row: pd.Series, date, strategy: str = 'breakout'):
        """Enter a new position."""
        # Skill 05 step 8: ATR adaptive logic
        # High volatility (atr14 > atr20): use atr10 (faster, tighter stop)
        # Low volatility (atr14 <= atr20): use atr20 (wider stop, more room to breathe)
        atr10 = row.get('atr10', row['atr14'])
        atr20 = row.get('atr20', row['atr14'])
        if not pd.isna(atr10) and not pd.isna(atr20) and not pd.isna(row['atr14']):
            if row['atr14'] > atr20:
                # High volatility: use atr10 (faster response, tighter stop)
                atr_for_sizing = atr10
            else:
                # Low volatility: use atr20 (wider stop, give position more room)
                atr_for_sizing = atr20
        else:
            atr_for_sizing = row['atr14']

        shares = self._calc_shares(atr_for_sizing, row['close'], code=code)
        if shares == 0:
            return  # 高价股小资金场景：不足100股不建仓

        # Skill 13: reduce position for mean reversion (首仓15% instead of 25%)
        if strategy == 'mean_reversion':
            max_shares_mr = int((self.initial_capital * 0.15) / row['close'] // 100) * 100
            shares = min(shares, max_shares_mr)

        cost = shares * row['close'] * (1 + BUY_COST)
        if cost > self.cash:
            return

        if strategy == 'mean_reversion':
            # Skill 13 stop loss: min(entry*0.97, bb_lower*0.98), locked never moves down
            stop_loss = min(row['close'] * 0.97, row.get('bb_lower', row['close']) * 0.98)
        else:
            stop_loss = row['close'] - 2 * row['atr14']  # skill 07: 入场价-2×ATR

        self.cash -= cost
        self.positions[code] = {
            'code': code,
            'shares': shares,
            'entry_price': row['close'],
            'entry_date': date.strftime('%Y-%m-%d'),
            'stop_loss': stop_loss,
            'highest_close': row['close'],  # 持仓期间最高收盘价 (skill 08)
            'industry': self.industry_map.get(code, 'unknown'),
            'below_ma20_days': 0,  # 连续低于20日线天数 (skill 08)
            'entry_date_for_t1': date.strftime('%Y-%m-%d'),  # T+1 lock: cannot sell on entry day
            'strategy': strategy,  # 'breakout' or 'mean_reversion'
        }

        self.trades.append({
            'date': date.strftime('%Y-%m-%d'),
            'code': code,
            'action': 'BUY',
            'shares': shares,
            'price': round(row['close'], 2),
            'cost': round(cost, 2),
            'reason': f'{strategy}_entry',
            'stop_loss': round(stop_loss, 2),
            'atr14': round(row['atr14'], 2),
            'vol_ratio': round(row['vol_ratio'], 2),
        })

    # ─────────────────────────────────────────────
    # Skill 08: Trend Exit
    # ─────────────────────────────────────────────
    def _check_exit(self, code: str, row: pd.Series, date):
        """Check exit signals (skill 08)."""
        pos = self.positions[code]
        close = row['close']

        # T+1 check: cannot sell on the same calendar day as entry
        if date.strftime('%Y-%m-%d') == pos['entry_date_for_t1']:
            return

        # Update highest close
        if close > pos['highest_close']:
            pos['highest_close'] = close

        # ── 1. Stop loss (skill 07) ──
        if close <= pos['stop_loss']:
            self._exit(code, close, date, 'stop_loss')
            return

        # ── 2. 20-day low close (优化：10日→20日，减少假信号) ──
        if not pd.isna(row.get('low_20d')) and close < row['low_20d']:
            self._reduce(code, close, date, '20d_low', 0.5)
            return

        # ── 3. Profit drawback protection (skill 08, 优化v2：放宽阈值让利润奔跑) ──
        entry = pos['entry_price']
        highest = pos['highest_close']
        current_profit = (close - entry) / entry
        max_profit = (highest - entry) / entry
        drawback = max_profit - current_profit

        if max_profit > 0.5 and drawback >= 0.20:
            self._exit(code, close, date, 'profit_drawback_50%')
            return
        if max_profit > 0.3 and drawback >= 0.15:
            self._reduce(code, close, date, 'profit_drawback_30%', 0.5)
            return

        # ── 4. 20-day MA breakdown (skill 08: 连续2日跌破才清仓) ──
        if not pd.isna(row.get('ma20')):
            if close < row['ma20']:
                pos['below_ma20_days'] += 1
                # Quick stop: if held <=3 days and already below ma20, exit immediately
                entry_date_dt = datetime.strptime(pos['entry_date_for_t1'], '%Y-%m-%d')
                hold_days = (date - entry_date_dt).days
                if hold_days <= 3:
                    self._exit(code, close, date, 'ma20_quick_stop')
                    return
                if pos['below_ma20_days'] >= 2:
                    self._exit(code, close, date, 'ma20_breakdown_2d')
                    return
            else:
                pos['below_ma20_days'] = 0

    def _exit(self, code: str, price: float, date, reason: str):
        """Full exit."""
        pos = self.positions[code]
        proceeds = pos['shares'] * price * (1 - SELL_COST)
        cost_basis = pos['shares'] * pos['entry_price'] * (1 + BUY_COST)
        pnl = proceeds - cost_basis
        pnl_pct = pnl / cost_basis * 100

        # Calculate actual hold days
        entry_date_dt = datetime.strptime(pos['entry_date_for_t1'], '%Y-%m-%d')
        hold_days = max(0, (date - entry_date_dt).days)

        self.cash += proceeds
        self.trades.append({
            'date': date.strftime('%Y-%m-%d'),
            'code': code,
            'action': 'SELL',
            'shares': pos['shares'],
            'price': round(price, 2),
            'proceeds': round(proceeds, 2),
            'pnl': round(pnl, 2),
            'pnl_pct': round(pnl_pct, 2),
            'reason': reason,
            'hold_days': hold_days,
        })
        del self.positions[code]

    def _reduce(self, code: str, price: float, date, reason: str, ratio: float):
        """Partial exit (reduce position)."""
        pos = self.positions[code]
        sell_shares = int(pos['shares'] * ratio // 100) * 100
        if sell_shares < 100:
            # A-share minimum lot is 100 shares. For a 100-share position,
            # a 50% reduce is impossible; liquidate instead to honor the signal.
            if pos['shares'] == 100:
                self._exit(code, price, date, f"{reason}_force_exit_100shares")
            return

        proceeds = sell_shares * price * (1 - SELL_COST)
        cost_basis = sell_shares * pos['entry_price'] * (1 + BUY_COST)
        pnl = proceeds - cost_basis
        pnl_pct = pnl / cost_basis * 100

        self.cash += proceeds
        pos['shares'] -= sell_shares

        self.trades.append({
            'date': date.strftime('%Y-%m-%d'),
            'code': code,
            'action': 'REDUCE',
            'shares': sell_shares,
            'price': round(price, 2),
            'proceeds': round(proceeds, 2),
            'pnl': round(pnl, 2),
            'pnl_pct': round(pnl_pct, 2),
            'reason': reason,
            'remaining': pos['shares'],
        })

    # ─────────────────────────────────────────────
    # Skill 13: Mean Reversion (placeholder hooks)
    # ─────────────────────────────────────────────
    def _check_mean_reversion_entry(self, row: pd.Series, code: str) -> bool:
        """Mean-reversion entry signal (skill 13).

        Entry conditions:
        1. RSI14 < 30 (oversold)
        2. close < bollinger lower band (price extended below range)
        3. volume contraction: vol_ratio < 1.0 (selling exhaustion)
           Exception: vol_ratio > 2.0 AND RSI14 < 20 → panic capitulation signal
        4. ADX < 20 (no strong trend — mean reversion works best in range)
        """
        if pd.isna(row.get('rsi14')) or pd.isna(row.get('bb_lower')):
            return False

        # Limit-down filter: don't buy if limit-down (can't execute)
        if 'pct_change' in row and not pd.isna(row['pct_change']):
            limit_pct = get_limit_pct(code)
            if row['pct_change'] <= -limit_pct * 100 * 0.99:
                return False  # 跌停封板，无法成交，待次日

        # Core conditions
        rsi_oversold = row['rsi14'] < 30
        below_bb_lower = row['close'] < row['bb_lower']

        # Volume condition: contraction or mild expansion (normal for A-share oversold bounces)
        # Exception: vol_ratio > 2.0 AND RSI14 < 20 → panic capitulation signal
        vol_ratio = row.get('vol_ratio', 0)
        vol_ok = vol_ratio < 1.5  # Allow mild expansion (matches skill 13 step 5: ≤1.5 is neutral/ok)
        panic_capitulation = vol_ratio > 2.0 and row['rsi14'] < 20
        vol_ok = vol_ok or panic_capitulation

        # ADX: no strong trend
        adx_ok = True
        if not pd.isna(row.get('adx14')):
            adx_ok = row['adx14'] < 20

        return rsi_oversold and below_bb_lower and vol_ok and adx_ok

    def _check_mean_reversion_exit(self, code: str, row: pd.Series, date) -> bool:
        """Mean-reversion exit signal (skill 13).

        Exit conditions (any triggers exit):
        1. price >= bb_mid (mean reversion target reached)
        2. RSI14 > 70 (overbought reversal)
        3. time stop: held >= 10 trading days without reverting
        4. stop loss: close < stop_loss_price (locked, never moves down)
        """
        pos = self.positions.get(code)
        if pos is None:
            return False

        # T+1 check: cannot sell on the same calendar day as entry
        if date.strftime('%Y-%m-%d') == pos['entry_date_for_t1']:
            return False

        # 1. Mean reversion target: price back to bb_mid → reduce 50% (half target reached)
        if not pd.isna(row.get('bb_mid')) and row['close'] >= row['bb_mid']:
            self._reduce(code, row['close'], date, 'mr_bb_mid_target', 0.5)
            # After reduce, position may be gone (100-share force_exit) — check before continuing
            if code not in self.positions:
                return True

        # 1b. Mean reversion complete: price >= bb_upper → full exit (beyond mean)
        if not pd.isna(row.get('bb_upper')) and row['close'] >= row['bb_upper']:
            self._exit(code, row['close'], date, 'mr_bb_upper_target')
            return True

        # 2. RSI overbought
        if not pd.isna(row.get('rsi14')) and row['rsi14'] > 70:
            self._exit(code, row['close'], date, 'mr_rsi_overbought')
            return True

        # 3. Time stop: ~10 trading days (use 14 calendar days to approximate)
        entry_date_dt = datetime.strptime(pos['entry_date_for_t1'], '%Y-%m-%d')
        hold_days = (date - entry_date_dt).days
        if hold_days >= 14:  # 14 calendar days ≈ 10 trading days
            self._exit(code, row['close'], date, 'mr_time_stop_10d')
            return True

        # 4. Stop loss (locked, never moves down)
        if row['close'] < pos['stop_loss']:
            self._exit(code, row['close'], date, 'mr_stop_loss')
            return True

        return False

    # ─────────────────────────────────────────────
    # Performance Analysis
    # ─────────────────────────────────────────────
    def _generate_report(self) -> dict:
        """Generate performance report."""
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df['date'] = pd.to_datetime(equity_df['date'])
        equity_df = equity_df.set_index('date')

        # ── Equity metrics ──
        final_equity = equity_df['equity'].iloc[-1]
        total_return = (final_equity / self.initial_capital - 1) * 100
        total_days = len(equity_df)
        annual_return = ((final_equity / self.initial_capital) ** (252 / total_days) - 1) * 100

        # Max drawdown
        equity_df['peak'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['peak'] - equity_df['equity']) / equity_df['peak']
        max_drawdown = equity_df['drawdown'].max() * 100

        # Sharpe ratio (risk-free rate = 3% annual)
        daily_returns = equity_df['equity'].pct_change().dropna()
        if len(daily_returns) > 1 and daily_returns.std() > 0:
            sharpe = (daily_returns.mean() * 252 - 0.03) / (daily_returns.std() * np.sqrt(252))
        else:
            sharpe = 0

        # Calmar ratio
        calmar = annual_return / max_drawdown if max_drawdown > 0 else 0

        # ── Trade metrics ──
        sell_trades = [t for t in self.trades if t['action'] in ('SELL', 'REDUCE')]
        wins = [t for t in sell_trades if t['pnl'] > 0]
        losses = [t for t in sell_trades if t['pnl'] < 0]

        win_rate = len(wins) / len(sell_trades) * 100 if sell_trades else 0
        avg_win = np.mean([t['pnl'] for t in wins]) if wins else 0
        avg_loss = abs(np.mean([t['pnl'] for t in losses])) if losses else 1
        profit_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0

        # ── Exit reason breakdown ──
        exit_reasons = defaultdict(int)
        for t in sell_trades:
            exit_reasons[t['reason']] += 1

        # ── Market exposure ──
        market_ok_days = equity_df['market_ok'].sum()
        market_exposure = market_ok_days / total_days * 100

        report = {
            'summary': {
                'initial_capital': self.initial_capital,
                'final_equity': round(final_equity, 2),
                'total_return_pct': round(total_return, 2),
                'annual_return_pct': round(annual_return, 2),
                'max_drawdown_pct': round(max_drawdown, 2),
                'sharpe_ratio': round(sharpe, 2),
                'calmar_ratio': round(calmar, 2),
                'total_trading_days': total_days,
                'market_exposure_pct': round(market_exposure, 2),
            },
            'trade_stats': {
                'total_trades': len(self.trades),
                'sell_trades': len(sell_trades),
                'win_rate_pct': round(win_rate, 2),
                'profit_loss_ratio': round(profit_loss_ratio, 2),
                'avg_win': round(avg_win, 2),
                'avg_loss': round(avg_loss, 2),
                'exit_reasons': dict(exit_reasons),
            },
            'equity_curve': self.equity_curve,
            'trades': self.trades,
        }
        return report


# ═══════════════════════════════════════════════════════════════
# Report Output
# ═══════════════════════════════════════════════════════════════
def print_report(report: dict):
    """Print performance summary to console."""
    s = report['summary']
    t = report['trade_stats']

    print("\n" + "=" * 70)
    print("  BACKTEST PERFORMANCE REPORT")
    print("=" * 70)
    print(f"  Initial Capital:     ¥{s['initial_capital']:>14,.0f}")
    print(f"  Final Equity:        ¥{s['final_equity']:>14,.2f}")
    print(f"  Total Return:         {s['total_return_pct']:>13.2f}%")
    print(f"  Annual Return:        {s['annual_return_pct']:>13.2f}%")
    print(f"  Max Drawdown:         {s['max_drawdown_pct']:>13.2f}%")
    print(f"  Sharpe Ratio:         {s['sharpe_ratio']:>13.2f}")
    print(f"  Calmar Ratio:         {s['calmar_ratio']:>13.2f}")
    print("-" * 70)
    print(f"  Total Trades:         {t['total_trades']:>13d}")
    print(f"  Sell/Reduce Trades:   {t['sell_trades']:>13d}")
    print(f"  Win Rate:             {t['win_rate_pct']:>13.2f}%")
    print(f"  Profit/Loss Ratio:    {t['profit_loss_ratio']:>13.2f}")
    print(f"  Avg Win:             ¥{t['avg_win']:>13.2f}")
    print(f"  Avg Loss:            ¥{t['avg_loss']:>13.2f}")
    print("-" * 70)
    print(f"  Trading Days:         {s['total_trading_days']:>13d}")
    print(f"  Market Exposure:      {s['market_exposure_pct']:>13.2f}%")
    print("-" * 70)
    print("  Exit Reasons:")
    for reason, count in sorted(t['exit_reasons'].items(), key=lambda x: -x[1]):
        print(f"    {reason:<25s} {count:>5d}")
    print("=" * 70)

    # ── Business standard assessment ──
    print("\n  BUSINESS STANDARD ASSESSMENT:")
    checks = [
        ("Annual Return > 15%", s['annual_return_pct'] > 15),
        ("Max Drawdown < 15%", s['max_drawdown_pct'] < 15),
        ("Sharpe Ratio > 1.0", s['sharpe_ratio'] > 1.0),
        ("Win Rate > 40%", t['win_rate_pct'] > 40),
        ("Profit/Loss Ratio > 2.0", t['profit_loss_ratio'] > 2.0),
        ("Calmar Ratio > 1.0", s['calmar_ratio'] > 1.0),
    ]
    for name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"    {status}  {name}")
    pass_count = sum(1 for _, p in checks if p)
    print(f"\n  Overall: {pass_count}/6 standards passed")
    print("=" * 70)


def save_report(report: dict, output_dir: str):
    """Save report to JSON and plot equity curve."""
    os.makedirs(output_dir, exist_ok=True)

    # Save JSON
    json_path = os.path.join(output_dir, 'backtest_report.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nReport saved to: {json_path}")

    # Plot equity curve
    equity_df = pd.DataFrame(report['equity_curve'])
    equity_df['date'] = pd.to_datetime(equity_df['date'])
    equity_df = equity_df.set_index('date')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[3, 1])

    # Equity curve
    ax1.plot(equity_df.index, equity_df['equity'], color='blue', linewidth=1)
    ax1.axhline(y=report['summary']['initial_capital'], color='gray',
                linestyle='--', alpha=0.5, label='Initial Capital')
    ax1.set_title('Equity Curve', fontsize=14)
    ax1.set_ylabel('Equity (¥)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Drawdown
    equity_df['peak'] = equity_df['equity'].cummax()
    equity_df['drawdown'] = (equity_df['peak'] - equity_df['equity']) / equity_df['peak'] * 100
    ax2.fill_between(equity_df.index, equity_df['drawdown'], 0, color='red', alpha=0.3)
    ax2.set_title('Drawdown (%)', fontsize=12)
    ax2.set_ylabel('Drawdown %')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    png_path = os.path.join(output_dir, 'backtest_equity_curve.png')
    plt.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Chart saved to: {png_path}")


# ═══════════════════════════════════════════════════════════════
# Main Entry
# ═══════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description='Stock Trading System Backtest')
    parser.add_argument('--stocks', nargs='*', default=None,
                        help='Stock codes (default: 10 representative stocks)')
    parser.add_argument('--start', default='20200101', help='Start date (YYYYMMDD)')
    parser.add_argument('--end', default='20251231', help='End date (YYYYMMDD)')
    parser.add_argument('--capital', type=int, default=INITIAL_CAPITAL,
                        help='Initial capital (default: 1000000)')
    args = parser.parse_args()

    # ── Build stock list ──
    industry_map = get_stock_list_by_industry()
    if args.stocks:
        stock_codes = args.stocks
    else:
        # Default: pick 1-2 from each industry = 10 representative stocks
        stock_codes = []
        for stocks in industry_map.values():
            stock_codes.extend(stocks[:1])  # 1 per industry

    # Build code -> industry mapping
    code_to_industry = {}
    for industry, codes in industry_map.items():
        for code in codes:
            code_to_industry[code] = industry

    print(f"Loading data for {len(stock_codes)} stocks...")
    print(f"Stock list: {stock_codes}")
    print()

    # ── Fetch data ──
    stock_data = {}
    for code in stock_codes:
        print(f"  Fetching {code}...", end=' ')
        df = get_stock_data(code, args.start, args.end)
        if not df.empty:
            stock_data[code] = df
            print(f"✅ {len(df)} rows")
        else:
            print("❌ failed")

    print(f"\nFetching index data (000001)...", end=' ')
    index_data = get_index_data("000001", args.start, args.end)
    print(f"✅ {len(index_data)} rows")

    if not stock_data or index_data.empty:
        print("ERROR: No data available for backtest")
        return

    # ── Run backtest ──
    engine = BacktestEngine(capital=args.capital)
    engine.industry_map = code_to_industry
    report = engine.run(stock_data, index_data)

    # ── Output ──
    print_report(report)
    output_dir = os.path.join(os.path.dirname(__file__), 'results')
    save_report(report, output_dir)


if __name__ == "__main__":
    main()
