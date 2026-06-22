# 炒股的智慧 — 反例候选 (counter-example-extractor 产出)

> 阶段1.5 会做去重,这里宁多勿少。
> 反例是阶段2的B(Boundary)段核心素材。

- id: ce01
  title: 频繁交易导致的失败模式
  type: counter-example
  source_chapter: 第五章 华尔街的家训
  source_quote: |
    "我开始专职炒股的时候,每天不买或卖上一次就觉得自己没完成当天的工作。
    结果我为此付出了巨额的学费。当经验累积到一定地步,你就会明白股市不是每天都有盈利机会的。
    频繁交易常常是因为枯燥无聊。频繁交易不仅损失手续费,同时使交易的质量降低。"
  failure_mode: |
    把"每天交易"作为任务完成的心态,导致无信号交易、情绪化进出、手续费侵蚀利润。
  mechanism: |
    把"过程"当"目的"——把交易行为本身当作工作产出,而非用规则过滤信号。
    行为经济学: 行动频率与"忙碌感"满足感正相关,但与实际收益无关。
    心理上,空仓=无产出=焦虑,触发"做点什么"的冲动。
  warning_signs:
    - 每天不交易就觉得"无事可做"
    - 持仓时间<3天
    - 交易决策主要由"无聊"或"焦虑"驱动
    - 手续费占账户亏损的显著比例
  bound_to:
    - "p08 别频繁交易"
    - "f02 概率思维"
  tags: [counter-example, frequency-trap, transaction-cost]

- id: ce02
  title: 向下摊平导致的破产
  type: counter-example
  source_chapter: 第五章
  source_quote: |
    "英国的巴林银行就这样全了。上海石化在美国挂牌上市,1997年最高曾达到每股45美元。
    从45跌到35,很低了吧?是不是再补上2000股?再跌到25美元,你准备怎么办?
    结果上海石化一路跌到每股10美元。"
  failure_mode: |
    在亏损时持续加仓以"摊低成本",等待反弹解套。
    实际效果: 亏损扩大、单股风险集中、最终可能全损。
  mechanism: |
    沉没成本谬误: 既然已经投入,放弃=承认损失,加仓=可能翻本。
    锚定效应: 以买入价为参照系,而非以当前价为新起点。
    赌博谬误: "已经跌了这么多,该反弹了"——但实际上下跌无下限。
  warning_signs:
    - 持有亏损仓位的理由是"等反弹回本"
    - 计划"再补一点,降低成本"
    - 用"价值投资"为加仓辩解,实际是套牢
  bound_to:
    - "p09 不要向下摊平"
    - "p10 忘掉入场价"
  tags: [counter-example, sunk-cost, position-averaging, barings-bank]

- id: ce03
  title: 贪小便宜导致赚小亏大
  type: counter-example
  source_chapter: 第一章 第三节
  source_quote: |
    "好获小利,买进的股票升了一点,便迫不及待地脱手。
    这只股票或许有75%继续上升的机会,但为了避免25%什么都得不到的可能性,
    股民宁可少赚些。结果是可能有5000元利润的机会,你只得到500元。
    任何炒过股的读者都明白,要用较出场价更高的价位重新入场是多么困难。"
  failure_mode: |
    在小额盈利时立即兑现,而在亏损时死扛不止损,导致整体收益结构严重负偏。
  mechanism: |
    损失厌恶(卡尼曼): 损失100的痛苦>获得100的快乐2倍。
    短期确定性偏好: 兑现"已得"的小利 > 等待"或得"的大利。
    卖出后悔vs.继续持有后悔的非对称性: 卖早了不痛(钱到手了),
    卖晚了痛(纸面变实际亏损),于是选择过早卖出去。
  warning_signs:
    - 盈利单平均持仓时间 < 亏损单平均持仓时间
    - 频繁说"赚了一笔,落袋为安"
    - 对"浮盈"感到焦虑,想"锁定"
  bound_to:
    - "p02 截短亏损,让利润奔跑"
    - "p13 涨时不要急于获利了结"
  tags: [counter-example, loss-aversion, profit-taking, disposition-effect]

- id: ce04
  title: 死扛不止损——套牢陷阱
  type: counter-example
  source_chapter: 第一章 第三节
  source_quote: |
    "而一旦买进的股票跌了,股民便死皮赖脸不肯止损,想像出各种各样的理由说服自己
    下跌只是暂时的。其真正的原因只不过为了搏那25%可能全身而退的机会!
    结果是小亏慢慢积累成大亏。每次我看到中文中'套牢'、'割肉'等英文所没有的词汇,
    都要拍案叫绝。发明这些名词的人真应得诺贝尔文学奖!"
  failure_mode: |
    亏损时不执行止损,期待反弹,导致小亏变中亏、中亏变大亏、大亏变套牢。
  mechanism: |
    处置效应(disposition effect): 倾向于卖出盈利,持有亏损。
    确认偏误: 只看支持"会反弹"的信息,忽略支持"会继续跌"的信息。
    合理化心理: 为不执行止损编造理由(基本面好、长期看好、暂时回调等)。
  warning_signs:
    - 买入后价格下跌,未触发止损
    - 反复说"这只是暂时的"
    - 找各种理由(基本面、行业、政策)支持"再等等"
    - "解套"成为主要持仓目标
  bound_to:
    - "p01 止损是最高行为准则"
    - "p11 股市从来不会错"
  tags: [counter-example, disposition-effect, confirmation-bias, loss-accumulation]

- id: ce05
  title: 过度自信——天才选太多
  type: counter-example
  source_chapter: 第一章 第一节
  source_chapter_id: 1
  source_quote: |
    "随着时间的推移和阅历的增加,我慢慢感悟这些聪明人失败的原因大约有两个:
    一、炒股的技能太活了;二,他们太聪明,选择太多。炒股是有技术的。
    '股票市场是有经验的人获得很多金钱,有金钱的人获得很多经验的地方。'"
  failure_mode: |
    高学历、高智商的人在股票市场反而失败,因"选择太多"分散了注意力和深耕度。
  mechanism: |
    选择悖论: 选择越多,决策越难,执行力越差。
    浅尝辄止: 聪明人尝试多种方法都未深入,每种都未到精通。
    替代效应: 失败后转向其他"看起来更容易"的机会,永不积累。
  warning_signs:
    - 同时关注超过20只股票
    - 同时使用超过3种不同的分析方法
    - 频繁更换策略,每种策略用时<1年
  bound_to:
    - "p07 避免买太多股票"
    - "f08 学股四阶段"
  tags: [counter-example, choice-overload, overconfidence, strategy-switching]

- id: ce06
  title: 不知止损规则的含义——技术性误用
  type: counter-example
  source_chapter: 第四章 第一节
  source_quote: |
    "如果对公司的判断正确且在适合的价位进场,你最终会看到股票价值。
    第三, 你必须独立思考。如果你自认不具备足够的知识来做判断,最好就不要做任何判断。
    第四, 你必须有自信,这自信必须来自知识和经验,并非一时的头脑发热。
    第五, 不要不懂装懂,要有自知之明。对自己不懂的东西,要承认自己不懂。"
  failure_mode: |
    设定止损规则但未真正理解其作用,导致规则流于形式,实际执行时仍受情绪驱动。
  mechanism: |
    规则字面遵守 vs. 规则精神理解: 即使止损规则被写下来,如果内心不认同
    (例如认为"公司是好公司,跌了不该卖"),在真正触及止损线时仍会犹豫。
  warning_signs:
    - 写了止损规则但经常"灵活处理"
    - 触及止损位时,说服自己"这次不一样"
    - 规则被情绪不断修改
  bound_to:
    - "p01 止损是最高行为准则"
    - "f06 心理训练三步法"
  tags: [counter-example, rule-flexibility, half-hearted, false-discipline]

- id: ce07
  title: 模仿成功者但不知其条件
  type: counter-example
  source_chapter: 第五章 第二节
  source_quote: |
    "我花了整整五年的时间才觉得自己能理智地玩炒股游戏。
    那些著名的炒股名家,在他们成'家'之前通常都有一次甚至几次的破产经历。
    其中包括本书中提到的利物莫和巴鲁克。"
  failure_mode: |
    看到大师的盈利方法就模仿,但忽视大师的前置条件(5-6年学股、破产经历、独立思考等)。
  mechanism: |
    表层模仿谬误: 模仿"做什么"但不模仿"具备什么条件才做"。
    幸存者偏差: 只看到成功者,看不到同样方法失败的沉默大多数。
    时间尺度忽视: 大师5-6年学股,模仿者期望5-6个月见效。
  warning_signs:
    - "我也要像巴菲特一样买股票"
    - 不理解大师方法的前提就照搬
    - 期望短时间内复制成功路径
  bound_to:
    - "f08 学股四阶段模型"
    - "p17 优秀投资者共同素质"
  tags: [counter-example, surface-imitation, survivorship-bias, time-horizon]

- id: ce08
  title: 否认市场——"这次不一样"
  type: counter-example
  source_chapter: 第七章 抓住大机会
  source_quote: |
    "回头想想,人们会嘲笑当年的民众真是疯了。当年也不是没有头脑清醒的人,
    但他们太早了一步,他们指出这个泡沫会破碎,但市场用不断升高证明他们论断的错误。
    开始还有人听听他们的警钟,随后便嘲笑他们的短视。"
  failure_mode: |
    在泡沫中坚持"这次不一样"的判断,认为传统估值标准已不适用。
  mechanism: |
    锚定迁移: 把"最近的高价"作为新的"正常"参考点。
    适应性预期: 价格持续上涨使预期不断上调。
    叙事谬误: 为高价编造合理故事(新经济、互联网革命等)。
  warning_signs:
    - "这次是结构性变革,旧规则不适用"
    - 估值指标"已过时"
    - 嘲笑看空者为"老脑筋"
  bound_to:
    - "f07 假象参与退出框架"
    - "p11 股市从来不会错"
  tags: [counter-example, narrative-fallacy, adaptive-expectations, this-time-is-different]

- id: ce09
  title: 忽视系统性风险——逆大市操作
  type: counter-example
  source_chapter: 第二章 第三节
  source_quote: |
    "我发觉新手(我自己以前也是一样)用很多心思研究单独股票的基础层面和技术层面,
    认为再好的市场也有股票跌,再坏的市场也有股票升,所以忽视大市的走向。
    我要在这里强调:炒股是概率的游戏,逆大潮流而动,你的获胜概率就被大打折扣了。"
  failure_mode: |
    只关注个股分析,忽视大市(大盘)走向,在熊市中坚持买入,导致个股选择再准确也被β拖累。
  mechanism: |
    局部-整体忽视: 个股研究带来的"我能选对"的自信,系统性低估市场整体下行风险。
    主动选择偏差: 选择"研究充分"的个股,系统性忽视"研究不足"的大市。
  warning_signs:
    - 用大部分时间研究个股,几乎不研究大市
    - "再坏的市场也有股票升"作为持仓理由
    - 熊市中满仓持有
  bound_to:
    - "f04 大势优先框架"
    - "p15 大市不好时别买任何股票"
  tags: [counter-example, beta-blindness, micro-macro-mismatch, contrarian-foolishness]

- id: ce10
  title: 知行不一——"知道但做不到"
  type: counter-example
  source_chapter: 第三章 + 第六章
  source_quote: |
    "影响股票升落的因素就是这么多,真正重要的因素列出为占不满你的手指,
    甚至不识字的也可以在股市露一手。这样的行业,成功率甚至低过减肥!
    为什么?因为人们常常做不到自己知道应该做的事情!"
  failure_mode: |
    知道正确的原则(止损、让利奔跑、分散等)但在实际操作中无法坚持。
  mechanism: |
    知识-行动鸿沟: 知道 vs. 做之间的鸿沟是失败主因。
    即时满足偏好: 短期获利的快乐 > 长期遵守原则的好处。
    自我合理化: 每次违规都找理由("这次不一样"、"手续费不划算"等)。
  warning_signs:
    - 知道止损但经常不执行
    - 知道"不要频繁交易"但仍每天买卖
    - 知道"不要向下摊平"但在亏损时加仓
  bound_to:
    - "p18 普通人做不到自己知道该做的事情"
    - "f06 心理训练三步法"
  tags: [counter-example, knowledge-action-gap, akrasia, self-deception]

- id: ce11
  title: 跟随大流——高位接盘
  type: counter-example
  source_chapter: 第二章 第三节
  source_quote: |
    "你如果随大流,则你将常常在高点入市,低点出市,你将成为失败者。
    长期以来我们已习惯于'集体思维'。但炒股需要不同的思维方式。
    如果股市大多数人都看好某股票,他们都已按自己的能力入场,
    还有谁来买股使股市继续升得更高?"
  failure_mode: |
    跟随大众情绪买入,在"人人都谈论股票"时入场,在最低点出市。
  mechanism: |
    群体思维: 在不确定情境下,倾向于跟随他人行为。
    信息级联: 观察到他人买入→推断有信息→跟进→形成正反馈。
    错失恐惧(FOMO): "再不上车就来不及了"。
  warning_signs:
    - "大家都在买"
    - "我邻居/同事都赚钱了"
    - 媒体报道"全民炒股热"
  bound_to:
    - "f04 大势优先框架"
    - "p15 大市不好时别买任何股票"
  tags: [counter-example, herd-mentality, FOMO, late-entry]

- id: ce12
  title: 报复性加倍下注——赌徒谬误
  type: counter-example
  source_chapter: 第一章
  source_quote: |
    "人好报复,所以犹如赌徒一般,输了一手,下一手下注就加倍,
    再输,再加倍,于是剃光头的时间又加快了。"
  failure_mode: |
    亏损后加倍的赌徒行为,期望"赢一次回本",结果加速破产。
  mechanism: |
    赌徒谬误: 错误认为"连输后必赢一次"。
    复仇心理: 把市场视为"对手",亏损=被对手打败,要"报仇"。
    仓位管理崩溃: 风险敞口在情绪驱动下非线性放大。
  warning_signs:
    - 亏损后仓位翻倍
    - "这一次一定要赚回来"
    - 把亏损归因于"运气不好"而非"判断错"
  bound_to:
    - "p01 止损是最高行为准则"
    - "p03 20%止损硬线"
  tags: [counter-example, gamblers-fallacy, revenge-trading, position-escalation]

- id: ce13
  title: 买自己不懂的生意
  type: counter-example
  source_chapter: 第五章 第二节 巴菲特
  source_quote: |
    "我只能进行我所熟悉的投资方式。这样做或许会失去一些巨额且容易的盈利机会。
    但我不能进行我不熟悉的投资方式,因为这可能导致巨额的损失。"
    "对投资的对象可以有弹性。什么生意都可以买,但不要付出超出其价值的价格。"
  failure_mode: |
    投资超出自己能力圈的公司,即使最终可能盈利,过程中的不确定性使判断失误风险剧增。
  mechanism: |
    能力圈错位: 在自己不懂的领域做判断,准确率随机(50%)。
    故事谬误: 被"动人故事"吸引,忽视自己是否真懂其价值。
  warning_signs:
    - "这家公司做什么的?" 答不上来
    - 买入理由是"大家都在买"或"看起来会涨"
    - 无法用自己的话说清公司靠什么赚钱
  bound_to:
    - "f08 学股四阶段"
    - "p15 大市不好时别买任何股票"
  tags: [counter-example, circle-of-competence, story-driven, blind-investment]
