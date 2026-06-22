# 炒股的智慧 — 原则候选 (principle-extractor 产出)

> 阶段1.5 会做去重,这里宁多勿少。

- id: p01
  title: 止损是最高行为准则
  type: principle
  source_chapter: 第五章 华尔街的家训
  source_quote: |
    "止损,止损,止损!我不知道该怎样强调这两字的重要,我也不知还能怎么解释这两个字,
    这是炒股行的最高行为准则。你如果觉得自己实在没法以比进价更低的价钱卖出手中的股票,
    那就赶快退出这行吧!"
  summary: |
    在交易中,止损规则的优先级高于其他所有考量。
    如果无法执行止损(在亏损达到预设点时坚决卖出),应退出市场。
    适用于: 任何有下行风险的资本配置决策。
  tags: [principle, risk-management, non-negotiable]

- id: p02
  title: 截短亏损,让利润奔跑
  type: principle
  source_chapter: 第四章
  source_quote: |
    "华尔街将炒股的诀巧归纳成两句话:截短亏损,让利润奔跑!
    英文叫 Cut loss short, let profit run!意思即是一见股票情况不对, 即刻止损, 把它缩得越短越好!
    一旦有了利润,就必须让利润奔跑,从小利润跑成大利润。"
  summary: |
    在盈亏两端采取不对称策略:亏损时快速离场(缩小单笔损失),
    盈利时耐心持有(放大单笔收益)。
    这是用正不对称性构造长期正期望的数学原则。
  tags: [principle, asymmetric-strategy, expectation-value]

- id: p03
  title: 截断亏损单的金额不应超过总投资额20%
  type: principle
  source_chapter: 第四章 第一节
  source_quote: |
    "你必须有个止损点,这个止损点不应超出投资额的20%。
    请读者切切牢记,否则这里讲的一切都是空的。"
  summary: |
    单笔交易的预设止损线不应超过总投资额的20%,以确保即使所有交易都止损,
    也仍有资本继续参与市场。
    数字原则:5元股票止损10%=0.5元空间;50元股票止损10%=5元空间。
  tags: [principle, position-sizing, hard-limit, rule-of-thumb]

- id: p04
  title: 入场前必先确定止损点
  type: principle
  source_chapter: 第四章 第一节
  source_quote: |
    "在选买点的最最重要点是选择止损点。即在你进场之前,你必须很清楚
    若股票的运动和你的预期不合,你必须在何点止损离场。
    换句话说,你在投资做生意,不要老是想你要赚多少钱,
    首先应该清楚自己能亏得起多少。"
  summary: |
    决策时序: 先定最大可承受亏损→再定入场点,而非反过来。
    原则基于风险预算:每一笔投资的风险敞口应预定义,反向推导出仓位。
    适用于任何有可量化损失的决策。
  tags: [principle, decision-order, risk-first]

- id: p05
  title: 分散风险——五到十只股票
  type: principle
  source_chapter: 第五章
  source_quote: |
    "手手头的资本分成五至十份,在你认为至少有1:3的风险报酬比率时
    把其中的一份入市,同时牢记止损的最高生存原则,长期下来,不赚钱都难。"
  summary: |
    资本应分散到5-10只股票中,每笔交易的资金占比与风险回报比正相关。
    触发条件:风险报酬比至少1:3才入场;固定手数分散。
    适用于非专业投资者的资产配置。
  tags: [principle, diversification, risk-budget]

- id: p06
  title: 有疑问,离场!
  type: principle
  source_chapter: 第五章
  source_quote: |
    "这是条很容易明白但很不容易做到的规则。
    很多时候,你根本就对股票的走势失去感觉,你不知它要往上爬还是朝下跌,
    你也搞不清它处在升势还是跌势。此时,你的最佳选择就是离场!"
  summary: |
    当对持仓/机会缺乏清晰判断时,默认动作是离场(卖出或观望)而非继续持有/加仓。
    适用条件: 无法判断走势、感觉不对、胜算不超过50%。
    适用于任何"宁可不参与"优于"糊涂参与"的决策。
  tags: [principle, default-action, awareness-check]

- id: p07
  title: 避免买太多股票——注意力是稀缺资源
  type: principle
  source_chapter: 第五章
  source_quote: |
    "问自己你能记住几个电话号码?普通人是110个,你呢?
    手头股票太多时,产生的结果就是注意力分散,失去对单独股票的感觉。
    将注意力集中在三至五只最有潜力的股票。"
  summary: |
    持仓数量应受注意力容量限制,通常3-5只,极限20只。
    超过此限,跟踪质量下降,判断力被稀释。
    适用于: 投资组合构建、副业项目选择、并行任务管理。
  tags: [principle, focus, attention-budget, portfolio-management]

- id: p08
  title: 别频繁交易
  type: principle
  source_chapter: 第五章
  source_quote: |
    "在你留意跟踪的股票中,每天都有70%胜算的交易机会是骗人的。
    频繁交易常常是因为枯燥无聊。频繁交易不仅损失手续费,
    同时使交易的质量降低。"
  summary: |
    减少非必要交易,因为: 1) 手续费侵蚀利润 2) 频繁进出降低决策质量 3) 多为情绪驱动而非信号驱动。
    反面: 70%所谓的"每日机会"是噪音。
    适用于: 任何"做得越多越好"的反直觉场景。
  tags: [principle, frequency-control, transaction-cost, discipline]

- id: p09
  title: 不要向下摊平
  type: principle
  source_chapter: 第五章
  source_quote: |
    "犯了错,不是老老实实地认错,重新开始,抱着侥幸心理,向下摊平,
    把平均进价降低,希望股票小有反弹就能挽回损失,甚至赚钱。
    这是常人的想法和做法,在炒股这行则是破产的捷径。"
  summary: |
    亏损时不加仓以降低平均成本(向下摊平)。
    黄金铁律: 第一次入场后,纸面上没有利润的话不要加码。
    纸面有利润才表示判断正确,可加注。
    适用于: 任何"沉没成本"陷阱场景——不因已投入资源而加倍投入。
  tags: [principle, anti-sunk-cost, position-management, hard-rule]

- id: p10
  title: 忘掉入场价
  type: principle
  source_chapter: 第五章
  source_quote: |
    "之所以难以忘掉进价,这和人性中喜赚小偏宜,决不愿吃小亏的天性有关。
    人很难改变自己的人性,那就试着忘掉进价吧!
    这样你就能专注于正确的时间做正确的事。"
  summary: |
    决策应基于对当前价格走势的判断,而非买入价(锚定效应)。
    检验方法: 假设"假如我今天手边有钱,还会买这只股票吗?" 若否,应卖出。
    适用于任何需突破"既有投入"心理障碍的决策。
  tags: [principle, anchoring, fresh-look, decision-quality]

- id: p11
  title: 股市从来不会错
  type: principle
  source_chapter: 第五章
  source_quote: |
    "记住: 股市从来都不会错,它总是走自己要走的路,会错的只有人自己。
    你所能做的只有追随股市。见到危险信号,不要三心二意,不要存有幻想,把股票全部脱手。"
  summary: |
    决策归责: 当你的预期与市场表现冲突时,错的是你的判断,不是市场。
    操作含义: 见到危险信号立即清仓,不抱反弹幻想。
    适用于: 任何需要"事实优先于预期"的认知场景。
  tags: [principle, market-honesty, accountability, error-correction]

- id: p12
  title: 不要试图寻找最高点
  type: principle
  source_chapter: 第四章 第二节
  source_quote: |
    "让我提醒股友: 不要试图寻找股票的最高点,你永远不知股票会升多高。
    就我个人的体会,做何时卖股票的决定较决定何时买股票更为困难。"
  summary: |
    放弃预测极值的幻想,转为"中间一截"策略——抓到波幅的60-70%即可。
    极端值的不可知性使精确择时成为低期望值行为。
    适用于: 任何要求"完美时机"的决策场景。
  tags: [principle, satisficing, accepting-uncertainty]

- id: p13
  title: 涨时不要急于获利了结
  type: principle
  source_chapter: 第三章 第一节
  source_quote: |
    "炒股高手利物莫特别指明,他炒股的秘诀不是他怎样思考,
    而是在他买对了的时候能够安坐不动。这是很难的一件事,
    你要克服对脱手获利的冲动。"
  summary: |
    在确认趋势正常后,克服"落袋为安"冲动,让持仓继续参与升势。
    行为挑战: 已知正确但需不动=逆"兑现小利"本能。
    配合p02使用,形成完整的不对称策略。
  tags: [principle, letting-winners-run, overcoming-impulse]

- id: p14
  title: 失败者贪小便宜、吃不得小亏
  type: principle
  source_chapter: 第一章
  source_quote: |
    "好贪小偏宜,吃不得小亏的心态使一般股民几乎必然地成了输家。
    股市没有击败你,你自己击败了自己。"
  summary: |
    自我诊断检查项: 赚小钱就跑 + 亏小钱不止损 = 输家模式。
    行为根源: 风险厌恶+短视的复合人性弱点。
    修正路径: 见p01-p03止损规则。
  tags: [principle, self-diagnosis, failure-pattern]

- id: p15
  title: 大市不好时,别买任何股票
  type: principle
  source_chapter: 第二章 第三节
  source_quote: |
    "虽然这有一个学习过程,但一定要在心理上不断提醒自己:
    大市不好时,别买任何股票。
    请记着: 当街头巷尾的民众都在谈论股市如何容易赚钱的时候,
    大市往往已经到顶或接近到顶。"
  summary: |
    大市是胜率的乘数,熊市中个股α不足以补偿β下行。
    操作含义: 宁可空仓等待,不做逆大市操作。
    大市到顶的反向指标: 大众普遍谈论股市赚钱。
    适用于: 任何有"系统性风险敞口"的市场参与决策。
  tags: [principle, market-context, anti-crowd, defensive]

- id: p16
  title: 看得见的指标才重要
  type: principle
  source_chapter: 第三章 第一节
  source_quote: |
    "股窜上,股价升,股价跌了,你在干什么?
    实际的操作不同于理论上的指标。你看到的指标是死的,你要活学活用。"
    (技术分析vs实际操作的边界)
  summary: |
    理论工具(均线/MACD等)是参考,非教条。
    真正的判断标准是: 交易量配合 + 走势特征 + 临界点突破 三者综合。
    反对: 机械套用指标,无差别交易。
  tags: [principle, theory-vs-practice, flexibility]

- id: p17
  title: 优秀的投资者具有共同素质——可迁移于任何行业
  type: principle
  source_chapter: 前言
  source_quote: |
    "我相信书中阐述的原理适合任何行业。成功的人士往往具有很多相似的素质,
    如果你具有炒股成功所需的素质,在其它行业, 我相信你也一样能获得成功。"
  summary: |
    核心素质跨场景可迁移: 1) 锲而不舍 2) 战胜自己 3) 独立思考 4) 甘于孤独 5) 耐心与自制。
    不炒股的人也可阅读并应用这些素质于自身领域。
    适用于: 任何需识别"领域通用核心素质"的场景。
  tags: [principle, transferable-qualities, expertise, meta-principle]

- id: p18
  title: 普通人"做不到自己知道该做的事情"
  type: principle
  source_chapter: 第三章
  source_quote: |
    "我们都知道诚实是取信于人的不二法门,有多少人做到了?
    我们都知道'贪'是受骗的根源,有多少人做到了'不贪'?
    这就是为何成功的概率甚至低过减肥——减肥只需要4个字:少吃多动,
    但100人参加,只有2%成功持续1年。"
  summary: |
    知行合一是核心障碍: 知道正确的事 vs 持续做正确的事之间的鸿沟是失败主因。
    适用范围: 远超炒股——减肥、学习、健康、关系管理。
    修正方向: 应用知识需毅力,毅力来自反复的痛苦反馈(见f06)。
  tags: [principle, knowledge-action-gap, discipline, universal]
