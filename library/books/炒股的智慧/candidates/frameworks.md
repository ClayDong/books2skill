# 炒股的智慧 — 框架候选 (framework-extractor 产出)

> 阶段1.5 会做去重,这里宁多勿少。

- id: f01
  title: 临界点决策模型
  type: framework
  source_chapter: 第四章 何时买股票
  source_quote: |
    "图中所有的突破点都可以叫临界点。我总是将买卖控制在临界点附近。
    什么是'临界点'呢？大家知道水在100度变成蒸汽，科学上称100度正是水的临界点。
    把它推广开来……在股票的操作系统上，这些点往往是公众对股价重新评估的点，
    也就是在这些点上，你入场的获胜概率最高。"
  summary: |
    临界点 = 公众对股价重新评估的转折点,在此入场获胜概率最高。
    通过将物理相变的隐喻移植到金融市场,作者建立了一个基于"概率拐点"而非"价格高低"
    的决策框架。识别临界点 = 识别交易量/价格/支撑阻力线三者共振的时刻。
    这把"什么时候买卖"从主观判断转化为可学习的模式识别问题。
  tags: [framework, decision, technical-analysis, market-timing]

- id: f02
  title: 概率思维框架
  type: framework
  source_chapter: 第三章 成功的要素
  source_quote: |
    "股票是概率的游戏，无论什么样的买卖决定，都没有100%正确或不正确的划分。"
    "久赌必赢的技巧在于每次下注，你的获胜概率必须超过50%，
    只要你只下本金的小部分,不会为几次坏运气就剃光头,从长期而言你是胜定了。"
  summary: |
    炒股不是追求单次正确,而是建立长期概率优势。
    框架三要素: 1) 胜算>50%才入场 2) 下注小到失败也不淘汰 3) 让盈利单奔跑、亏损单快速离场。
    这是把赌场盈利模型移植到股市的数学框架,把交易从"赌博"变成"开着赌场的生意"。
  tags: [framework, probability, decision, gambling-analogy]

- id: f03
  title: 临界点四阶段识别法
  type: framework
  source_chapter: 第二章 技术分析
  source_quote: |
    "任何正常的股票运动都分为四个阶段：1.牛皮阶段 2.正常升势 3.疯狂阶段 4.最后阶段"
  summary: |
    把任何股票运动划分为四个阶段: 牛皮(无方向)→正常升势(波浪上升+交易量配合)→
    疯狂(暴利但危险)→最后(崩盘前夜)。每个阶段对应不同的操作策略:
    牛皮观望、升势买入、疯狂逐步退出、最后清仓。
    这是把价格走势从"连续流"离散化为"可操作状态机"的框架。
  tags: [framework, technical-analysis, stage-model, market-cycles]

- id: f04
  title: 大势优先框架
  type: framework
  source_chapter: 第二章 第三节 股票分析之我见
  source_quote: |
    "炒股是概率的游戏,逆大潮流而动,你的获胜概率就被大打折扣了。
    将大市和单独股票结合起来考虑,是专业炒手们必须培养的心态。
    虽然这有一个学习过程,但一定要在心理上不断提醒自己:大市不好时,别买任何股票。"
  summary: |
    决策层次: 大市(牛/熊) → 类别股 → 个股。自上而下三层过滤。
    大市决定胜率乘数,类别股决定行业β,个股决定α。
    在熊市中即使看好个股也应减仓或空仓,这是用系统降低决策噪音的框架。
  tags: [framework, top-down, market-context, position-sizing]

- id: f05
  title: 移动止损加码法
  type: framework
  source_chapter: 第四章 第二节 何时卖股票
  source_quote: |
    "买入后，如果股票开始正常的升势,它应有一浪高过一浪的特点。
    你可以将止损点放在每个波浪的浪谷,随着波浪往上翻,你将卖点由A->B->C->D->E往上移。
    这样就能保证你不会在升势时过早离场。"
  summary: |
    随股价上升不断上移止损点,实现"截短亏损,让利润奔跑"的动态版本。
    框架: 1) 入场设初始止损 2) 股价创新高,止损移到上一浪谷 3) 趋势加速可加码
    4) 跌破移动止损则清仓。这把"何时止盈"转化为机械规则,避免情绪化早退。
  tags: [framework, position-management, trailing-stop, technical-analysis]

- id: f06
  title: 心理训练三步法
  type: framework
  source_chapter: 第六章 心理建设
  source_quote: |
    "你必须学习体会按规则行动是愉快的,不按规则行动是痛苦的。
    刚学止损的时候,亏钱总是痛苦的,不然何为割肉？
    随着时间的推移,你经历了小损成为大损的过程……
    慢慢地成为下意识的行动,一旦股票运动不对,不采取行动就寝食难安。"
  summary: |
    把"止损"从痛苦→习惯→直觉的转变路径显性化。
    步骤: 1) 规则先行(写下来止损点) 2) 痛苦反馈(每次不执行都赔钱) 3) 内化(违规寝食难安)。
    这是一个用"重复痛苦"训练"正确行为"的认知重塑框架,适用于任何需克服人性弱点的场景。
  tags: [framework, psychology, habit-formation, self-regulation]

- id: f07
  title: 假象参与退出框架
  type: framework
  source_chapter: 第七章 抓住大机会
  source_quote: |
    "经济史是一部基于假象和谎言的连续剧,经济史的演绎从不基于真实的剧本,
    但它铺平了累积巨额财富的道路。
    做法就是认清其假象,投入其中,在假象被公众认识之前退出游戏。"
  summary: |
    索罗斯范式: 把泡沫视为可参与可利用的"假象",三阶段:
    1) 识别假象(价格已脱离价值但仍有上涨动力)
    2) 投入其中(在大众尚未清醒时建立头寸)
    3) 提前退出(在大众觉醒前离场)。
    这把"市场非理性"从风险转化为机会,前提是能识别"非理性"的终点。
  tags: [framework, bubble, reflexivity, contrarian-strategy]

- id: f08
  title: 学股四阶段模型
  type: framework
  source_chapter: 第八章 学股的四个阶段
  source_quote: |
    "我在这里就以自己的学股历程谈谈学股经过的阶段,你可以参照我的描述,
    估计一下自己现在处于什么阶段。蛮干阶段、摸索阶段、体验风险阶段、久赌必赢阶段。"
  summary: |
    把学股划分为四个递进阶段: 蛮干(无系统)→摸索(试验规则)→体验风险(大亏反思)→久赌必赢(规则内化)。
    每个阶段有不同的思维特征、操作特征、心理特征,可自评定位。
    这是用阶段论把"成为专家"从模糊目标转化为可诊断、可突破的连续过程。
  tags: [framework, learning-stages, self-assessment, expertise-development]

- id: f09
  title: 临界点买股三层过滤模型
  type: framework
  source_chapter: 第四章 第一节 何时买股票
  source_quote: |
    "你应该先运用基础分析,选择最有希望的股票。
    在这个基础上,再看这只股票是否在上升阶段。
    在具体买卖时,在突破临界点时入场,以便提高获胜概率。"
  summary: |
    买股决策的三层过滤: 1) 基础分析(选对公司) 2) 阶段判断(选对时机) 3) 临界点入场(选对价格)。
    这是一个"在什么价位买什么公司的什么阶段股票"的决策树,每层降低不确定性。
    与f04的自上而下不同,这是单股操作时的"由内而外"分析流程。
  tags: [framework, decision-tree, multi-factor-analysis, stock-picking]

- id: f10
  title: 分层下注资金管理
  type: framework
  source_chapter: 第三章 第二节 资金管理
  source_quote: |
    "具体的做法就是分层下注。你如果预备买1000股某只股票,第一手别买1000股,
    先买200股试试,看看股票的运动是否符合你的预想,然后再决定下一步怎么做。
    如果不对,尽速止损。如果一切正常,再进400股,结果又理想的话,买足1000股。"
  summary: |
    把单笔交易分解为多个递增子单,每层根据前一层结果决定是否继续。
    步骤: 1) 试仓(20%仓位验证假设) 2) 验证通过→加仓(40%) 3) 持续验证→满仓(100%)。
    这是用"递进确认"控制单笔决策风险的资金管理框架,把"all-in"从赌注变为可调参数。
  tags: [framework, position-sizing, risk-management, incremental-commitment]
