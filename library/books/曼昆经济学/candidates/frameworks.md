# 曼昆经济学 — 框架候选 (阶段 1 产出)

> framework-extractor 产出。每条候选将在阶段 1.5 三重验证。

```yaml
- id: f01
  title: 机会成本思维
  type: framework
  source_chapter: 第1章 经济学十大原理
  source_quote: |
    "一种东西的机会成本（opportunity cost）是为了得到这种东西所必须放弃的东西。
    当做出任何一项决策时，决策者都应该认识到每一种可能的行动所带来的机会成本。"
  summary: |
    面对任何选择时，不只看付出的代价（会计成本），更要问"放弃了什么最佳替代选项"。
    机会成本 = 显性成本 + 隐性成本（如时间、放弃的收益）。
    上大学的最大成本不是学费，而是放弃的工作收入。
  tags: [decision, mental-model, opportunity-cost]

- id: f02
  title: 边际决策法
  type: framework
  source_chapter: 第1章 经济学十大原理
  source_quote: |
    "理性人通常通过比较边际收益（marginal benefit）与边际成本（marginal cost）来做决策。
    理性人考虑边际量。"
  summary: |
    决策不在"全做或全不做"之间选择，而在"多一单位值不值"之间判断。
    比较边际收益（MB）与边际成本（MC）：MB>MC 则做，MB<MC 则停，MB=MC 为最优。
    不看平均成本/收益，只看增量的边际值。
  tags: [decision, mental-model, marginal-analysis]

- id: f03
  title: 激励分析框架
  type: framework
  source_chapter: 第1章 经济学十大原理
  source_quote: |
    "激励（incentive）是引起一个人做出行动的某种东西。由于理性人通过比较成本与收益做出决策，
    所以他们会对激励做出反应。"
  summary: |
    预测任何政策/规则/制度变化的效果时，先分析它如何改变了相关主体的边际成本或边际收益。
    关键追问：这个变化让什么变得更贵了？让什么变得更便宜了？谁的行为会因此改变？
    警惕意外后果（unintended consequences）——激励改变可能引发意料之外的行为变化。
  tags: [decision, behavioral-prediction, incentive]

- id: f04
  title: 比较优势决策框架
  type: framework
  source_chapter: 第3章 相互依存性与贸易的好处
  source_quote: |
    "比较优势：一个生产者以低于其他生产者的机会成本生产一种物品。
    机会成本最低的人应该专业化生产该物品，通过贸易使双方都受益。"
  summary: |
    分工依据不是"谁做得最好"（绝对优势），而是"谁放弃的代价最小"（比较优势）。
    即使A在所有方面都强于B，只要A的机会成本在X上更高，B就应该做X，A做Y，然后贸易。
    适用于个人职业选择、团队分工、国际贸易。
  tags: [decision, specialization, trade, comparative-advantage]

- id: f05
  title: 供求均衡分析
  type: framework
  source_chapter: 第4章 供给与需求的市场力量
  source_quote: |
    "供给与需求的力量共同决定了市场中每种物品的价格和销售量。
    均衡价格是使供给量等于需求量的价格。"
  summary: |
    分析任何市场现象的三步法：(1) 识别影响需求曲线的因素（偏好/收入/相关品价格/预期/买家数量）；
    (2) 识别影响供给曲线的因素（投入品价格/技术/预期/卖家数量）；
    (3) 看曲线移动后的新均衡点——价格和数量如何变化。
    "需求增加"（曲线右移）≠ "需求量增加"（沿曲线移动）。
  tags: [market-analysis, supply-demand, equilibrium]

- id: f06
  title: 弹性分析框架
  type: framework
  source_chapter: 第5章 弹性及其应用
  source_quote: |
    "需求价格弹性衡量需求量对价格变化的反应程度。
    如果弹性大于1，需求是富有弹性的；如果小于1，需求是缺乏弹性的。"
  summary: |
    判断价格变化对总收益的影响：
    富有弹性（|E|>1）→ 降价增加总收益，涨价减少总收益；
    缺乏弹性（|E|<1）→ 降价减少总收益，涨价增加总收益；
    单位弹性（|E|=1）→ 价格变化不影响总收益。
    弹性大小取决于：替代品可得性、必需品vs奢侈品、市场定义范围、时间长短。
  tags: [pricing, market-analysis, elasticity]

- id: f07
  title: 福利分析框架
  type: framework
  source_chapter: 第7章 消费者、生产者与市场效率
  source_quote: |
    "消费者剩余是买者愿意支付的量减去其实际支付的量。
    生产者剩余是卖者得到的量减去其生产成本。
    总剩余=消费者剩余+生产者剩余。使总剩余最大化的结果就是有效率的。"
  summary: |
    评估任何市场结果或政策的三步法：
    (1) 计算消费者剩余（需求曲线以下、价格以上的面积）；
    (2) 计算生产者剩余（价格以下、供给曲线以上的面积）；
    (3) 总剩余是否最大化？如果政策导致总剩余减少，减少的部分就是无谓损失。
  tags: [welfare, efficiency, policy-evaluation]

- id: f08
  title: 市场结构分析框架
  type: framework
  source_chapter: 第14-17章 竞争市场、垄断、垄断竞争、寡头
  source_quote: |
    "竞争市场：许多买者卖者，产品相同，价格接受者。
    垄断：单一卖者，价格制定者，进入壁垒。
    寡头：少数卖者，策略互动，博弈论分析。"
  summary: |
    判断行业竞争格局的四维分类法：
    (1) 买家/卖家数量（多→少）；
    (2) 产品差异度（同质→差异）；
    (3) 进入壁垒（低→高）；
    (4) 企业对价格的控制力（无→完全）。
    不同结构下企业行为、定价策略、效率水平截然不同。
  tags: [market-structure, competitive-analysis, pricing]

- id: f09
  title: 外部性分析框架
  type: framework
  source_chapter: 第10章 外部性
  source_quote: |
    "外部性是一个人的行为对旁观者福利的影响。
    负外部性使社会成本大于私人成本，正外部性使社会价值大于私人价值。
    市场均衡使社会结果无效率。"
  summary: |
    识别和应对市场失灵的框架：
    (1) 识别行为是否影响第三方（外部性存在？）；
    (2) 判断方向（正/负）和大小；
    (3) 私人成本/收益 vs 社会成本/收益的差距；
    (4) 选择应对：管制（命令与控制）、庇古税/补贴、可交易许可证、科斯协商。
  tags: [market-failure, externality, policy-design]
```
