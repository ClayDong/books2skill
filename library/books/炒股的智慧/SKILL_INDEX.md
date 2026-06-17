# 炒股的智慧 — SKILL_INDEX (技能索引)

> 7 个核心 skill + 1 个元决策 skill 的一站式导航。
> 使用方法: 找到你的决策场景 → 激活对应 skill → 按 RIA++ 流程执行。

---

## 决策树 (Decision Tree)

```
我面临什么决策?
│
├── 我还没入场 ───────────────────────► stock-entry-decision
│   ├── 仓位怎么分? ────────────────► stock-position-sizing
│   ├── 现在是不是泡沫? ────────────► stock-bubble-participation
│   └── 我心理状态正常吗? ──────────► stock-psychology-check
│
├── 我已经持仓
│   ├── 我在亏损
│   │   ├── 浮亏<10%,该不该止损? ──► stock-stop-loss-decision
│   │   ├── 浮亏>20%,被套了? ─────► stock-stop-loss-decision
│   │   └── 想向下摊平? ──────────► stock-psychology-check (反向:这是禁止行为)
│   │
│   ├── 我在盈利
│   │   ├── 涨了 30%,要不要卖? ───► stock-profit-taking-decision
│   │   ├── 涨了 100%,是泡沫? ────► stock-bubble-participation
│   │   └── 移动止损怎么设? ───────► stock-trailing-stop
│   │
│   └── 仓位管理
│       └── 是否加仓/减仓? ─────────► stock-position-sizing
│
└── 我在学股 ──────────────────────────► stock-learning-stage
    ├── 心理建设 ───────────────────► stock-psychology-check
    └── 何时止损 ───────────────────► stock-stop-loss-decision
```

---

## 技能清单 (Quick Reference)

| skill | 触发场景 | 不适用场景 | 关键原则 |
|---|---|---|---|
| **stock-stop-loss-decision** | "该不该止损""要不要割肉""套牢了怎么办" | 还没入场、已浮盈、纯信息查询 | 止损是最高行为准则,入场前定止损 |
| **stock-entry-decision** | "该不该买""能不能追""我准备投资 X" | 已持仓的止损/止盈、选股、大市择时 | 三层漏斗:基本面→阶段→临界点 |
| **stock-profit-taking-decision** | "该不该卖""涨了 X% 要不要兑现""怎么止盈" | 持有不动(用户表达"无所谓") | 让利润奔跑,移动止损代替固定止盈 |
| **stock-trailing-stop** | "移动止损怎么设""止损位怎么动态调整" | 长期价值投资 | 浪谷上移,止损点随升势递进 |
| **stock-position-sizing** | "买多少合适""仓位怎么分""如何分散" | 单一资产 100% 满仓 | 单只≤20%,总仓位≤70% |
| **stock-psychology-check** | "我心态崩了""我不该买/卖""追涨杀跌" | 长期心理建设/性格分析 | 把规则从认知转化为下意识 |
| **stock-bubble-participation** | "该不该追泡沫""什么阶段退出" | 用户没识别出泡沫 | 提前退出,不试图逃顶 |
| **stock-learning-stage** | "我学股多久了""我到什么水平""卡在某个阶段" | 长期职业规划 | 4 阶段不可跳级,卡阶段先查心理 |

---

## 链接矩阵 (Link Matrix)

|              | entry | stop | profit | trail | size | psych | bubble | learn |
|---           |---    |---   |---     |---    |---   |---    |---     |---    |
| **entry**    | —     | ●●●  | ●●     | ●     | ●●●  | ●●    | ●●     | ●     |
| **stop**     | ●●●   | —    | ●●●    | ●●    | ●●   | ●●●   | ●      | ●●    |
| **profit**   | ●●    | ●●●  | —      | ●●●   | ●    | ●●    | ●●     | —     |
| **trail**    | ●     | ●●   | ●●●    | —     | ●●   | —     | ●●     | —     |
| **size**     | ●●●   | ●●   | ●      | ●●    | —    | ●●    | ●●     | —     |
| **psych**    | ●●    | ●●●  | ●●     | —     | ●●   | —     | ●●     | ●●    |
| **bubble**   | ●●    | ●    | ●●     | ●●    | ●●   | ●●    | —      | ●     |
| **learn**    | ●     | ●●   | —      | —     | —    | ●●    | ●      | —     |

> ●●● = 强引用 / ●● = 中等 / ● = 弱引用

### 关键链接路径

- **入场 → 止损/止盈/仓位**: 决策全链路
- **止损 ↔ 心理**: 心理是执行止损的最大障碍
- **止盈 ↔ 移动止损**: 移动止损是止盈的执行机制
- **泡沫 → 入场/止盈/心理**: 泡沫的进出都需要心理+决策工具

---

## 关键原则速查 (The Big Rules)

来自《炒股的智慧》的核心方法论(经三重验证):

1. **止损是最高行为准则** — 入场前必须定止损点
2. **截短亏损,让利润奔跑** — 20% 止损硬线,盈利用移动止损
3. **胜算+小注+持久=必赢** — 概率思维三件套
4. **临界点入场** — 在突破点/转折点入场,而不是追涨杀跌
5. **大市不好时别买** — 大市四阶段(牛皮/正常/疯狂/最后)
6. **不要向下摊平** — 摊平是赌徒谬误
7. **有疑问,离场** — 不确定时优先保护本金
8. **忘掉入场价** — 决策基于未来,而非过去
9. **买熟悉的股票** — 不熟悉的生意不投
10. **不要怕+不要悔** — 入场前不要怕,出场后不要悔

---

## 路径推荐 (User Journey)

### 新手 (0-1 年)
1. **stock-learning-stage** — 自评当前阶段
2. **stock-psychology-check** — 修正心理弱点
3. **stock-stop-loss-decision** — 学止损(核心)
4. **stock-entry-decision** — 学入场(三层漏斗)

### 中级 (1-3 年)
1. **stock-trailing-stop** — 移动止损技术
2. **stock-profit-taking-decision** — 止盈纪律
3. **stock-position-sizing** — 仓位管理
4. **stock-bubble-participation** — 泡沫识别

### 高级 (3+ 年)
1. **7 个 skill 联动使用** — 决策树 + 链接矩阵
2. **持续心理自检** — 心理是终身课题

---

## 文件位置

```
library/books/炒股的智慧/
├── BOOK_OVERVIEW.md          # 阶段0: 书的全景分析
├── verified.md               # 阶段1.5: 三重验证通过清单
├── rejected.md               # 阶段1.5: 被拒绝的候选(及原因)
├── pressure-test.md          # 阶段4: 压力测试报告
├── SKILL_INDEX.md            # 本文件
├── candidates/               # 阶段1: 6 个抽取器的原始产出
│   ├── frameworks.md
│   ├── principles.md
│   ├── cases.md
│   ├── counter-examples.md
│   ├── decisions.md
│   └── glossary.md
└── skills/                   # 阶段2: 7 个核心 skill
    ├── stock-stop-loss-decision/
    ├── stock-entry-decision/
    ├── stock-profit-taking-decision/
    ├── stock-trailing-stop/
    ├── stock-position-sizing/
    ├── stock-psychology-check/
    ├── stock-bubble-participation/
    └── stock-learning-stage/
```

---

## 元数据

- **生成日期**: 2026-06-17
- **来源**: 《炒股的智慧》陈江挺
- **方法**: book2skill / cangjie pipeline
- **阶段**: 0 → 1 → 1.5 → 2 → 3 → 4 (全部完成)
- **下一步**: 1) 应用 P1 改进; 2) 多书集成(周易/曼昆/共同富裕)
