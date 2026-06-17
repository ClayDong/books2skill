# 曼昆经济学 — 反例候选 (阶段 1 产出)

> counter-example-extractor 产出。

```yaml
- id: ce01
  title: 忽视机会成本导致错误决策
  type: counter-example
  source_chapter: 第1章
  bound_framework: f01 机会成本思维
  source_quote: |
    "上大学的成本并不是你用于学费、书籍、住宿和伙食的钱加总。
    即使你离开了学校，你也需要有睡觉的地方并且需要吃饭。
    上大学最大的成本是你放弃的工作收入。"
  summary: |
    常见错误：只算会计成本（花了多少钱），忽略隐性成本（放弃了什么）。
    典型表现：自己开店觉得"不用付工资"——忽略了放弃的工资收入。
  tags: [fallacy, opportunity-cost, sunk-cost-confusion]

- id: ce02
  title: 在平均而非边际上做决策
  type: counter-example
  source_chapter: 第1章
  bound_framework: f02 边际决策法
  source_quote: |
    "当平均成本告诉你该停产时，边际分析可能告诉你该继续生产。
    航空公司在航班即将起飞前以低于平均成本的价格卖票仍可获利——
    因为边际成本（多一个乘客的燃油和零食）远低于平均成本。"
  summary: |
    常见错误：用平均成本/收益做决策，而非边际值。
    导致：过早停产（平均成本高但边际成本低时）、或过度生产（平均成本低但边际成本高时）。
  tags: [fallacy, marginal-analysis, average-vs-marginal]

- id: ce03
  title: 忽视激励的意外后果
  type: counter-example
  source_chapter: 第1章
  bound_framework: f03 激励分析框架
  source_quote: |
    "汽油价格上升鼓励人们开更省油的车、住得离工作地点更近、坐公共交通。
    当政府对某些行为征税或补贴时，人们会改变行为以规避税收或获取补贴。"
  summary: |
    常见错误：设计政策时只考虑目标效果，忽视行为反应。
    典型案例：租金管制→住房短缺；最低工资→低技能失业；安全带法→驾驶更冒险（佩兹曼效应）。
  tags: [fallacy, unintended-consequence, incentive]

- id: ce04
  title: 价格管制导致更差结果
  type: counter-example
  source_chapter: 第6章
  bound_framework: f05 供求均衡分析
  source_quote: |
    "价格上限导致短缺，价格下限导致过剩。
    短缺导致配给、排队、黑市；过剩导致浪费、政府收购。"
  summary: |
    常见错误：以为价格管制能"保护"弱势群体，实际上扭曲了市场信号。
    租金管制→住房质量下降、新建减少；最低工资→低技能失业；农产品价格支持→奶油湖。
  tags: [fallacy, price-control, market-distortion]

- id: ce05
  title: 混淆"需求增加"与"需求量增加"
  type: counter-example
  source_chapter: 第4章
  bound_framework: f05 供求均衡分析
  source_quote: |
    "需求量增加是指沿需求曲线移动（价格变化引起）。
    需求增加是指整条需求曲线右移（非价格因素引起）。"
  summary: |
    常见错误：把"价格下降导致买得更多"说成"需求增加"。
    实际上价格变化只引起需求量变化（沿曲线移动），只有收入/偏好/相关品价格等变化才引起需求变化（曲线移动）。
  tags: [fallacy, terminology, demand]

- id: ce06
  title: 混淆会计利润与经济利润
  type: counter-example
  source_chapter: 第1章
  bound_framework: f01 机会成本思维
  source_quote: |
    "会计利润=总收益-显性成本。经济利润=总收益-显性成本-隐性成本（机会成本）。
    企业获得零经济利润时仍在正常运营——它恰好获得了正常回报。"
  summary: |
    常见错误：看到会计利润为正就认为"赚钱了"，实际上可能经济利润为零（资源放在别处也能赚这些）。
    零经济利润=正常回报，不是"不赚钱"。
  tags: [fallacy, profit, opportunity-cost]

- id: ce07
  title: 沉没成本谬误
  type: counter-example
  source_chapter: 第1章（隐含）
  bound_framework: f02 边际决策法
  source_quote: |
    "理性人面向未来做决策。已经发生的、无法收回的成本（沉没成本）不应影响当前决策。
    边际分析只看未来的边际成本和边际收益。"
  summary: |
    常见错误："已经投入这么多了，不能放弃"——沉没成本不应影响决策。
    正确做法：只看从现在起继续投入的边际成本 vs 边际收益。
  tags: [fallacy, sunk-cost, decision]

- id: ce08
  title: 合成谬误——对个人成立的对整体不一定成立
  type: counter-example
  source_chapter: 第1章（隐含）
  bound_framework: f03 激励分析框架
  source_quote: |
    "一个人站起来看球赛能看得更清楚，但所有人都站起来并不会所有人都看得更清楚。
    对个人正确的结论对整体不一定正确。"
  summary: |
    常见错误：从个体行为推导整体结果时忽视反馈效应。
    典型案例：一个人储蓄更多→更富有；所有人储蓄更多→总需求下降→收入减少→更穷（节俭悖论）。
  tags: [fallacy, composition, macro-micro]
```
