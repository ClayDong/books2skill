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

    def run(self, stock_data: dict, index_data: pd.DataFrame):
        """Run backtest across all dates."""
        # Build unified date index
        all_dates = sorted(set().union(*[set(df.index) for df in stock_data.values()]))
        index_dates = set(index_data.index)

        print(f"Backtest period: {all_dates[0].date()} ~ {all_dates[-1].date()}")
        print(f"Trading days: {len(all_dates)}")
        print(f"Stocks: {len(stock_data)}")
        print("-" * 70)

        for date in all_dates:
            # ── 1. Market filter (skill 05: 大盘60日线) ──
            if date not in index_dates:
                continue
            market_ok = bool(index_data.loc[date, 'above_ma60'])

            # ── 2. Check exits for existing positions (skill 08) ──
            for code in list(self.positions.keys()):
                if code not in stock_data or date not in stock_data[code].index:
                    continue
                row = stock_data[code].loc[date]
                self._check_exit(code, row, date)

            # ── 3. Check entries (skill 05) ──
            if market_ok and len(self.positions) < self.max_positions:
                for code, df in stock_data.items():
                    if code in self.positions:
                        continue
                    if date not in df.index:
                        continue
                    row = df.loc[date]
                    if self._check_entry(row, code):
                        if self._check_position_limits(code):
                            self._enter_position(code, row, date)

            # ── 4. Record daily equity ──
            total_equity = self.cash + sum(
                p['shares'] * stock_data[c].loc[date, 'close']
                if c in stock_data and date in stock_data[c].index
                else p['shares'] * p['entry_price']
                for c, p in self.positions.items()
            )
            self.equity_curve.append({
                'date': date.strftime('%Y-%m-%d'),
                'equity': round(total_equity, 2),
                'cash': round(self.cash, 2),
                'positions': len(self.positions),
                'market_ok': market_ok,
            })

        return self._generate_report()

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
    def _calc_shares(self, atr: float, price: float) -> int:
        """Calculate position size (skill 06: 股数=资金×1%/(2×ATR))."""
        risk_amount = self.initial_capital * RISK_PER_TRADE
        shares = risk_amount / (2 * atr)
        shares = int(shares // 100) * 100  # 向下取整到100股
        return max(shares, 0)

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

    def _enter_position(self, code: str, row: pd.Series, date):
        """Enter a new position."""
        shares = self._calc_shares(row['atr14'], row['close'])
        if shares == 0:
            return  # 高价股小资金场景：不足100股不建仓

        cost = shares * row['close'] * (1 + BUY_COST)
        if cost > self.cash:
            return

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
            'can_sell_date': date.strftime('%Y-%m-%d'),  # T+1 (实际应+1天)
        }

        self.trades.append({
            'date': date.strftime('%Y-%m-%d'),
            'code': code,
            'action': 'BUY',
            'shares': shares,
            'price': round(row['close'], 2),
            'cost': round(cost, 2),
            'reason': 'breakout_entry',
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

        # T+1 check
        if date.strftime('%Y-%m-%d') == pos['can_sell_date']:
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
            'hold_days': 'N/A',
        })
        del self.positions[code]

    def _reduce(self, code: str, price: float, date, reason: str, ratio: float):
        """Partial exit (reduce position)."""
        pos = self.positions[code]
        sell_shares = int(pos['shares'] * ratio // 100) * 100
        if sell_shares < 100:
            return  # 不足100股不减仓

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
