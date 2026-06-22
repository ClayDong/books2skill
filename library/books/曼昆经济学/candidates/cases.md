# 曼昆经济学 — 案例候选 (阶段 1 产出)

> case-extractor 产出。

```yaml
- id: c01
  title: 租金管制与住房短缺
  type: case
  source_chapter: 第6章 供给、需求与政府政策
  bound_framework: f05 供求均衡分析
  source_quote: |
    "租金管制是价格上限的一个例子。当价格上限低于均衡价格时，
    需求量超过供给量，出现短缺。短期内供给缺乏弹性，长期内供给富有弹性，
    房东不再维修房屋，住房质量下降。"
  summary: |
    纽约市的租金管制政策：本意保护租客，结果导致住房短缺、质量下降、黑市盛行。
    说明价格管制扭曲市场信号，短期看似有利，长期激励扭曲导致更差结果。
  tags: [price-control, housing, unintended-consequence]

- id: c02
  title: 最低工资法与就业
  type: case
  source_chapter: 第6章
  bound_framework: f05 供求均衡分析
  source_quote: |
    "最低工资法是价格下限的一个例子。如果最低工资高于均衡工资，
    劳动供给量超过需求量，产生失业。最低工资对青少年和低技能工人影响最大。"
  summary: |
    最低工资政策的双面性：提升在职工人收入，但减少低技能工人的就业机会。
    说明善意政策需分析激励效应和分布影响。
  tags: [price-control, labor, unemployment]

- id: c03
  title: 汽油税与税收归宿
  type: case
  source_chapter: 第6章
  bound_framework: f06 弹性分析框架
  source_quote: |
    "税收归宿取决于供给和需求的弹性。对汽油征税，由于需求缺乏弹性（短期内开车习惯不变），
    大部分税负由消费者承担。长期需求更富有弹性，税负更多转向生产者。"
  summary: |
    谁交税不等于谁承担税负。税收归宿由弹性决定——弹性小的一方承担更多。
    说明分析政策效果需区分法定归宿和经济归宿。
  tags: [tax, elasticity, tax-incidence]

- id: c04
  title: 1923年德国恶性通胀
  type: case
  source_chapter: 第1章
  bound_framework: p09 价格上升源于货币过多
  source_quote: |
    "1921年1月，德国一份日报的价格为0.3马克。不到两年之后，1922年11月，
    一份日报的价格为7000万马克。货币量增加如此之快，以至于价格水平暴涨。"
  summary: |
    德国魏玛共和国滥发货币→恶性通胀→民众储蓄化为乌有→社会动荡→纳粹崛起。
    说明货币超发的灾难性后果，验证"通胀是货币现象"。
  tags: [inflation, monetary-policy, historical]

- id: c05
  title: 苏联解体与市场机制缺失
  type: case
  source_chapter: 第1章
  bound_framework: p06 市场通常是组织经济活动的好方法
  source_quote: |
    "20世纪80年代末和90年代初的苏联解体、东欧剧变是该世纪最重要的事件之一。
    中央计划经济失败的一个关键原因是价格机制被废除，没有信号引导资源配置。"
  summary: |
    苏联计划经济 vs 市场经济：没有价格信号，中央计划者无法知道该生产什么、生产多少。
    验证"看不见的手"的有效性——价格机制是信息处理系统。
  tags: [market-vs-planning, historical, information]

- id: c06
  title: 农民与牧牛人的贸易
  type: case
  source_chapter: 第3章
  bound_framework: f04 比较优势决策框架
  source_quote: |
    "假设一个农民和一个牧牛人各自生产牛肉和土豆。
    即使牧牛人在两方面都更擅长（绝对优势），只要机会成本不同，
    两人仍可通过专业化生产和贸易使双方都受益。"
  summary: |
    经典比较优势案例：牧牛人养牛成本更低（放弃的土豆少），农民种土豆成本更低。
    专业化+贸易使总产量增加，双方都获得更多牛肉和土豆。
  tags: [comparative-advantage, trade, specialization]

- id: c07
  title: 垄断定价与无谓损失
  type: case
  source_chapter: 第15章
  bound_framework: f08 市场结构分析框架
  source_quote: |
    "垄断者选择边际收益等于边际成本的产量，此时价格高于边际成本。
    与竞争市场相比，垄断产量更低、价格更高，产生无谓损失。"
  summary: |
    垄断企业通过限制产量提高价格，消费者剩余部分转化为利润、部分消失（无谓损失）。
    说明市场势力导致效率损失，是反垄断政策的理论基础。
  tags: [monopoly, deadweight-loss, pricing]

- id: c08
  title: 污染管制与可交易许可证
  type: case
  source_chapter: 第10章
  bound_framework: f09 外部性分析框架
  source_quote: |
    "当存在负外部性时，社会成本大于私人成本。政府可以通过管制或
    庇古税来纠正。可交易污染许可证制度允许企业在市场上买卖排放权，
    实现减排成本最小化。"
  summary: |
    环境污染是经典负外部性。命令与控制（直接管制）vs 市场化手段（庇古税/可交易许可证）。
    后者更有效率，因为让减排成本最低的企业先减排。
  tags: [externality, pollution, policy-design]

- id: c09
  title: 公地悲剧
  type: case
  source_chapter: 第11章 公共物品和公共资源
  bound_framework: f09 外部性分析框架
  source_quote: |
    "公共资源在市场中往往被过度使用。当一个人使用公共资源时，
    他减少了别人对该资源的使用。由于这种负外部性，公共资源往往被过度使用。"
  summary: |
    公地悲剧：公共牧场被过度放牧，因为个人收益归自己，成本由所有人承担。
    解决方案：私有化、配额制、社区自治。说明产权界定对资源效率的关键作用。
  tags: [commons, externality, property-rights]

- id: c10
  title: 二手车市场与信息不对称
  type: case
  source_chapter: 第22章 微观经济学前沿
  bound_framework: f08 市场结构分析框架
  source_quote: |
    "阿克洛夫的柠檬市场：卖者知道车的质量而买者不知道。
    好车车主不愿以低价出售，坏车车主愿意。结果市场上充斥坏车，
    好车被挤出市场——逆向选择。"
  summary: |
    信息不对称导致市场失灵：逆向选择（交易前）和道德风险（交易后）。
    解决方案：信号传递（保修/学历）、筛选（保险免赔额）。
  tags: [information-asymmetry, adverse-selection, market-failure]
```
