# 炒股的智慧 — 阶段1.5 拒绝清单

> 未通过V1/V2/V3三重验证,降级为example/引用/术语,不独立成skill。
> 必须写明不通过的是哪一项、原因是什么(审计价值)。

## framework

### f04 — 大势优先框架
```yaml
id: f04
title: 大势优先框架
V1: 通过
  - 第二章"技术分析之大市" + 第四章"临界点" + 第八章"学股"
V2: 通过
  - 能推出"熊市宁可不买"等具体判断
V3: **不通过**
  why_not_common: "自上而下"分析是基本投资常识,作者无新意。属于"有道理但无独特性"。
  degradation: 合并到 p15 "大市不好时别买任何股票",作为其执行细节
```

### f09 — 临界点买股三层过滤模型
```yaml
id: f09
title: 临界点买股三层过滤模型
V1: 通过
  - 第四章具体描述
V2: 临界通过
  - 能描述"基础-技术-时机"三层过滤
V3: **不通过**
  why_not_common: 这是"基础+技术+时机"分析的常识组合,作者未提供新视角
  degradation: 合并到 f01 "临界点决策模型"和d01 "入场决策",不独立
```

## principle

### p05 — 分散风险五到十只
```yaml
id: p05
title: 分散风险五到十只
V1: 通过
  - 第五章"家训"
V2: 通过
  - 能推出"每笔1:3+分散5-10只"的规则
V3: **不通过**
  why_not_common: "分散投资"是金融学ABC,5-10只这个数字也无独特性
  degradation: 合并到 p07 "避免买太多股票",作为其反向条件
```

### p08 — 别频繁交易
```yaml
id: p08
title: 别频繁交易
V1: 通过
  - 第五章 + 第六章
V2: 通过
  - 能解释"手续费+情绪"双重损失
V3: **不通过**
  why_not_common: "减少交易"是基本投资智慧,非独特视角
  degradation: 合并到 ce01 "频繁交易导致的失败模式",作为反例的具体化
```

### p12 — 不要试图寻找最高点
```yaml
id: p12
title: 不要试图寻找最高点
V1: 通过
  - 第四章
V2: 通过
  - 能解释"中间一截"策略
V3: **不通过**
  why_not_common: "不要追求精确顶底"是技术分析常识
  degradation: 合并到 f05 "移动止损加码法"和 d03 "止盈决策",作为其前提
```

### p16 — 看得见的指标才重要
```yaml
id: p16
title: 看得见的指标才重要
V1: **不通过**
  why: 这是作者对技术分析工具的边界讨论,书中只在一处提及,未形成独立框架
  degradation: 写入"技术分析边界"小节作为引用,不独立成 principle
```

## case (多数降级为 example, 5条保留)

### c03 — 36注赌博故事
```yaml
id: c03
title: 36注赌博
V1: 通过
  - 引子 + 第三章(双用)
V2: 通过
  - 能说明"集中下注+运气"的边界
V3: **临界 - 决定降级**
  why_not_common: 36注故事作为单次案例很好,但其方法论贡献已并入 f02 "概率思维"
  degradation: 保留为 f02 框架的 example,不独立
```

### c04 — 小偷教子
```yaml
id: c04
title: 小偷教子
V1: 通过
  - 引子 + 第六章
V2: 通过
  - 能说明"止损=逃命能力"
V3: 临界
  why_not_common: 偷窃故事有文化争议,不是所有skill用户都适合
  degradation: 保留为 p01 止损原则的 example,但用"年轻人三字"(c02)替代主例
```

### c05 — 抛硬币画走势图
```yaml
id: c05
title: 抛硬币画走势图
V1: 通过
  - 第二章
V2: 通过
  - 能说明"模式幻觉"
V3: **不通过**
  why_not_common: 这是反技术分析极端派,作者不是这立场
  degradation: 合并到 ce01 频繁交易(作为"过度技术分析"反例),或作为"技术分析边界"小节引用
```

### c06 — 巴菲特1969逃离
```yaml
id: c06
title: 巴菲特1969逃离
V1: 通过
  - 第五章
V2: 通过
  - 能说明"能力圈"原则
V3: **不通过**
  why_not_common: 巴菲特案例已被反复引用,无新意
  degradation: 合并到 p06 "有疑问离场",作为该原则的例证
```

### c07 — 索罗斯买银行股
```yaml
id: c07
title: 索罗斯买银行股
V1: 通过
  - 第五章
V2: 通过
  - 能说明"市场错误识别"
V3: **不通过**
  why_not_common: 索罗斯案例是金融常识
  degradation: 合并到 f07 "假象参与退出框架"作为 example
```

### c08 — 巴鲁克破产再起
```yaml
id: c08
title: 巴鲁克破产再起
V1: 通过
  - 第六章 + 第八章
V2: 通过
  - 能说明"体验风险阶段"
V3: **不通过**
  why_not_common: 5-6年学股的故事是典型鸡汤
  degradation: 合并到 f08 "学股四阶段模型"的 case 段
```

### c10-c13 — 历史泡沫案例(南海/佛罗里达/科威特/永生)
```yaml
V1: 通过(各案例都有内部描述)
V2: 通过(能说明泡沫模式)
V3: **不通过**
  why_not_common: 泡沫案例在所有投资书里都反复出现
  degradation: 合并到 f07 "假象参与退出框架"的 case 段,不独立
```

### c14 — 巴林银行
```yaml
id: c14
title: 巴林银行破产
V1: 通过
  - 第五章
V2: 通过
  - 能说明"向下摊平的毁灭性"
V3: **临界**
  why_not_common: 经典案例,有保留价值
  degradation: **保留为 ce02 "向下摊平"反例的主例**
```

### c15 — 上海石化
```yaml
id: c15
title: 上海石化1997
V1: 通过
  - 第五章
V2: 通过
  - 能说明"套牢时间不可预测"
V3: **不通过**
  why_not_common: 与c14重复
  degradation: 合并到 ce02 "向下摊平"反例
```

### c16 — 王安电脑
```yaml
id: c16
title: 王安电脑
V1: 通过
  - 第二章 + 第四章 + 第八章(三处引用)
V2: 通过
  - 能说明"绩优股也会消亡"
V3: 通过
  why_not_common: 中国/华人文化中的具体案例,有保留价值
  degradation: **保留为 example,在 p11 "股市从来不会错"和"长线持有风险"中作为反例**
```

### c17-c20 — 微软/王安/麦当劳/新态(盈利增长案例)
```yaml
V1: 通过
V2: 通过(能说明盈利加速增长)
V3: **不通过**
  why_not_common: 这些是"高增长公司"的典型案例,在所有投资书出现
  degradation: 合并到"基础分析"案例段,不独立
```

## counter-example (5条保留,其余降级为Boundary素材)

### ce01, ce02 — 频繁交易+向下摊平
**保留** 为 boundary 核心素材,分别对应 p08 和 p09 的失败模式

### ce05 — 过度自信
```yaml
V3: **不通过**
  why_not_common: "聪明人反而失败"是常见鸡汤,作者无新视角
  degradation: 合并到 p07 "避免买太多股票"的失败模式
```

### ce06 — 规则流于形式
```yaml
V3: **不通过**
  why_not_common: "形式主义"是组织行为学常识
  degradation: 合并到 f06 "心理训练三步法",作为其反面
```

### ce07 — 表层模仿
```yaml
V3: **不通过**
  why_not_common: "幸存者偏差"是行为金融学常识
  degradation: 合并到 f08 "学股四阶段模型"作为警示
```

### ce09 — 忽视系统性风险
```yaml
V3: **不通过**
  why_not_common: "自上而下"是基本投资常识
  degradation: 合并到 p15 "大市不好时别买"
```

### ce11 — 跟随大流高位接盘
```yaml
V3: **不通过**
  why_not_common: "FOMO"是投资心理学常识
  degradation: 合并到 p15 反面
```

### ce12 — 报复性加倍下注
```yaml
V3: **不通过**
  why_not_common: "赌徒谬误"是行为金融学常识
  degradation: 合并到 ce02 "向下摊平"反例
```

## decision (5条降级,6条保留)

### d04 — 大市到顶时如何退出
```yaml
V1: 通过
V2: 通过
V3: **不通过**
  why_not_common: 这是 d03 止盈决策在大市层面的应用
  degradation: 合并到 d03 止盈决策
```

### d07 — 何时空仓等待
```yaml
V1: 通过
V2: 通过
V3: **不通过**
  why_not_common: 与 d08 "清仓"重叠
  degradation: 合并到 d08
```

### d08 — 何时把已有投资转换为现金
```yaml
V1: 通过
V2: 通过
V3: **临界**
  why_not_common: 与 d07 重叠
  degradation: 合并到 d02 止损决策的扩展
```

### d09 — 资金应分散到几只
```yaml
V3: **不通过**
  why_not_common: 5-10只是常识
  degradation: 合并到 p07 "避免买太多股票"
```

### d10 — 模拟-实盘过渡
```yaml
V1: 通过
V2: 临界
V3: **不通过**
  why_not_common: "先小规模再扩大"是任何技能学习的常识
  degradation: 合并到 f10 "分层下注"的扩展
```

## glossary (9条降级,6条保留)

### g03 — 截短亏损,让利润奔跑
```yaml
V1: 通过
V2: 通过
V3: 临界
  why_not_common: 英文投资常识,中文环境内已是"截短亏损让利奔跑"高频表达
  degradation: **保留为 p02 principle 的术语解释,但不独立成 glossary**
```

### g05, g06 — 基础分析/技术分析
```yaml
V3: **不通过**
  why_not_common: 字典义已完整,作者未给出新定义
  degradation: 仅作为"分析框架总览"中引用,不独立
```

### g07 — 大市
```yaml
V3: **不通过**
  why_not_common: 中文金融术语,字典已定义
  degradation: 合并到 p15 解释
```

### g08 — 正常升势
```yaml
V3: **不通过**
  why_not_common: 这是 f03 框架的具体特征
  degradation: 合并到 f03
```

### g09 — 移动止损
```yaml
V3: **不通过**
  why_not_common: 这是 f05 框架的术语
  degradation: 合并到 f05
```

### g11, g12 — 牛皮阶段/最后阶段
```yaml
V3: **不通过**
  why_not_common: f04 框架的子阶段
  degradation: 合并到 f04
```

### g14 — 假象
```yaml
V3: 临界
  why_not_common: 索罗斯概念,作者用法无新意
  degradation: 合并到 f07 框架的解释中
```

---

## 数量统计

| 类别 | 降级 |
|---|---|
| framework | 2 (f04, f09) |
| principle | 4 (p05, p08, p12, p16) |
| case | 13 |
| counter-example | 8 (5 保留为反例,3 降级) |
| decision | 5 |
| glossary | 9 |
| **总计** | **41 / 87 (47%)** |

> 47% 降级率,合理。本书"实操类"内容多,真正能升级为通用 skill 的需要满足"反常识+可操作+多场景"三个条件。
