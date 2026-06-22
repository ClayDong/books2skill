# 炒股的智慧 — 决策场景候选 (decision-extractor 产出)

> 阶段1.5 会做去重,这里宁多勿少。
> 本书为"实操类",采用直接提取策略:作者明确讨论"面对X时应该怎么决定"。

- id: d01
  title: 入场前是否买这只股票?
  type: decision-scene
  source_chapter: 第四章 第一节 何时买股票
  decision_scenario: |
    面对一只候选股票,是否在当前价位买入?
    这是股票投资最核心的决策,需要从"我能不能赚"转变为"我亏得起多少"的视角。
  decision_variables:
    - 当前价格 vs 内在价值(基础分析)
    - 股票所处阶段(技术分析)
    - 大市走向(牛/熊)
    - 入场后最大可承受亏损(止损线)
    - 风险报酬比(至少1:3)
  decision_flow: |
    1. 基础分析:该公司经营情况、盈利增长、新产品/回购等
    2. 大市判断:大市处于牛市还是熊市?熊市不买
    3. 阶段判断:股票处于哪个阶段(牛皮/正常升势/疯狂/最后)
    4. 临界点判断:是否在突破点/支撑位/交易量配合的入场时机
    5. 止损点设定:在入场前先定止损点(不超过总投资额20%)
    6. 仓位计算:根据止损距离反推仓位
    7. 分层下注:先买20%试仓,验证后再加仓
  bound_to_methodology:
    - f01 临界点决策模型
    - f02 概率思维框架
    - f04 大势优先框架
    - f09 临界点买股三层过滤模型
    - f10 分层下注资金管理
  common_traps:
    - 看到"已经涨了"就跟买,而不是看是否在临界点
    - 没有止损点就开始买入
    - 大市不好时强行选股
    - all-in 而非分层下注
  applicable_scope: 投资决策 > 个股入场决策
  tags: [decision, entry-timing, stock-purchase, critical-decision]

- id: d02
  title: 持仓后是否止损离场?
  type: decision-scene
  source_chapter: 第五章 + 第一章
  decision_scenario: |
    持仓股票跌破止损点,是否执行止损?
    这是人性最大考验——大多数人在此决策失败,导致小亏变大亏。
  decision_variables:
    - 当前价格 vs 预设止损点
    - 跌破幅度(是否触及关键支撑线)
    - 持仓理由是否仍然成立
    - 自己的情绪状态(是否在合理化)
    - 替代机会的吸引力
  decision_flow: |
    1. 对照预设止损点:是否已触及?
    2. 如果触及,先做"假设我今天没持仓,会买入吗?"测试
    3. 如果答案为否,立即执行止损
    4. 如果答案为是,审视自己是否有合理化倾向
    5. 写出卖出理由(防止"再等等"陷阱)
    6. 立即下单,不给自己反悔时间
  bound_to_methodology:
    - f06 心理训练三步法
    - p01 止损是最高行为准则
  common_traps:
    - "这次不一样,会反弹的"(确认偏误)
    - "再等等,跌更多再说"(沉没成本)
    - "基本面没变,只是技术回调"(合理化)
    - 拖延到收盘后再说(给犹豫留空间)
  applicable_scope: 投资决策 > 持仓管理决策
  tags: [decision, stop-loss, exit, emotional-control]

- id: d03
  title: 浮盈时是否卖出获利?
  type: decision-scene
  source_chapter: 第四章 第二节 + 第三章
  decision_scenario: |
    持仓股票已有账面盈利,是否在当前价位卖出?
    决策张力: 落袋为安(贪小便宜心理) vs 让利润奔跑(截短亏损让利润奔跑原则)。
  decision_variables:
    - 浮盈幅度
    - 股票所处阶段(正常升势 vs 疯狂阶段)
    - 移动止损点位置
    - 交易量是否异常(放巨量=危险信号)
    - 大市是否到顶
  decision_flow: |
    1. 评估股票阶段:仍在正常升势?还是进入疯狂阶段?
    2. 如果是正常升势:不卖,移动止损到上一浪谷
    3. 如果是疯狂阶段:开始分批卖出
    4. 检查危险信号:交易量暴增但股价不涨?两天转头?无重大利好?
    5. 任意危险信号触发:立即清仓
    6. 不试图寻找最高点,中间一截即可
  bound_to_methodology:
    - f05 移动止损加码法
    - p02 截短亏损,让利润奔跑
    - p13 涨时不要急于获利了结
  common_traps:
    - 见好就收(贪小便宜)
    - 试图精准逃顶(最高点不可知)
    - 看见"转头"就慌(其实可能是正常回调)
    - 媒体吹捧时贪心(大市到顶信号)
  applicable_scope: 投资决策 > 持仓管理决策
  tags: [decision, take-profit, exit, profit-taking]

- id: d04
  title: 大市到顶时如何退出?
  type: decision-scene
  source_chapter: 第二章 第三节 + 第七章
  decision_scenario: |
    大市持续上涨,但已经出现"大众普遍谈论赚钱"等危险信号,
    面对可能即将到来的熊市,如何调整持仓?
  decision_variables:
    - 大市指数的相对位置
    - 大众情绪(媒体、社交、街头巷尾讨论)
    - 龙头股表现(是否开始疲软)
    - 垃圾股表现(是否开始活跃=末期信号)
    - 升跌股票比例
  decision_flow: |
    1. 观察大众情绪:是否所有人都在谈论股票赚钱?
    2. 检查龙头股:是否开始疲软、停滞?
    3. 检查垃圾股:是否开始活跃上涨?(末期信号)
    4. 检查升跌比例:是否有大量股票开始跌?
    5. 任意两个信号触发:开始分批减仓
    6. 减仓时使用移动止损,锁定部分利润
    7. 不试图逃顶,而是分批撤退
  bound_to_methodology:
    - f04 大势优先框架
    - p15 大市不好时别买任何股票
    - f07 假象参与退出框架
  common_traps:
    - "这次不一样,会继续涨"(叙事谬误)
    - 贪婪,想再多赚一点
    - 觉得"已经赚了,跌一点也没事"
    - 媒体说"还会涨"就信
  applicable_scope: 投资决策 > 大市仓位决策
  tags: [decision, market-top, bubble, exit-timing]

- id: d05
  title: 面对泡沫是否参与?
  type: decision-scene
  source_chapter: 第七章 抓住大机会
  decision_scenario: |
    面对一个明显的泡沫(房地产、股票、新概念),
    是参与(买入)在退出前获利,还是完全不参与?
  decision_variables:
    - 泡沫的相对阶段(早期/中期/晚期)
    - 假象的"持续力"(基本面是否还能撑一阵)
    - 自己的退出纪律
    - 资金规模和风险承受力
    - 对泡沫破裂的判断能力
  decision_flow: |
    1. 评估自己是否能识别"假象"(前提:能识别才有资格参与)
    2. 评估自己的退出纪律(不能严格退出的不参与)
    3. 如果选择参与:小仓位、明确退出信号
    4. 设定"只要X信号出现就清仓"的硬规则
    5. 写下来,贴在显眼处,防止临场改变
    6. 严格执行,不在退出时犹豫
  bound_to_methodology:
    - f07 假象参与退出框架
    - p11 股市从来不会错
  common_traps:
    - 自认为能识别顶部,实际不能
    - 没有退出规则就参与
    - 退出规则被"再多赚一点"心理破坏
    - 资金量超出自己能承受损失的规模
  applicable_scope: 投资决策 > 泡沫参与决策
  tags: [decision, bubble, reflexivity, contrarian]

- id: d06
  title: 是否加仓——浮盈后是否扩大战果?
  type: decision-scene
  source_chapter: 第三章 第一节
  decision_scenario: |
    已有持仓浮盈(买入后上涨),是否在此基础上加仓?
    决策张力: 让利润奔跑 vs 见好就收 / 加仓的边际风险。
  decision_variables:
    - 浮盈幅度
    - 加仓后的风险敞口
    - 总仓位是否超出风险承受力
    - 加仓的临界点是否可靠
  decision_flow: |
    1. 确认"第一次入场的判断正确"——这是加仓的前提
    2. 检查总仓位:加仓后是否超过风险承受力?
    3. 评估新加仓位的新止损点
    4. 如果止损点合理且判断正确,加仓
    5. 永远不要在纸面无利润时加仓(见p09)
  bound_to_methodology:
    - f10 分层下注资金管理
    - p02 截短亏损,让利润奔跑
  common_traps:
    - 在纸面无利润时加仓(沉没成本陷阱)
    - 加仓过度导致单股风险集中
    - 取消原止损点(更危险)
  applicable_scope: 投资决策 > 仓位管理决策
  tags: [decision, position-sizing, add-to-winner, trailing-add]

- id: d07
  title: 何时空仓等待机会?
  type: decision-scene
  source_chapter: 第三章 + 第八章
  decision_scenario: |
    当前没有值得买入的标的,是否空仓等待?
    决策张力: 空仓=没钱赚的焦虑 vs 强行选股=亏钱的风险。
  decision_variables:
    - 大市环境(熊市/盘整/牛市)
    - 候选标的的胜算
    - 现金的机会成本
    - 自身的耐心和纪律
  decision_flow: |
    1. 检查大市:熊市或盘整期,优先空仓
    2. 评估候选标的:没有1:3风险报酬比的机会,不入场
    3. 检查自身状态:对市场有感觉?还是感到迷茫?
    4. 如果迷茫,执行p06"有疑问,离场"——空仓
    5. 写明空仓条件(什么信号出现才再次入场)
    6. 定期(如每周)检查条件,无信号则继续空仓
  bound_to_methodology:
    - p06 有疑问,离场
    - p15 大市不好时别买任何股票
    - f08 学股四阶段
  common_traps:
    - "不操作就是浪费时间"的心理压力
    - 强行选股以"证明自己在做事"
    - 听到别人赚钱而焦虑入场
  applicable_scope: 投资决策 > 仓位决策
  tags: [decision, cash-position, patience, market-timing]

- id: d08
  title: 何时把已有投资转换为现金?
  type: decision-scene
  source_chapter: 第三章 第一节 + 第六章
  decision_scenario: |
    已有持仓但对市场走势失去感觉,是否清仓观望?
    适用于: 趋势不明、自己对操作不自信、关键事件前。
  decision_variables:
    - 持仓的理由是否仍然成立
    - 持仓盈亏状态(是否在合理化)
    - 自己对市场的判断
    - 未来关键事件的时间表
  decision_flow: |
    1. 问自己:如果今天没持仓,会买入吗?
    2. 如果答案是"不知道"或"不会":清仓
    3. 如果答案是"会":保持
    4. 如果有重大事件(政策、业绩、地缘)临近:考虑减仓等待
    5. 清仓不等于退出市场,而是转换状态
  bound_to_methodology:
    - p06 有疑问,离场
    - p10 忘掉入场价
    - p11 股市从来不会错
  common_traps:
    - 因浮亏而"不舍得"卖
    - 因浮盈而"贪图"更多
    - 因沉没成本而"硬扛"
  applicable_scope: 投资决策 > 持仓管理
  tags: [decision, cash-out, exit, re-evaluation]

- id: d09
  title: 资金应分散到几只股票?
  type: decision-scene
  source_chapter: 第五章
  decision_scenario: |
    决定投资时,应分散到几只股票?
    决策张力: 分散降低单股风险 vs 过度分散降低跟踪质量。
  decision_variables:
    - 资金总量
    - 候选标的数量和质量
    - 自己能跟踪研究的时间
    - 各标的相关性(同行业=低分散)
  decision_flow: |
    1. 评估资金量:5万以下→3-5只,大资金→可分散到10-20只
    2. 评估自己的研究时间:能每周跟踪多少只?
    3. 评估候选标的相关性:不要都买科技股
    4. 选定分散数量后,每只分配大致相等的资金
    5. 设定"超过N只就不再买入"的硬规则
  bound_to_methodology:
    - p05 分散风险
    - p07 避免买太多股票
  common_traps:
    - 过度集中(单股爆仓风险)
    - 过度分散(跟踪不过来,变 ETF 化)
    - 集中在同行业(伪分散)
  applicable_scope: 投资决策 > 资产配置
  tags: [decision, diversification, portfolio-construction]

- id: d10
  title: 模拟仓的失败是否影响真仓决策?
  type: decision-scene
  source_chapter: 第六章 心理建设
  decision_scenario: |
    模拟交易或纸上模拟显示某种方法可行,是否在真实资金中应用?
    决策张力: 模拟成功→真仓操作 vs 模拟和实战的心理差异。
  decision_variables:
    - 模拟盘的时间跨度
    - 模拟与实战的资金规模差异
    - 心理压力差异
    - 模拟的统计样本量
  decision_flow: |
    1. 检查模拟时间是否足够长(>1年,经历牛熊)
    2. 检查模拟是否包含完整的心理压力(模拟时心不痛)
    3. 真仓从最小规模开始(总资金的5-10%)
    4. 表现稳定后逐步加码
    5. 任何"感觉不一样"出现,立即回到小规模
  bound_to_methodology:
    - f10 分层下注资金管理
    - f06 心理训练三步法
  common_traps:
    - 模拟成功就认为真仓也会成功
    - 心理压力使真仓表现远差于模拟
    - 一次真仓成功就过度加码
  applicable_scope: 投资决策 > 策略应用
  tags: [decision, paper-trading, real-money, scaling-up]

- id: d11
  title: 学股到哪个阶段了?
  type: decision-scene
  source_chapter: 第八章 学股的四个阶段
  decision_scenario: |
    自我评估当前炒股能力水平,在"蛮干→摸索→体验风险→久赌必赢"四阶段中处于哪一阶段?
    这是个元决策: 决定下一步该补什么课、做什么调整。
  decision_variables:
    - 操作是否有系统
    - 是否有经历重大亏损
    - 是否能从亏损中学习
    - 是否能稳定执行规则
    - 长期是否盈利
  decision_flow: |
    1. 检查操作是否有系统(蛮干=无系统)
    2. 检查是否经历重大亏损(摸索=未经历)
    3. 检查是否从亏损中学习(体验风险=经历并反思)
    4. 检查是否能稳定执行规则(久赌必赢=规则内化)
    5. 对照各阶段特征,定位自己
    6. 决定下一步:蛮干→学基础,摸索→做小仓位,体验风险→反思复盘,久赌必赢→优化系统
  bound_to_methodology:
    - f08 学股四阶段模型
    - p17 优秀投资者共同素质
  common_traps:
    - 误判自己的阶段(自认为"摸索"实际是"蛮干")
    - 跳过体验风险阶段(未真正经历重大亏损)
    - 给自己贴"久赌必赢"标签但其实做不到
  applicable_scope: 元决策 > 能力评估
  tags: [decision, self-assessment, learning-stage, meta-decision]
