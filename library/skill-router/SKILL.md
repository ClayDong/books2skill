---
name: skill-router
description: |
  当用户说"我该不该做X" / "怎么选Y" / "我的情况是Z" 等开放式决策问题时,作为总路由器自动按"价值观→哲学→操作→学科"4层调用相关 skill。
  这是藏经阁的核心入口,几乎所有决策问题都应该先调用本 skill。
source: cross-book (炒股的智慧 + 周易 + 大师兄)
tags: [meta, router, decision-support, cross-book]
related_skills: [ALL]
---

# 藏经阁决策路由器 (Library Skill Router)

## 触发条件

- "我该不该做 X"
- "我该怎么选 Y"
- "我遇到 Z 情况"
- "给我建议"
- 任何开放式决策/选择/评估问题

**总是先调用本 skill**, 它会路由到具体 skill。

---

## 第一步: 识别问题类型

### 类型 1: 投资类
- "我该不该买 X"
- "选哪只股票"
- "该不该止盈/止损"
- "市场崩了怎么办"

### 类型 2: 仓位/资金类
- "我应该买多少"
- "该不该加仓"
- "杠杆多少合适"
- "我还有子弹吗"

### 类型 3: 时机/趋势类
- "现在是买入时机吗"
- "该不该等"
- "这个趋势会持续吗"

### 类型 4: 长期决策类
- "我该不该换工作"
- "该不该创业"
- "该不该买房"
- "我该不该长期持有"

### 类型 5: 创业/事业类
- "我这个创业想法对吗"
- "该不该进新行业"
- "我该不该扩张"

### 类型 6: 危机/转折类
- "市场崩了"
- "我被套了"
- "我焦虑"
- "怎么办"

### 类型 7: 人生/价值观类
- "我为什么而活"
- "工作有什么意义"
- "我不开心"
- "做人该怎么做"

### 类型 8: 子女教育类
- "孩子该怎么教"
- "该不该让 X 学 Y"
- "怎么培养"

### 类型 9: 政策/经济类
- "经济形势如何"
- "国家政策怎么走"
- "该不该投政策方向"

---

## 第二步: 4 层路由

```
Layer 1 (价值观, 大师兄):
  - 几乎所有问题都应先看价值观
  - sweeper-monk (做人)
  - giving (意义)
  - long-termism (长期)

Layer 2 (哲学, 周易):
  - 重大决策/时机判断
  - i-ching-time-position (时位中正)
  - i-ching-life-cycle (阶段)
  - i-ching-advance-retreat (进退)
  - i-ching-crisis-transformation (危机)
  - i-ching-revolution-timing (革命)
  - i-ching-decision-omen (几微)

Layer 3 (操作, 炒股的智慧):
  - 投资的具体操作
  - stock-trend-judgment (趋势)
  - stock-entry-decision (入场)
  - stock-profit-taking-decision (止盈)
  - stock-stop-loss-decision (止损)
  - stock-position-sizing (仓位)
  - stock-bubble-participation (泡沫)
  - stock-psychology-check (心态)
  - stock-learning-stage (学习阶段)

Layer 4 (学科, 经济学原理):
  - 待 OCR 后补足
  - 经济周期, 风险管理, 行为金融等
```

---

## 第三步: 决策路径示例

### 路径 1: 投资选股

```
1. dashixiong-long-termism (长期视角)
2. dashixiong-cash-cow (现金奶牛)
3. dashixiong-cultural-investment (跨域类比)
4. i-ching-time-position (时位中正)
5. stock-trend-judgment (趋势)
6. stock-entry-decision (入场)
7. dashixiong-keep-one-bite (仓位)
```

### 路径 2: 创业决策

```
1. dashixiong-giving (意义)
2. dashixiong-sweeper-monk (态度)
3. dashixiong-long-termism (长期)
4. dashixiong-cash-cow (好生意?)
5. i-ching-life-cycle (阶段)
6. i-ching-time-position (时机)
7. dashixiong-keep-one-bite (留现金流)
```

### 路径 3: 职业换工作

```
1. dashixiong-long-termism (10 年视角)
2. i-ching-life-cycle (阶段)
3. dashixiong-sweeper-monk (态度)
4. dashixiong-giving (意义)
```

### 路径 4: 危机应对

```
1. dashixiong-keep-one-bite (留一口)
2. i-ching-crisis-transformation (危机转化)
3. stock-psychology-check (心态)
4. stock-bubble-participation (泡沫)
```

### 路径 5: 人生迷茫

```
1. dashixiong-giving (付出)
2. dashixiong-sweeper-monk (扫地僧)
3. dashixiong-long-termism (长期)
4. i-ching-life-cycle (阶段)
```

### 路径 6: 子女教育

```
1. dashixiong-cultural-investment (皇室培养)
2. dashixiong-long-termism (长期)
3. dashixiong-sweeper-monk (态度)
4. i-ching-life-cycle (阶段)
```

### 路径 7: 政策/经济

```
1. (待 OCR) 经济学原理
2. dashixiong-long-termism (长期)
3. dashixiong-cultural-investment (跨域)
4. i-ching-time-position (时机)
```

### 路径 8: 仓位管理

```
1. dashixiong-keep-one-bite (留一口)
2. stock-position-sizing (具体仓位)
3. dashixiong-long-termism (长期)
4. i-ching-advance-retreat (进退)
```

---

## 第四步: 整合输出

### 输出格式

```
【藏经阁决策报告】

问题: [用户的问题]

[Layer 1 - 价值观 (大师兄)]
  - dashixiong-X: [输出]
  - ...

[Layer 2 - 哲学 (周易)]
  - i-ching-X: [输出]
  - ...

[Layer 3 - 操作 (炒股的智慧)]
  - stock-X: [输出]
  - ...

[Layer 4 - 学科 (经济学原理)]
  - (待 OCR)

[综合建议]
  - 短期: ...
  - 中期: ...
  - 长期: ...

[风险提示]
  - ...

[行动清单]
  1. [ ] 行动 1
  2. [ ] 行动 2
  ...
```

### 冲突处理

如果不同层意见冲突:
1. 价值观 > 哲学 > 操作 (重大决策)
2. 操作 > 哲学 (投资操作)
3. 看 LIBRARY_OVERVIEW 的冲突清单

---

## 第五步: 持续支持

### 复盘
- 每周: 检查行动清单
- 每月: 复盘决策
- 季度: 重新评估长期判断

### 异常
- 重大事件: 重新跑决策路径
- 情绪异常: 调用 stock-psychology-check

---

## 路由速查表

| 用户问题关键词 | 优先 Layer | 优先 skill |
|---|---|---|
| "该不该 X" | 价值观 | dashixiong-long-termism |
| "选 Y" | 操作 | stock-trend-judgment |
| "时机" | 哲学 | i-ching-time-position |
| "我被套" | 操作 | stock-stop-loss-decision |
| "市场崩" | 哲学 | i-ching-crisis-transformation |
| "我迷茫" | 价值观 | dashixiong-giving |
| "做人" | 价值观 | dashixiong-sweeper-monk |
| "现金/仓位" | 操作 | dashixiong-keep-one-bite |
| "经济" | 学科 | (待 OCR) |
| "阶段" | 哲学 | i-ching-life-cycle |
| "孩子" | 价值观+操作 | dashixiong-cultural-investment |
| "进退" | 哲学 | i-ching-advance-retreat |

---

## 元数据

- **创建日期**: 2026-06-17
- **来源**: 跨书整合 (大师兄 + 周易 + 炒股的智慧)
- **方法**: 4 层决策支持 (价值观→哲学→操作→学科)
- **类型**: 元 skill (router)
- **状态**: 第 4 层待 OCR 后完善
