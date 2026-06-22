#!/usr/bin/env python3
"""
stock-trading-system 自动化校验脚本

解决"每次review都能发现新问题"的根因：把确定性检查从人工review变成机器校验。

用法：
    python validate_system.py              # 全部检查（13项）
    python validate_system.py --check ria  # 只检查某一项
    python validate_system.py --fix-hints  # 显示修复建议

可用检查项：ria test source count params ref desc contract
            rlen ocr related tpparam bt

退出码：0=全部通过，1=有错误，2=有警告但无错误
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
SKILL_DIRS = sorted([d for d in BASE.iterdir() if d.is_dir() and d.name[0].isdigit()])

errors = []
warnings = []


def err(check, target, msg):
    errors.append({"check": check, "target": target, "msg": msg})


def warn(check, target, msg):
    warnings.append({"check": check, "target": target, "msg": msg})


# ── 工具函数 ──

def parse_frontmatter(content):
    """简单YAML frontmatter解析（支持多行 | 和 > 格式）"""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    lines = match.group(1).split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if ':' in line and not line.startswith(' '):
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()
            # 多行格式: key: | 或 key: >
            if value in ('|', '>'):
                multiline = []
                i += 1
                while i < len(lines) and (lines[i].startswith('  ') or lines[i].strip() == ''):
                    multiline.append(lines[i].strip())
                    i += 1
                fm[key] = ' '.join(multiline)
                continue
            fm[key] = value
        i += 1
    return fm


def read_file(path):
    return Path(path).read_text(encoding='utf-8')


def read_skill(skill_dir):
    return read_file(skill_dir / "SKILL.md")


def read_test_prompts(skill_dir):
    tp = skill_dir / "test-prompts.json"
    if not tp.exists():
        return None
    return json.loads(tp.read_text(encoding='utf-8'))


def extract_books(text):
    """提取《》内的书名"""
    return set(re.findall(r'《(.+?)》', text))


# ── 检查1: RIA-TV++六段完整性 ──

def check_ria():
    required = ['## R —', '## I —', '## A1 —', '## A2 —', '## E —', '## B —']
    for d in SKILL_DIRS:
        content = read_skill(d)
        for seg in required:
            if seg not in content:
                err("RIA-TV++", d.name, f"缺少段落: {seg}")


# ── 检查2: test-prompts.json完整性 ──

def check_test_prompts():
    for d in SKILL_DIRS:
        tp = read_test_prompts(d)
        if tp is None:
            err("test-prompts", d.name, "test-prompts.json 不存在")
            continue
        cases = tp.get("test_cases", [])
        types = [c.get("type", "") for c in cases]
        st = types.count("should_trigger")
        snt = types.count("should_not_trigger")
        ec = types.count("edge_case")
        if st < 3:
            err("test-prompts", d.name, f"should_trigger 只有 {st} 条，需≥3")
        if snt < 2:
            err("test-prompts", d.name, f"should_not_trigger 只有 {snt} 条，需≥2")
        if ec < 1:
            warn("test-prompts", d.name, f"edge_case 只有 {ec} 条，建议≥1")


# ── 检查3: source_book一致性 + 无"训练数据"残留 ──

def check_source_book():
    # 从BOOK_OVERVIEW提取书籍-作者映射
    bo = read_file(BASE / "BOOK_OVERVIEW.md")
    bo_books = extract_books(bo)

    for d in SKILL_DIRS:
        content = read_skill(d)
        fm = parse_frontmatter(content)
        skill_sb = fm.get("source_book", "")

        tp = read_test_prompts(d)
        tp_sb = tp.get("source_book", "") if tp else ""

        # 检查"训练数据"残留
        if "训练数据" in skill_sb:
            err("source_book", d.name, f"SKILL.md source_book 含'训练数据': {skill_sb}")
        if "训练数据" in tp_sb:
            err("source_book", d.name, f"test-prompts.json source_book 含'训练数据': {tp_sb}")

        # 检查书名匹配（SKILL.md vs test-prompts.json）
        skill_books = extract_books(skill_sb)
        tp_books = extract_books(tp_sb)
        if skill_books and tp_books and skill_books != tp_books:
            err("source_book", d.name,
                f"书名不一致: SKILL.md={skill_books} vs test-prompts={tp_books}")


# ── 检查4: 书籍数量一致性 ──

def check_book_count():
    bo = read_file(BASE / "BOOK_OVERVIEW.md")
    idx = read_file(BASE / "INDEX.md")
    so = read_file(BASE / "SYSTEM_OVERVIEW.md")

    counts = {}
    for name, text in [("BOOK_OVERVIEW", bo), ("INDEX", idx), ("SYSTEM_OVERVIEW", so)]:
        m = re.search(r'(\d+)\s*本', text)
        counts[name] = m.group(1) if m else "?"

    unique = set(counts.values())
    if len(unique) > 1:
        err("书籍数量", "三文档", f"不一致: {counts}")

    # 检查BOOK_OVERVIEW的13 Skill架构表行数
    skill_table_match = re.search(r'## 13 Skill 架构.*?\n(\|.*?\|.*?\n)+', bo, re.DOTALL)
    if skill_table_match:
        table = skill_table_match.group(0)
        data_rows = [l for l in table.split('\n') if l.startswith('|') and '---' not in l and 'skill' not in l.lower()]
        if len(data_rows) != 13:
            err("书籍数量", "BOOK_OVERVIEW", f"13 Skill架构表有 {len(data_rows)} 行，应为13")


# ── 检查5: 08参数一致性（10日低点→20日低点） ──

def check_08_params():
    d = BASE / "08-trend-exit"
    if not d.exists():
        return
    content = read_skill(d)
    tp = read_test_prompts(d)

    # 禁用词：参数性用法（"10日低点出场"是规则，"10日低点太敏感"是B段比较说明，允许）
    forbidden_skill = ["10日低点出场", "10日最低价"]
    forbidden_test = ["10日低点", "10日最低"]  # test-prompts不应有任何旧参数残留

    for word in forbidden_skill:
        if word in content:
            err("08参数", "SKILL.md", f"含禁用词 '{word}'（应为'20日低点出场'）")
    if tp:
        tp_str = json.dumps(tp, ensure_ascii=False)
        for word in forbidden_test:
            if word in tp_str:
                err("08参数", "test-prompts.json", f"含禁用词 '{word}'（应为'20日低点'）")

    # 检查应包含的关键参数
    required_params = ["20日低点", "浮盈>30%回撤15%", "浮盈>50%回撤20%"]
    for param in required_params:
        if param not in content:
            err("08参数", "SKILL.md", f"缺少关键参数: {param}")


# ── 检查6: 引用完整性（INDEX引用图 vs 实际目录） ──

def check_references():
    idx = read_file(BASE / "INDEX.md")

    # 提取mermaid图中的skill节点
    mermaid_match = re.search(r'```mermaid\n(.*?)```', idx, re.DOTALL)
    if mermaid_match:
        graph = mermaid_match.group(1)
        nodes = re.findall(r'S\d+\[([^\]]+)\]', graph)
        existing_skills = {d.name for d in SKILL_DIRS}
        for node in nodes:
            if node not in existing_skills:
                err("引用完整性", "INDEX.md", f"mermaid图引用了不存在的skill: {node}")

    # 检查13自成闭环：13的SKILL.md说不委托07/08，但INDEX引用图不应有S13→S07/S08
    if mermaid_match and "S13 -->|" in mermaid_match.group(1):
        graph = mermaid_match.group(1)
        s13_edges = re.findall(r'S13\s*-->\|([^|]+)\|\s*S(\d+)', graph)
        for edge_label, target_num in s13_edges:
            if target_num in ["07", "08"]:
                err("引用完整性", "INDEX.md",
                    f"S13-->S{target_num}({edge_label})与13自成闭环矛盾（13不委托07/08）")


# ── 检查7: description非空 + trigger条件 ──

def check_description():
    for d in SKILL_DIRS:
        content = read_skill(d)
        fm = parse_frontmatter(content)
        desc = fm.get("description", "")
        if not desc or desc == "|":
            err("description", d.name, "description 为空")
        # 检查是否有关键trigger信号说明
        if "trigger" not in desc.lower() and "当用户" not in desc:
            warn("description", d.name, "description 未明确trigger条件")


# ── 检查8: 接口契约完整性（05/13互斥 + ATR传递链 + 13→06布林带止损） ──

def check_interface_contracts():
    # 05应有市场状态校验（与13互斥）
    s05 = read_skill(BASE / "05-breakout-entry")
    if "13-mean-reversion" not in s05 or "波动率分位" not in s05:
        err("接口契约", "05", "缺少与13的互斥逻辑（波动率分位判断）")

    # 07应接受05的自适应ATR
    s07 = read_skill(BASE / "07-atr-stop-loss")
    if "由05" not in s07 and "自适应ATR" not in s07:
        err("接口契约", "07", "未声明接受05的自适应ATR")

    # 06应接受05的自适应ATR + 13的布林带止损
    s06 = read_skill(BASE / "06-position-sizing")
    if "由05" not in s06 and "自适应ATR" not in s06:
        err("接口契约", "06", "未声明接受05的自适应ATR")
    if "布林带止损" not in s06 and "13" not in s06:
        err("接口契约", "06", "未声明接受13的布林带止损价")

    # 13应自带止损和出场（不委托07/08）
    s13 = read_skill(BASE / "13-mean-reversion")
    if "不委托 07/08" not in s13 and "不委托07/08" not in s13:
        err("接口契约", "13", "未声明'自带止损和出场，不委托07/08'")

    # 13步骤6应先定义止损价再调用06
    step6_match = re.search(r'6\.\s*\*\*入场信号输出\*\*.*?(?=\d\.\s*\*\*)', s13, re.DOTALL)
    if step6_match:
        step6 = step6_match.group(0)
        stop_loss_pos = step6.find("止损价")
        call_06_pos = step6.find("06-position-sizing")
        if stop_loss_pos > 0 and call_06_pos > 0 and stop_loss_pos > call_06_pos:
            err("接口契约", "13步骤6", "因果倒置：调用06在定义止损价之前")


# ── 检查9: R段引用长度校验（≤150字/段，CLAUDE.md红线第3条） ──

def check_r_quote_length():
    for d in SKILL_DIRS:
        content = read_skill(d)
        # 提取R段（## R — 到下一个 ## 或 --- 之间）
        r_match = re.search(r'## R —.*?(?=\n## |\n---\n)', content, re.DOTALL)
        if not r_match:
            continue
        r_section = r_match.group(0)
        # 提取所有 > "..." 引用文本
        quotes = re.findall(r'>\s*"([^"]+)"', r_section)
        for i, quote in enumerate(quotes, 1):
            # 计算字符数（去掉空白）
            clean = re.sub(r'\s+', '', quote)
            if len(clean) > 150:
                err("R段引用长度", d.name,
                    f"第{i}段引用 {len(clean)} 字，超过150字红线（CLAUDE.md第3条）")


# ── 检查10: R段OCR原文标注校验 ──

def check_r_ocr_annotation():
    # OCR修复的6本书（来自BOOK_OVERVIEW.md）
    ocr_books = {
        "海龟交易法则", "通向财务自由之路", "股市趋势技术分析",
        "日本蜡烛图技术", "交易心理分析", "笑傲股市"
    }
    for d in SKILL_DIRS:
        content = read_skill(d)
        r_match = re.search(r'## R —.*?(?=\n## |\n---\n)', content, re.DOTALL)
        if not r_match:
            continue
        r_section = r_match.group(0)
        # 提取R段引用的书名
        r_books = set(re.findall(r'《(.+?)》', r_section))
        # 如果引用了OCR修复的书，检查是否有"OCR原文"标注
        for book in r_books:
            if book in ocr_books:
                if "OCR原文" not in r_section and "OCR 原文" not in r_section:
                    err("R段OCR标注", d.name,
                        f"R段引用了OCR修复的《{book}》，但未标注'OCR原文'")


# ── 检查11: related_skills双向一致性 ──

def check_related_skills_bidirectional():
    # 先收集所有skill的related_skills
    all_related = {}
    for d in SKILL_DIRS:
        content = read_skill(d)
        fm = parse_frontmatter(content)
        rs = fm.get("related_skills", "")
        # 解析 [a, b, c] 格式
        rs_match = re.match(r'\[(.+)\]', rs)
        if rs_match:
            skills = [s.strip() for s in rs_match.group(1).split(',')]
            all_related[d.name] = skills
        else:
            all_related[d.name] = []

    # 检查双向一致性
    for skill, related in all_related.items():
        for target in related:
            if target not in all_related:
                err("related_skills", skill,
                    f"related_skills引用了不存在的skill: {target}")
                continue
            # 检查反向引用
            if skill not in all_related[target]:
                warn("related_skills", skill,
                    f"related_skills有{target}，但{target}的related_skills没有{skill}（单向引用）")


# ── 检查12: test-prompts expected_behavior与SKILL.md关键参数一致性（启发式） ──

def check_test_prompt_params():
    # 08的关键参数词（从SKILL.md提取，检查test-prompts是否同步）
    s08 = BASE / "08-trend-exit"
    if not s08.exists():
        return
    content = read_skill(s08)
    tp = read_test_prompts(s08)
    if not tp:
        return

    # 08应包含的关键参数（在expected_behavior中应能找到对应描述）
    key_params = {
        "20日低点": ["20日低", "20日最低"],
        "浮盈>30%回撤15%": ["浮盈.*30%", "回撤.*15%"],
        "浮盈>50%回撤20%": ["浮盈.*50%", "回撤.*20%"],
    }
    tp_str = json.dumps(tp, ensure_ascii=False)
    for param, patterns in key_params.items():
        found = any(re.search(p, tp_str) for p in patterns)
        if not found:
            err("test参数一致性", "08 test-prompts.json",
                f"expected_behavior中未找到关键参数 '{param}' 的描述")


# ── 检查13: 回测参数与SKILL.md参数一致性 ──

def check_backtest_params():
    bt = BASE / "backtest" / "backtest.py"
    if not bt.exists():
        return
    bt_content = read_file(bt)
    s08 = read_skill(BASE / "08-trend-exit")

    # 检查1: backtest.py用low_20d，SKILL.md说20日低点
    if "low_20d" in bt_content and "20日低点" not in s08:
        err("回测参数", "08 vs backtest.py",
            "backtest.py用low_20d，但08 SKILL.md未提及'20日低点'")
    # 反向：如果backtest.py还有low_10d，说明旧参数残留
    if "low_10d" in bt_content and "low_10d" in bt_content:
        # 检查low_10d是否还在出场逻辑中使用（非注释行）
        for line in bt_content.split('\n'):
            stripped = line.strip()
            if 'low_10d' in stripped and not stripped.startswith('#'):
                # 如果low_10d出现在出场判断中（非计算列），报错
                if 'close' in stripped and 'low_10d' in stripped:
                    err("回测参数", "backtest.py",
                        f"backtest.py仍在出场逻辑中使用low_10d: {stripped}")
                    break

    # 检查2: backtest.py的浮盈回撤参数应与SKILL.md一致
    # backtest.py: max_profit > 0.5 and drawback >= 0.20 → 浮盈>50%回撤20%
    # backtest.py: max_profit > 0.3 and drawback >= 0.15 → 浮盈>30%回撤15%
    bt_has_50_20 = bool(re.search(r'max_profit\s*>\s*0\.5.*drawback\s*>=\s*0\.20', bt_content, re.DOTALL))
    bt_has_30_15 = bool(re.search(r'max_profit\s*>\s*0\.3.*drawback\s*>=\s*0\.15', bt_content, re.DOTALL))
    skill_has_50_20 = "浮盈>50%回撤20%" in s08
    skill_has_30_15 = "浮盈>30%回撤15%" in s08

    if bt_has_50_20 != skill_has_50_20:
        err("回测参数", "08 vs backtest.py",
            f"浮盈>50%回撤20%: backtest.py={bt_has_50_20}, SKILL.md={skill_has_50_20}")
    if bt_has_30_15 != skill_has_30_15:
        err("回测参数", "08 vs backtest.py",
            f"浮盈>30%回撤15%: backtest.py={bt_has_30_15}, SKILL.md={skill_has_30_15}")


# ── 主函数 ──

def main():
    only_check = None
    if "--check" in sys.argv:
        idx = sys.argv.index("--check")
        if idx + 1 < len(sys.argv):
            only_check = sys.argv[idx + 1]

    show_hints = "--fix-hints" in sys.argv

    all_checks = [
        ("ria", "RIA-TV++六段完整性", check_ria),
        ("test", "test-prompts.json完整性", check_test_prompts),
        ("source", "source_book一致性 + 无训练数据残留", check_source_book),
        ("count", "书籍数量一致性", check_book_count),
        ("params", "08参数一致性", check_08_params),
        ("ref", "引用完整性", check_references),
        ("desc", "description非空 + trigger条件", check_description),
        ("contract", "接口契约完整性", check_interface_contracts),
        ("rlen", "R段引用长度≤150字", check_r_quote_length),
        ("ocr", "R段OCR原文标注", check_r_ocr_annotation),
        ("related", "related_skills双向一致性", check_related_skills_bidirectional),
        ("tpparam", "test-prompts参数一致性", check_test_prompt_params),
        ("bt", "回测参数与SKILL.md一致性", check_backtest_params),
    ]

    print("=" * 60)
    print("stock-trading-system 自动化校验")
    print("=" * 60)

    for key, name, func in all_checks:
        if only_check and only_check != key:
            continue
        print(f"\n--- {name} ---")
        func()
        print(f"  完成")

    print("\n" + "=" * 60)
    total = len([c for c in all_checks if not only_check or c[0] == only_check])
    print(f"汇总: {total}项检查, {len(errors)}错误, {len(warnings)}警告")

    if errors:
        print("\n错误:")
        for e in errors:
            print(f"  ❌ [{e['check']}] {e['target']}: {e['msg']}")
            if show_hints:
                print(f"     修复: 参考 CLAUDE.md 变更影响清单，同步检查相关文件")

    if warnings:
        print("\n警告:")
        for w in warnings:
            print(f"  ⚠️ [{w['check']}] {w['target']}: {w['msg']}")

    if not errors and not warnings:
        print("\n✅ 全部通过")
    elif not errors:
        print("\n✅ 无错误（有警告）")

    print("=" * 60)

    sys.exit(1 if errors else (2 if warnings else 0))


if __name__ == "__main__":
    main()
