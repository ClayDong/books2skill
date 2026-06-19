# Router Prompts — 意图驱动路由层

> 本文件包含阶段 5（多书协同编排）步骤 1-3 使用的所有 prompt。
> 调用方：book2skill 元 skill 的编排层。
>
> ## 变量绑定契约
>
> | 变量 | 来源 | 取值方式 | 缺失时默认 |
> |---|---|---|---|
> | `{{USER_INTENT}}` | 用户输入 | 原始意图文本 | — |
> | `{{BOOKS_LIST}}` | library/GLOBAL_INDEX.md | 已拆书目列表 | — |
> | `{{INTENT_JSON}}` | intent-classifier 输出 | 完整 JSON | — |
> | `{{GLOBAL_INDEX}}` | library/GLOBAL_INDEX.md | 文件全文 | 报错（前置条件） |
> | `{{GLOSSARY_UNIFIED}}` | library/GLOSSARY_UNIFIED.md | 文件全文 | 跳过术语消解 |
> | `{{KNOWN_CONFLICTS}}` | library/CONFLICTS.md | 文件全文 | 空字符串 |
> | `{{CANDIDATES}}` | coarse-recall 输出 | JSON 数组 | 空数组→走兜底 |
> | `{{TOP3}}` | fine-recall 输出 | top3 字段 | — |
> | `{{DETECTED_CONFLICTS}}` | conflict-detector 输出 | conflicts 数组 | 空数组 |

---

## 1. intent-classifier（意图分类器）

**用途**：理解用户意图，分档 A/B/C，输出结构化意图对象。

```prompt
你是一个意图分类器。用户提出了一个意图，你需要：

1. 理解意图的本质（决策 / 分析 / 执行 / 学习）
2. 判断涉及领域（投资 / 职业 / 创业 / 认知 / ...）
3. 判断时间 horizon（紧急 / 短期 / 中期 / 长期 / 未知）
4. 分档：
   - A 档（简单）：单 skill 即可回答。特征：意图明确、单一领域、无冲突
   - B 档（单框架）：意图落在某本书的框架体系内，需组合该书 2-3 个 skill。特征：单一领域但需多步推理
   - C 档（多框架冲突）：意图命中多本书的冲突观点。特征：跨领域、或同领域不同流派

用户意图：{{USER_INTENT}}

已拆书目：{{BOOKS_LIST}}

输出 JSON：
{
  "intent_type": "decision|analysis|execution|learning",
  "domain": ["投资", "职业", ...],
  "time_horizon": "紧急|短期|中期|长期|未知",
  "risk_preference": "保守|中性|激进|未知",
  "reversibility": "不可逆|高成本可逆|低成本可逆|未知",
  "capital_type": "自有|借贷|混合|未知",
  "target_type": "增长|保本|套利|转型|未知",
  "tier": "A|B|C",
  "tier_reason": "为什么分这个档",
  "needs_clarification": false,
  "clarification_question": "（如需澄清）要问用户什么",
  "missing_signals": ["risk_preference", "reversibility"]
}

判断规则：
- 如果意图模糊到无法判断领域 → needs_clarification=true，提出澄清问题
- 如果 intent_type 无法从意图中唯一确定（即意图同时包含 ≥2 种 intent_type 的特征，如"我想了解投资并决定要不要买"同时是 learning + decision）→ needs_clarification=true，针对性追问（如"你想做决策还是做分析？短期还是长期？"）
  - 正例："帮我分析这个项目" → intent_type=analysis（唯一）
  - 正例："我该不该止损" → intent_type=decision（唯一）
  - 反例："我想了解投资并决定要不要买" → needs_clarification=true（learning + decision 混合）
- 如果情境信号不足（risk_preference/reversibility/capital_type/target_type 中有 ≥2 个为"未知"）→ 在 missing_signals 中列出缺失字段，供 judge-protocol 做补全提问（注意：intent-classifier 只负责识别缺失信号，不判断阈值；阈值由 judge-protocol 根据决策情境动态判断）
- 如果意图明确但只涉及单一方法论 → A 档
- 如果意图需要组合多个方法论但不冲突 → B 档
- 如果意图可能命中冲突观点（如"该不该止损"） → C 档

输出约束：必须是合法 JSON，不要包含 markdown 代码块标记或解释文字。所有字段必须存在，无法判断时用 null。
```

---

## 2. coarse-recall（粗召）

**用途**：从全局 skill 索引中召回 top-10 候选。

```prompt
你是一个粗召器。给定用户意图和全局 skill 索引，召回 top-10 候选 skill。

用户意图（结构化）：{{INTENT_JSON}}

全局 skill 索引：{{GLOBAL_INDEX}}

统一术语表：{{GLOSSARY_UNIFIED}}

召回规则：
1. 语义相关度：意图 vs skill 的 description + i_summary（I 段摘要）
2. tags 硬过滤：意图领域必须与 skill tags 有交集
3. source_book 权威性加权：authority 为 A 级的书的方法论优先（authority 来自 GLOBAL_INDEX，不是临场判断）
4. **术语消解（三步执行）**：
   - 步骤 1（召回前）：扫描意图关键词，查 GLOSSARY_UNIFIED 的 aliases，扩展召回关键词（如意图说"止损"，扩展为"止损|割肉"）
   - 步骤 2（召回时）：用扩展后的关键词集匹配 skill description 和 i_summary
   - 步骤 3（召回后）：去重——如果同一 skill 被多个 alias 召回，只保留 recall_score 最高的一条
5. 宁多勿漏：粗召目标是 recall，不是 precision

输出 JSON 数组，每条：
{
  "skill_id": "<book-slug>::<skill-slug>",
  "source_book": "书名",
  "description": "skill 的 description",
  "recall_score": 0.0-1.0,
  "recall_reason": "为什么召回这个 skill"
}

注意：
- 召回最多 10 个候选，不足时返回实际相关数量，不要凑数。如果相关 skill 超过 10 个，按 recall_score 降序取前 10
- 如果全局索引中没有相关 skill，返回空数组 []
- 如果 {{GLOSSARY_UNIFIED}} 为空或不存在，跳过术语消解步骤，直接基于意图原始关键词做语义召回。不要编造术语别名
- 不要编造不存在的 skill
- skill_id 必须能在 GLOBAL_INDEX 中找到

输出约束：必须是合法 JSON 数组，不要包含 markdown 代码块标记或解释文字。
```

---

## 3. fine-recall（精排）

**用途**：对粗召的 top-10 重排，取 top-3。冲突检测由 conflict-detector 统一负责，本 prompt 只做精排。

```prompt
你是一个精排器。对粗召的 top-10 候选 skill 重排，取 top-3。

用户意图：{{INTENT_JSON}}

候选 skill 列表：{{CANDIDATES}}

已知冲突矩阵：{{KNOWN_CONFLICTS}}

精排特征：
1. 语义相关度（意图 vs skill 的 i_summary）
2. B 段排除检查：skill 的 B 段（Boundary）是否排除了当前场景？如果是，大幅扣分
3. source_book 权威性（authority 字段）
4. 冲突感知精排：如果两个候选 skill 在 KNOWN_CONFLICTS 中存在已知冲突，都保留（用于后续 conflict-detector 检测）。如果 top-3 中存在多对冲突，全部保留；如果冲突 skill 数量 ≥3，触发 crag-evaluator 评估为 ambiguous

输出 JSON：
{
  "top3": [
    {
      "skill_id": "...",
      "rank": 1,
      "rerank_score": 0.0-1.0,
      "rerank_reason": "为什么排这个位置",
      "boundary_check": "B段是否排除当前场景 + 理由"
    }
  ]
}

注意：
- 本 prompt 只做精排，不输出冲突检测结果。冲突检测由 conflict-detector 统一负责
- 如果 {{CANDIDATES}} 为空数组，返回空 top3，由编排层直接走 crag-evaluator 评估为 incorrect + empty_recall

输出约束：必须是合法 JSON，不要包含 markdown 代码块标记或解释文字。所有字段必须存在，无法判断时用 null。
```

---

## 4. crag-evaluator（CRAG 三档评估）

**用途**：对精排结果做 CRAG 风格的三档评估，决定是否需要兜底。

**重要**：CRAG 评估的是**召回质量**，不是冲突可消解性。范式对立冲突如果召回质量高（correct），正常走 debate-protocol 呈现多元视角，**不是 fallback**。

```prompt
你是一个 CRAG 评估器。对精排结果评估，判断召回质量。

用户意图：{{INTENT_JSON}}

精排 top-3：{{TOP3}}

冲突检测结果：{{DETECTED_CONFLICTS}}

评估三档：
- correct（准确）：top-3 中至少有 1 个 skill 高度相关（rerank_score > 0.8），且 B 段不排除当前场景
- ambiguous（模糊）：top-3 有相关 skill 但置信度不高（0.5-0.8），或存在未消解的范式对立冲突
- incorrect（错误）：top-3 都不相关（rerank_score < 0.5），或召回为空

输出 JSON：
{
  "crag_tier": "correct|ambiguous|incorrect",
  "confidence": 0.0-1.0,
  "action": "proceed|degrade|fallback",
  "fallback_type": "empty_recall|irrelevant_recall|unresolvable_conflict|ambiguous_intent",
  "fallback_message": "（如需兜底）给用户的反馈消息",
  "fallback_options": ["选项1", "选项2"]
}

confidence 计算规则：confidence = max(top3.rerank_score)。与 crag_tier 的对应关系：
- correct：confidence > 0.8
- ambiguous：confidence 0.5-0.8
- incorrect：confidence < 0.5

action 判断规则：
- correct → action=proceed，进入冲突消解（无论是否有冲突，包括范式对立）
- ambiguous → action=proceed（标注中置信度），仍进入冲突消解
- incorrect + 召回为空 → action=fallback, fallback_type=empty_recall
- incorrect + 有召回但不相关 → action=degrade, fallback_type=irrelevant_recall（降级用 top-3 做非精确匹配回答，标注"低置信度"）
- ambiguous + 补全提问后仍无法判断适用条件 → action=fallback, fallback_type=unresolvable_conflict（仅用于真正死局，不是所有范式对立）
- ambiguous + 意图模糊 → action=fallback, fallback_type=ambiguous_intent

注意：
- 范式对立冲突如果召回质量高（correct），正常走 debate-protocol，不是 fallback
- fallback_type=unresolvable_conflict 仅用于"补全提问后仍无法判断适用条件"的真正死局

输出约束：必须是合法 JSON，不要包含 markdown 代码块标记或解释文字。所有字段必须存在，无法判断时用 null。
```
