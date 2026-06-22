# 曼昆经济学 — 术语词典 (阶段 1 产出)

> glossary-extractor 产出。所有 skill 共享此词典。

```yaml
- id: g01
  term: 机会成本
  type: term
  source_chapter: 第1章
  author_definition: |
    "为了得到某种东西所必须放弃的东西。"
  key_distinction: |
    ≠ 会计成本（只算花的钱）
    = 显性成本 + 隐性成本（放弃的最佳替代品价值）
    例：上大学的机会成本 = 学费 + 放弃的工资收入
  why_it_matters: 所有决策类 skill 的基础概念。混淆机会成本与会计成本会导致系统性决策错误。

- id: g02
  term: 边际变动
  type: term
  source_chapter: 第1章
  author_definition: |
    "对现有行动计划的微小增量调整。"
  key_distinction: |
    ≠ 平均值（总成本/总数量）
    = 增量值（多一单位的成本/收益）
    边际成本（MC）= 多生产一单位的额外成本
    边际收益（MB）= 多消费一单位的额外收益
  why_it_matters: 理性决策的核心机制。在边际上做比较是经济学区别于常识思维的关键。

- id: g03
  term: 理性人
  type: term
  source_chapter: 第1章
  author_definition: |
    "系统而有目的地尽最大努力实现其目标的人。"
  key_distinction: |
    ≠ 完全信息（理性不等于全知）
    ≠ 永远正确（理性是在给定信息下做最优选择）
    ≠ 自私（理性人的目标可以是利他的）
  why_it_matters: 经济学模型的基本假设。理解其限制（行为经济学）是正确使用经济分析的前提。

- id: g04
  term: 看不见的手
  type: term
  source_chapter: 第1章
  author_definition: |
    "亚当·斯密的概念：个体在追求自身利益时，仿佛被一只看不见的手引导，
    促进了社会利益。"
  key_distinction: |
    ≠ "市场万能"（存在市场失灵）
    = 价格机制作为信息处理和资源分配系统
    价格传递稀缺性信息、协调分散决策、激励生产
  why_it_matters: 理解市场效率的核心隐喻。也是政府干预辩论的焦点。

- id: g05
  term: 市场失灵
  type: term
  source_chapter: 第1章
  author_definition: |
    "市场单独不能有效配置资源的情况。"
  key_distinction: |
    ≠ "市场坏了"（市场仍在运行，只是结果无效率）
    三大来源：外部性、公共物品、市场势力（垄断）
  why_it_matters: 政府干预的正当性基础。识别市场失灵是政策设计的第一步。

- id: g06
  term: 无谓损失
  type: term
  source_chapter: 第8章
  author_definition: |
    "市场扭曲（如税收）引起的总剩余减少。"
  key_distinction: |
    ≠ 税收总额（那是转移，不是损失）
    = 因扭曲导致交易不发生而消失的福利
    无谓损失与税率平方成正比（税率翻倍→损失四倍）
  why_it_matters: 评估任何市场干预（税收、价格管制、垄断）效率成本的工具。

- id: g07
  term: 消费者剩余
  type: term
  source_chapter: 第7章
  author_definition: |
    "买者愿意支付的量减去其实际支付的量。"
  key_distinction: |
    ≠ "省了钱"（它是福利衡量，不是会计概念）
    = 需求曲线以下、价格以上的面积
  why_it_matters: 福利分析的基础工具。与生产者剩余一起衡量市场效率。

- id: g08
  term: 弹性
  type: term
  source_chapter: 第5章
  author_definition: |
    "衡量需求量或供给量对某因素（如价格）变化的反应程度。"
  key_distinction: |
    ≠ "变化量"（那是绝对值）
    = 百分比变化之比（无量纲）
    |E|>1 富有弹性，|E|<1 缺乏弹性，|E|=1 单位弹性
  why_it_matters: 定价决策、税收归宿分析、政策效果预测的核心参数。

- id: g09
  term: 比较优势
  type: term
  source_chapter: 第3章
  author_definition: |
    "一个生产者以低于其他生产者的机会成本生产一种物品的能力。"
  key_distinction: |
    ≠ 绝对优势（谁做得更好）
    = 谁放弃的代价更小
    即使在所有方面都弱，只要差距不均匀，仍有比较优势
  why_it_matters: 贸易理论基石。适用于个人分工、企业战略、国际贸易。

- id: g10
  term: 外部性
  type: term
  source_chapter: 第10章
  author_definition: |
    "一个人的行为对旁观者福利的影响，且这种影响未通过价格反映。"
  key_distinction: |
    ≠ "间接影响"（通过价格传导的影响不是外部性）
    正外部性：教育、疫苗接种、技术研发
    负外部性：污染、噪音、拥堵
  why_it_matters: 识别市场失灵的关键概念。政策设计的出发点。

- id: g11
  term: 沉没成本
  type: term
  source_chapter: 第1章（隐含）
  author_definition: |
    "已经发生且无法收回的成本。"
  key_distinction: |
    ≠ 可避免成本（可以通过改变决策避免的）
    = 不应影响当前决策的过去支出
  why_it_matters: 防止沉没成本谬误——"已经投入这么多了不能放弃"是错误推理。

- id: g12
  term: 效率
  type: term
  source_chapter: 第1章
  author_definition: |
    "社会能从其稀缺资源中得到最大利益的特性。"
  key_distinction: |
    ≠ "速度快"或"成本低"
    = 总剩余最大化（资源配置使所有互利的交易都发生）
    与"平等"（分配均匀）构成权衡
  why_it_matters: 政策评估的核心维度之一。效率与平等的权衡是政治经济学的基本议题。
```
