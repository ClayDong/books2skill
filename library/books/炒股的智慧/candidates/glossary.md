# 炒股的智慧 — 术语候选 (glossary-extractor 产出)

> 阶段1.5 会做去重,这里宁多勿少。

- id: g01
  term: 临界点
  type: term
  source_chapter: 第四章
  author_definition: |
    "图中所有的突破点都可以叫临界点。我总是将买卖控制在临界点附近。
    什么是'临界点'呢？大家知道水在100度变成蒸汽,科学上称100度正是水的临界点。
    把它推广开来,经济活动的临界点指这个经济活动正进入另一种状态,
    决定它的条件已充分具备,在临界点附近买入(卖出),获胜概率最大。"
  key_distinction: |
    ≠ 物理相变点 — 是借喻,不是真的相变
    ≠ 转折点 — 强调"概率最高"的入场点
    ≠ 高点/低点 — 临界点是突破点,不一定是极值点
    = 公众对股价重新评估时,买入获胜概率最高的位置
  why_it_matters: |
    整个交易系统的核心是"在临界点附近操作",如不能正确理解"临界点",
    会把"突破点"误读为"最高点"或"最低点",导致操作时机错误。
    这是中文译词+中文思维,下游 skill 必须用此特定含义。
  tags: [term, core-concept, decision-point]

- id: g02
  term: 止损
  type: term
  source_chapter: 第四章 + 第五章
  author_definition: |
    "你必须有个止损点,这个止损点不应超出投资额的20%。
    在选买点的最最重要点是选择止损点。即在你进场之前,你必须很清楚
    若股票的运动和你的预期不合,你必须在何点止损离场。"
  key_distinction: |
    ≠ 停止损失 — 强调"执行",而非"认知"
    ≠ 风险控制 — 止损是规则的强制执行,不只是策略
    ≠ 心理准备 — 必须变成下意识行动,不能"考虑"
    = 预设价格点位+强制执行,亏损到此点必然卖出
  why_it_matters: |
    "止损"一词在所有投资 skill 都会出现。
    字典义: "停止损失",仅是认知;作者用法: 强制执行的动作。
    如果沿用字典义,会建议用户"考虑止损",这是错的,必须"执行止损"。
  tags: [term, core-concept, risk-management]

- id: g03
  term: 截短亏损,让利润奔跑
  type: term
  source_chapter: 第四章 + 第三章
  author_definition: |
    "华尔街将炒股的诀巧归纳成两句话:截短亏损,让利润奔跑!
    英文叫 Cut loss short, let profit run!
    意思即是一见股票情况不对,即刻止损,把它缩得越短越好!
    一旦有了利润,就必须让利润奔跑,从小利润跑成大利润。"
  key_distinction: |
    ≠ 简单的"少亏多赚" — 强调动作的不对称性
    ≠ 风险管理的"分散" — 强调单笔交易的时间结构
    = 亏损端:快速(分钟级)退出;盈利端:耐心(周/月级)持有
  why_it_matters: |
    这是策略性术语,不是心理建议。
    字典用法: "赚的比亏的多" — 数学期望;
    作者用法: 强制时间结构 — 在交易执行层面的具体动作。
    下游 skill 必须以"动作"形式表达,不能停留在"心态建议"。
  tags: [term, core-concept, asymmetric-strategy]

- id: g04
  term: 临界点四阶段
  type: term
  source_chapter: 第二章 第二节
  author_definition: |
    "任何正常的股票运动都分为四个阶段:
    1.牛皮阶段(Price Consolidation) 2.正常升势
    3.疯狂阶段(Over-bought Region) 4.最后阶段(End of Bull Market)"
  key_distinction: |
    ≠ 经济周期 — 这是个股走势图模式,非宏观经济周期
    ≠ 趋势阶段 — 强调"牛皮"和"疯狂"两个非趋势阶段
    = 个股走势的完整循环:无方向→上升→狂热→崩溃
  why_it_matters: |
    这是技术分析的核心框架,所有"何时买/卖"的判断都基于此。
    字典义: "阶段"无具体定义;作者用法: 四种特定状态及其特征。
    错过"牛皮"和"最后"两个阶段会导致追高杀跌。
  tags: [term, framework, technical-analysis, market-cycle]

- id: g05
  term: 基础分析
  type: term
  source_chapter: 第二章
  author_definition: |
    "基础分析(Company-specific Catalysts)指的是:公司经营情况、盈利增长、
    新产品上市、股票回购等。一般而言,股票的价格会随着这些因素的影响而变动。
    一些公司,这些因素是明显且可预见的;但其他一些公司,这些因素则充满风险和不确定性。"
  key_distinction: |
    ≠ 财务报表分析 — 作者主要看催化剂而非数字
    ≠ 估值分析 — 不强调PE/PB等指标
    = 关注"事件+趋势"而非"静态数字"
  why_it_matters: |
    字典义: "基础分析"= 财务报表分析;
    作者用法: 强调公司层面的变化驱动(盈利增长、新产品、回购)。
    在临界点判断时,基础分析提供"为什么涨"的逻辑,不是"现在是不是低估"。
  tags: [term, analysis-method, fundamental]

- id: g06
  term: 技术分析
  type: term
  source_chapter: 第二章
  author_definition: |
    "技术分析(Price Action Signals)指的是:利用股票过去的价格、成交量、
    运动轨迹等研究股票将来的走向。图表派主要参考这张图表,
    以便一眼看出股票在升还是在跌。"
  key_distinction: |
    ≠ 财务分析 — 关注价格本身而非基本面
    ≠ 预测未来 — 关注模式识别而非精确预测
    = 利用历史数据找"形态+临界点"以提高入场胜算
  why_it_matters: |
    字典义: 技术分析=用图表预测;
    作者用法: 强调"提高获胜概率"而非"准确预测"。
    这决定了下游 skill 应表达为"概率增强工具"而非"预测工具"。
  tags: [term, analysis-method, technical]

- id: g07
  term: 大市
  type: term
  source_chapter: 第二章 第三节
  author_definition: |
    "炒股是概率的游戏,逆大潮流而动,你的获胜概率就被大打折扣了。
    将大市和单独股票结合起来考虑,是专业炒手们必须培养的心态。
    大市不好时,别买任何股票。"
  key_distinction: |
    ≠ 行业板块 — 大市是整个市场(指数级别)
    ≠ 个股趋势 — 大市是系统性的,影响所有股票
    = 整体市场(牛/熊/盘整)的状态,是胜率的乘数
  why_it_matters: |
    中文金融术语,但作者用法有特殊性: 大市>个股,优先级更高。
    字典义: 大市=大盘;作者用法: 大市是决策的最高层过滤器。
    下游 skill 必须表达为"先看大市,再看个股"的分层决策。
  tags: [term, market-context, top-down]

- id: g08
  term: 正常升势
  type: term
  source_chapter: 第二章 第二节
  author_definition: |
    "正常升势(Normal Run)的技术走势特征是一浪高过一浪。
    浪谷及浪峰均递进升高。
    在一浪高过一浪的走势形态下,股票的活动范围不断扩展,
    股票价格通常会从最低价升至最高价的120%或130%甚至更高。"
  key_distinction: |
    ≠ 一般上升趋势 — 强调"波浪形态"和"一浪高过一浪"
    ≠ 强势股 — 强调技术形态特征而非市场表现
    = 有序的、可识别的上升形态,伴随交易量配合
  why_it_matters: |
    这是判定"是否加仓""是否继续持有"的核心信号。
    字典义: "升势"= 上升趋势;作者用法: 具体形态特征(浪谷浪峰递进+交易量配合)。
  tags: [term, technical-pattern, bullish-trend]

- id: g09
  term: 移动止损
  type: term
  source_chapter: 第四章 第二节
  author_definition: |
    "你可以将止损点放在每个波浪的浪谷,随着波浪往上翻,
    你将卖点由A->B->C->D->E往上移。
    这样就能保证你不会在升势时过早离场。"
  key_distinction: |
    ≠ 固定止损 — 是动态的,随股价上移
    ≠ 追踪止损(Trailing Stop) — 中文译法可能不同,但本质一致
    = 随升势上移的动态止损,保护既有利润
  why_it_matters: |
    这是"让利润奔跑"原则的具体执行机制。
    字典义: 无此特定术语;作者用法: 浪谷递进的动态止损点。
    下游 skill 必须表达为"随浪谷上移"的规则,不是简单的"止损上移"。
  tags: [term, technique, dynamic-stop, profit-protection]

- id: g10
  term: 套牢
  type: term
  source_chapter: 第一章 第三节
  author_definition: |
    "我每次看到中文中'套牢'、'割肉'等英文所没有的词汇,都要拍案叫绝。
    发明这些名词的人真应得诺贝尔文学奖!这些字正好描述着此种行为
    乃至其心理——被套住了——动弹不得——只能任人宰割。"
  key_distinction: |
    ≠ 浮亏 — 浮亏可继续持有,套牢强调被动心理
    ≠ 止损失败的代名词 — 套牢是"舍不得止损"的状态
    = 持有亏损仓位且不愿止损,被市场"套住"的心理状态
  why_it_matters: |
    这是中文特有的文化-心理复合术语,英文无对应词。
    它不是单纯描述亏损,而是描述"人性弱点+亏损"的状态。
    下游 skill 需要特别处理: 文化-心理层面的术语,仅中文适用。
  tags: [term, chinese-specific, psychological-state, failure-mode]

- id: g11
  term: 临界点四阶段之"牛皮阶段"
  type: term
  source_chapter: 第二章 第二节
  author_definition: |
    "牛皮阶段(Price Consolidation)指的是在阻力线和支撑线之间徘徊震荡。
    它不升不跌,似牛皮一样坚韧。"
  key_distinction: |
    ≠ 盘整 — 强调"无方向"而非"小幅波动"
    ≠ 缩量整理 — 不强调成交量特征
    = 价格在支撑/阻力线间无方向震荡
  why_it_matters: |
    这是临界点四阶段的第一阶段,操作意义:不入场,等待方向。
    字典义: "牛皮"= 顽抗;作者用法: 金融市场专门术语=无方向震荡。
  tags: [term, technical-pattern, consolidation]

- id: g12
  term: 临界点四阶段之"最后阶段"
  type: term
  source_chapter: 第二章 第二节
  author_definition: |
    "最后阶段(End of Bull Market)股票处于狂热状态,价格大幅上涨,
    但交易量异常放大,常常是机构出货的信号。
    危险信号:交易量暴增但股价不涨、两天转头、升势末期出现坏消息等。"
  key_distinction: |
    ≠ 顶部 — "最后阶段"是过程,不一定是最高点
    ≠ 熊市开始 — 是"牛市的最后一段"
    = 上升末段,机构出货,价格仍可升但风险极高
  why_it_matters: |
    这是清仓信号最密集的阶段,识别此阶段=识别逃顶时机。
    字典义: 无;作者用法: 特定的市场状态,机构出货的窗口。
  tags: [term, technical-pattern, bull-market-end, exit-signal]

- id: g13
  term: 学股四阶段
  type: term
  source_chapter: 第八章
  author_definition: |
    "我在这里就以自己的学股历程谈谈学股经过的阶段:
    一、蛮干阶段 — 不知为何买也不知为何卖
    二、摸索阶段 — 借鉴别人的经验,边学边用
    三、体验风险阶段 — 经历了大亏,痛定思痛
    四、久赌必赢阶段 — 规则内化,耐心等待机会"
  key_distinction: |
    ≠ 学习曲线 — 强调阶段不可跳越
    ≠ 技能等级 — 不是"高级 vs 低级",是"必经顺序"
    = 投资者从新手到稳定的心理+行为进化路径
  why_it_matters: |
    这是个"元框架",让自我定位和成长规划有据可依。
    字典义: 无;作者用法: 个人成长模型,5-6年完成。
    下游 skill 可用作"用户当前能力评估"的分类工具。
  tags: [term, learning-model, expertise, stage-theory]

- id: g14
  term: 假象(经济史观)
  type: term
  source_chapter: 第七章
  author_definition: |
    "经济史是一部基于假象和谎言的连续剧,经济史的演绎从不基于真实的剧本,
    但它铺平了累积巨额财富的道路。做法就是认清其假象,投入其中,
    在假象被公众认识之前退出游戏。"
  key_distinction: |
    ≠ 欺诈 — 假象是集体共同相信的故事,不一定是骗局
    ≠ 错误 — 假象在特定时间内"有效",推动价格上升
    = 投资者群体的共同信念,虽然不符合最终事实,但在短期内自我实现
  why_it_matters: |
    这是索罗斯反身性理论的简化版,是泡沫参与的核心理论基础。
    字典义: 假象=虚假的表象;作者用法: 市场结构性信念,有可利用性。
    下游 skill 在讨论"泡沫参与"时必须用此特定含义。
  tags: [term, philosophical, bubble-theory, reflexivity]

- id: g15
  term: 久赌必赢
  type: term
  source_chapter: 第三章 第二节
  author_definition: |
    "久赌必赢的技巧在于每次下注,你的获胜概率必须超过50%,
    只要你只下本金的小部分,不会为几次坏运气就剃光头,
    从长期而言你是胜定了。"
  key_distinction: |
    ≠ 赌博必赢 — 强调"概率优势+小注"两个前提
    ≠ 投资必赚 — 承认单次可能亏,长期必赢
    = 长期正期望值策略,需要满足两个数学条件
  why_it_matters: |
    这是全书的数学基础,把"炒股"从赌博转为正期望值游戏。
    字典义: 无;作者用法: 数学期望+仓位管理的复合策略。
    下游 skill 必须用数学语言表达,不能用模糊的"心态好就会赢"。
  tags: [term, mathematical, expectation-value, strategy]
