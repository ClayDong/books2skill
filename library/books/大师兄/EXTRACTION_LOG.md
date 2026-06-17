# 大师兄 EXTRACTION_LOG

> 完整的从阶段 0 到阶段 4 的过程记录

---

## 阶段 0 — BOOK_OVERVIEW

**输入**: 大师兄多场讲座口述稿

**方法**: 改编的 Adler 四步法(适用于口述/讲座)

| Adler 维度 | 改编后的做法 |
|---|---|
| 结构分析 | 主题域分析(无章节) |
| 解释学分析 | 核心世界观提取 |
| 批判性分析 | 独特性 vs 重合度 |
| 适用性分析 | 7 个 skill 候选 |

**输出**:
- d:\常用脚本\skills\cangjie-skill\library\books\大师兄\BOOK_OVERVIEW.md
- 识别 10 个主题域
- 识别 7 个潜在 skill

**关键挑战**:
- 口述内容无章节结构,需主题域重组
- 同一观点多次重复,需"合并"提取
- 东方文化背景需要本地化解释

---

## 阶段 1 — 6 候选文件

| 候选文件 | 数量 | 关键内容 |
|---|---|---|
| frameworks.md | 10 | 长期主义三圈/现金奶牛四要素/留一口/垂直制造/文化投资类比/付出循环/火象星座/扫地僧/表外风险/财富三分 |
| principles.md | 15 | 未来十年/留一口/反杠杆/扫地僧/付出/长期/文化/现金为王/反投机/垂直制造/火象/留余地/历史押韵/跨域/持续学习 |
| cases.md | 12 | 巴菲特解散基金/AI 板块/朱棣/特斯拉/亚马逊/微软/Google/Meta/郑和/麦哲伦/次贷/雷曼 |
| counter-examples.md | 8 | 满仓被套/杠杆爆仓/表外风险/索取的痛苦/过度牺牲/亢龙有悔/张扬失败/不担当 |
| decisions.md | 12 | 长期持有/换工作/创业/读MBA/子女教育/止盈/危机应对/创业资金/选股/选企业/资产配置/估值 |
| glossary.md | 12 | 现金奶牛/留一口/扫地僧/长期主义/付出/火象星座/垂直制造/贸易型/征服型/表外表内/扫地僧境界/留余地 |

**总候选: 69 个**

---

## 阶段 1.5 — 三重验证

**方法**:
- V1 跨域: 与现代管理/投资/心理学概念对应
- V2 预测力: 是否能预测决策结果
- V3 独特性: 与已有 skill 的差异化

**输出**:
- d:\常用脚本\skills\cangjie-skill\library\books\大师兄\verified.md
- d:\常用脚本\skills\cangjie-skill\library\books\大师兄\rejected.md

**结果**:
| 类型 | 候选 | 通过 | 通过率 |
|---|---|---|---|
| framework | 10 | 9 | 90% |
| principle | 15 | 14 | 93% |
| case | 12 | 12 | 100% |
| counter-example | 8 | 8 | 100% |
| decision | 12 | 12 | 100% |
| glossary | 12 | 12 | 100% |
| **总计** | **69** | **67** | **97%** |

**拒绝的 2 个**:
- f09 表外-表内风险模型 (与现代金融框架重合)
- p08 现金为王 (投资常识,无独特性)

**通过率极高的原因**:
1. 大师兄内容经过反复讲述,核心观点精炼
2. 抽取器已按"现代可操作+独特"标准筛选
3. 大师兄的"价值观"层(非操作层)与现代投资书的重合度反而低

---

## 阶段 2 — 6 核心 skill 构造

| Skill | 核心unit | RIA++ 完成度 |
|---|---|---|
| dashixiong-long-termism | f01 + p01 + p06 + 12 个 case | 100% |
| dashixiong-keep-one-bite | f03 + p02 + p12 + p03 + 8 个反例 | 100% |
| dashixiong-cash-cow | f02 + f10 + 4 个 case | 100% |
| dashixiong-cultural-investment | f05 + p07 + p13 + 4 个 case | 100% |
| dashixiong-sweeper-monk | f08 + p04 + p11 + 4 个 case | 100% |
| dashixiong-giving | f06 + p05 + 4 个 case | 100% |

每个 skill 包含:
- R 原文 (Reading)
- I 方法论骨架 (Interpretation)
- A1 书中的应用 (Past Application)
- A2 触发场景 (Trigger Scenarios)
- E 执行 (Execution)
- B 边界 (Boundary)
- 元数据

**平均每个 skill 长度: ~600 行**

---

## 阶段 3 — 跨书链接

**与周易 6 个 skill 的链接**:
- dashixiong-long-termism → i-ching-life-cycle (人生阶段 + 长期主义)
- dashixiong-long-termism → i-ching-advance-retreat (长期 + 进退)
- dashixiong-keep-one-bite → i-ching-advance-retreat (留一口 + 进退)
- dashixiong-cultural-investment → i-ching-time-position (跨域 + 时位)
- dashixiong-cultural-investment → i-ching-life-cycle (跨域 + 阶段)
- dashixiong-cultural-investment → i-ching-revolution-timing (大航海 + 革命时机)
- dashixiong-sweeper-monk → i-ching-life-cycle (扫地僧 + 阶段)
- dashixiong-sweeper-monk → i-ching-advance-retreat (扫地僧 + 进退)
- dashixiong-giving → i-ching-life-cycle (付出 + 阶段)
- dashixiong-giving → i-ching-crisis-transformation (付出 + 危机)

**与炒股的智慧 8 个 skill 的链接**:
- dashixiong-long-termism → stock-psychology-check (长期 + 心态)
- dashixiong-keep-one-bite → stock-position-sizing (留一口 + 仓位)
- dashixiong-keep-one-bite → stock-stop-loss-decision (留一口 + 止损)
- dashixiong-cash-cow → stock-trend-judgment (现金奶牛 + 趋势)
- dashixiong-cash-cow → stock-entry-decision (现金奶牛 + 入场)
- dashixiong-cash-cow → stock-profit-taking-decision (现金奶牛 + 止盈)
- dashixiong-cash-cow → stock-bubble-participation (现金奶牛 + 泡沫)

**与未来经济学原理 skill 的链接(预留)**:
- dashixiong-long-termism → 长周期经济学
- dashixiong-keep-one-bite → 风险管理
- dashixiong-cash-cow → 自由现金流
- dashixiong-cultural-investment → 制度经济学/历史类比

---

## 阶段 4 — 压力测试

| Skill | 测试场景 | 通过率 |
|---|---|---|
| long-termism | 7 个场景 | 100% |
| keep-one-bite | 7 个场景 | 100% |
| cash-cow | 7 个场景 | 100% |
| cultural-investment | 7 个场景 | 100% |
| sweeper-monk | 6 个场景 | 100% |
| giving | 6 个场景 | 100% |
| **总计** | **40 个场景** | **100%** |

**关键测试点**:
1. 大师兄语境的"留一口"能否转化为可操作建议
2. 长期主义三圈模型能否在 A 股/美股/创业场景下工作
3. 现金奶牛四要素能否在 AI 板块识别
4. 文化类比是否合理 (避免牵强类比)
5. 扫地僧境界是否平衡 (避免过度低调)
6. 付出哲学是否避免"伪付出"陷阱

**改进建议**:
- cash-cow 应增加"周期性行业"判断
- cultural-investment 应增加"类比过度"的警告
- sweeper-monk 应增加"需要张扬的场景"例外
- giving 应增加"被利用"的边界

---

## 关键学习

### 1. 口述内容的处理方法

**挑战**: 没有章节,同一观点多次重复

**方法**:
- 主题域重组(按观点而非时间)
- 重复观点合并,保留最经典表达
- 引用原文保持"大师兄"风格

### 2. 价值观层 vs 操作层

**挑战**: 大师兄内容多在"价值观"层,操作层较少

**方法**:
- 价值观层直接形成 skill (sweeper-monk, giving)
- 操作层补足 (cash-cow, keep-one-bite 的操作步骤)
- 与周易/炒股/经济学互补

### 3. 与现代概念的对应

**挑战**: 大师兄的"火象星座"等表述,如何与现代概念对应?

**方法**:
- 表格对比 (传统 vs 现代)
- 取共同点 + 差异点
- 不强行套用现代框架

### 4. 跨书链接

**关键洞察**:
- 大师兄 sweeper-monk + giving 是周易/炒股/经济学都不覆盖的
- 这是大师兄的**独特价值**
- 应该重点发挥

---

## 元数据

- **创建日期**: 2026-06-17
- **输入**: 大师兄多场讲座口述稿
- **方法**: 改编的 Adler 四步法 + RIA-TV++ + Zettelkasten 链接
- **输出**: 6 个核心 skill, 67 个验证通过的 unit, 40 个压力测试场景
- **总耗时**: 约 2 小时 (含对话)
- **通过率**: 97% (69 候选 → 67 通过)
- **跨书链接**: 与周易 10 个,与炒股 7 个
