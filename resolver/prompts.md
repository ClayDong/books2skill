# Resolver Prompts — 冲突消解层

> 本文件包含阶段 5（多书协同编排）步骤 4 使用的所有 prompt，以及阶段 6（决策卡片构造）的 card-drafter。
> 调用方：book2skill 元 skill 的编排层，在精排检测到冲突后调用。
>
> **card-drafter 属于阶段 6**，因同样涉及冲突消解逻辑，放在本文件便于参考。
>
> ## CONFLICTS.md 与 conflict-detector 的职责关系
>
> - `library/CONFLICTS.md` 是**历史冲突沉淀**（已知冲突的静态记录），用于阶段 5 精排阶段做 hint 加权
> - `conflict-detector`（本文件第 1 节）是**运行时新冲突检测**，检测召回 skill 之间的即时冲突
> - 运行时检测到的新冲突应**增量回写**进 CONFLICTS.md 的"冲突检测日志"段（在 `<!-- AUTO-GEN INCREMENTAL START -->` / `<!-- AUTO-GEN INCREMENTAL END -->` 标记内追加一条记录）
> - 回写时的字段映射：conflict-detector 输出的 `skill_a`/`skill_b` → CONFLICTS.md 的 `skills_involved`；`conflict_type`/`conflict_description`/`a_position`/`b_position`/`resolution_hint` 直接对应
>
> ## 变量绑定契约
>
> | 变量 | 来源 | 取值方式 | 缺失时默认 |
> |---|---|---|---|
> | `{{USER_INTENT}}` | 用户输入 | 原始意图文本（temporal-protocol 用于推断情境信号） | — |
> | `{{INTENT_JSON}}` | intent-classifier 输出 | 完整 JSON | — |
> | `{{TOP3}}` | fine-recall 输出 | top3 字段 | — |
> | `{{TOP3_SKILL_CONTENTS}}` | top-3 的 SKILL.md | XML 标签 `<skill id="...">...</skill>` 包裹拼接 | — |
> | `{{KNOWN_CONFLICTS}}` | library/CONFLICTS.md | 文件全文 | 空字符串 |
> | `{{DETECTED_CONFLICTS}}` | conflict-detector 输出 | conflicts 数组 | 空数组 |
> | `{{CONFLICT}}` | conflict-detector 输出 | conflicts[i] 单条 | — |
> | `{{SKILL_A}}` / `{{SKILL_B}}` | top-3 中冲突对的 skill | 完整 SKILL.md 内容 | — |
> | `{{OUTPUT}}` | 上游产出 | markdown 或 JSON | — |
> | `{{PARTICIPATING_SKILL_CONTENTS}}` | 参与产出的 skill | XML 标签包裹拼接 | — |
> | `{{PARTICIPATING_SKILLS}}` | 阶段 6 召回 | `[{skill_id, role, source_book, one_line_reason}]` JSON 数组 | — |
> | `{{EXECUTION_HISTORY}}` | 历史执行记录 | JSON 数组（可为空 `[]`） | `[]` |
> | `{{PREVIOUS_JUDGMENT}}` | judge-protocol 首次判断 | 中间结果 JSON（多轮交互用） | — |

---

## 1. conflict-detector（冲突检测器）

**用途**：对精排的 top-3 两两做立场冲突检测。是唯一的运行时冲突检测器。

```prompt
你是一个冲突检测器。对精排的 top-3 skill 两两检测立场冲突。

top-3 skill 列表：{{TOP3}}

每个 skill 的完整内容（含 R/I/A1/A2/E/B 段）：{{TOP3_SKILL_CONTENTS}}

已知冲突矩阵（历史沉淀）：{{KNOWN_CONFLICTS}}

检测规则：
1. **先查历史**：先查 KNOWN_CONFLICTS 中是否已有涉及 top-3 skill 的冲突记录。如有，直接采用历史分类（situational/paradigmatic/temporal），不重复判断
2. **再做运行时检测**：对没有历史记录的 pair，基于 skill 完整内容做运行时检测

对每对 skill (A, B)，判断：
1. A 和 B 是否对同一类问题给出相反的行动建议？
2. A 和 B 的前提假设是否互斥？
3. A 和 B 的适用边界是否重叠？

如果存在冲突，分类：
- situational（情境互补型）：A 和 B 在不同情境下各自正确
  - 示例：止损（短线）vs 不止损（长线）
- paradigmatic（范式对立型）：A 和 B 基于不同范式，不可消解
  - 示例：有效市场 vs 行为金融
- temporal（时代演变型）：A 是旧方法论，B 是新方法论（或反之）
  - 示例：传统营销 vs 增长黑客

输出 JSON：
{
  "conflicts": [
    {
      "skill_a": "...",
      "skill_b": "...",
      "has_conflict": true,
      "conflict_type": "situational|paradigmatic|temporal",
      "conflict_description": "冲突的具体描述",
      "a_position": "A 的立场",
      "b_position": "B 的立场",
      "resolution_hint": "消解提示（如情境互补型，说明各自适用的情境）",
      "source": "historical|runtime"
    }
  ],
  "no_conflict_pairs": [["skill_x", "skill_y"]]
}

输出约束：必须是合法 JSON，不要包含 markdown 代码块标记或解释文字。所有字段必须存在，无法判断时用 null。
```

---

## 2. judge-protocol（裁判协议，用于情境互补型冲突）

**用途**：对情境互补型冲突，根据用户情境信号裁决。

**多轮交互协议**：
1. 首次调用：输入 `{{INTENT_JSON}}` + `{{CONFLICT}}` + `{{SKILL_A}}` + `{{SKILL_B}}`
2. 若 `judgment=needs_more_info`，向用户提问 `clarification_question`
3. 用户回答后，第二次调用：输入更新后的 `{{INTENT_JSON}}`（将用户回答合并进对应字段）+ 原 `{{CONFLICT}}` + 原 `{{SKILL_A}}` + 原 `{{SKILL_B}}` + 新增字段 `{{PREVIOUS_JUDGMENT}}`
4. 第二次调用输出最终 judgment，不再触发 `needs_more_info`（**最多 1 轮补全**）

```prompt
你是一个裁判。两个 skill 在不同情境下各自正确，你需要根据用户当前情境选择其一。

用户意图（含情境信号）：{{INTENT_JSON}}

冲突信息：{{CONFLICT}}

skill A 完整内容：{{SKILL_A}}

skill B 完整内容：{{SKILL_B}}

首次判断的中间结果（多轮交互时传入，首次调用为 null）：{{PREVIOUS_JUDGMENT}}

裁决规则：
1. 提取用户意图中的情境信号（time_horizon、risk_preference、reversibility、capital_type、target_type）
2. 读取 INTENT_JSON.missing_signals，如果非空，根据决策情境动态判断是否需要补全提问：
   - 不可逆 + 高影响：≥1 个关键信号未知就提问（关键信号 = reversibility, time_horizon）
   - 高成本可逆 + 中影响：≥2 个未知提问
   - 低成本可逆 + 低影响：≥3 个未知提问，或直接走快速路径
3. **信号不足时，先输出初步建议（基于已有信号，标注"中置信度"），再附补全提问**——让用户立刻有收获，补全是"增值"而非"前置门槛"
4. 补全提问规则：
   - 最多 1 轮补全（不要连环问）
   - 单次只问 1 个问题，用选择题形式（"你指的是 A 还是 B？"）
   - ≤20 字
   - 1 轮后仍不足 → 用已有信号给初步建议 + 标注"低置信度"
5. 用户回答后（或 PREVIOUS_JUDGMENT 非空时），重新判断信号更匹配 A 还是 B 的适用条件
6. 如果补全后信号仍不足以判断 → judgment=unresolvable，走范式对立路径

输出 JSON：
{
  "judgment": "A|B|unresolvable|needs_more_info",
  "chosen_skill": "...",
  "reason": "为什么选这个 skill",
  "why_not_the_other": "为什么另一个不适用",
  "boundary_note": "使用这个 skill 时需要注意的边界",
  "alternative_trigger": "在什么情况下应该改用另一个 skill",
  "preliminary_advice": "（信号不足时）基于已有信号的初步建议，标注中置信度",
  "clarification_needed": ["risk_preference", "time_horizon"],
  "clarification_question": "（如需补全）要问用户什么，选择题形式，≤20 字"
}

注意：
- 不要为了给单一答案而强行裁决
- 情境信号不足时，优先输出初步建议 + 附补全提问（judgment=needs_more_info），而非直接降级为范式对立
- 补全后仍无法判断，judgment=unresolvable，走范式对立路径
- 必须说明"为什么另一个不适用"，让用户理解裁决逻辑
- missing_signals（来自 intent-classifier）是检测输出，clarification_needed（本 prompt 输出）是补全提问输出。judge-protocol 读取 missing_signals，非空时根据决策情境动态判断阈值

输出约束：必须是合法 JSON，不要包含 markdown 代码块标记或解释文字。所有字段必须存在，无法判断时用 null。
```

---

## 3. debate-protocol（多 Agent Debate，用于范式对立型冲突）

**用途**：对范式对立型冲突，不强行消解，呈现多元视角。

```prompt
你是一个 debate 主持人。两个 skill 基于不同范式，不可消解。你需要组织一场 debate，呈现多元视角。

用户意图：{{INTENT_JSON}}

冲突信息：{{CONFLICT}}

skill A 完整内容：{{SKILL_A}}（A 派立场）

skill B 完整内容：{{SKILL_B}}（B 派立场）

Debate 流程：
1. A 派发言：用 A 的方法论分析用户意图，给出建议 + 理由
2. B 派发言：用 B 的方法论分析用户意图，给出建议 + 理由
3. A 派反驳 B：指出 B 的建议在什么条件下会失效
4. B 派反驳 A：指出 A 的建议在什么条件下会失效
5. 主持人总结：基于用户已提供的情境信号动态标注"你当前更接近哪一派"，不选边

输出格式（markdown）：

## 多视角对照

### 你的问题
{{复述用户意图}}

### 基于你的情境信号
根据你提供的信号：
- 时间 horizon: {{time_horizon}}
- 风险偏好: {{risk_preference}}
- 可逆性: {{reversibility}}

你的情境更接近 **{{A/B 派}}**，因为 {{具体原因}}。

但请注意：{{另一派在什么条件下会更适合你}}。

如果上述信号有"未知"，请先回答以下诊断问题：
- {{诊断问题 1}}
- {{诊断问题 2}}

### A 派观点（来自《X》）
- **建议**: ... [来自《X》—— skill 人类可读名]
- **理由**: ...
- **适用条件**: ...

### B 派观点（来自《Y》）
- **建议**: ... [来自《Y》—— skill 人类可读名]
- **理由**: ...
- **适用条件**: ...

### A 派对 B 的反驳
- B 的建议在 ___ 条件下会失效，因为 ___

### B 派对 A 的反驳
- A 的建议在 ___ 条件下会失效，因为 ___

### 主持人总结
两派基于不同范式，各有适用场景。决策权在你：
- 如果你的情境更接近 ___ → 倾向 A 派
- 如果你的情境更接近 ___ → 倾向 B 派
- 如果无法判断 → 建议先收集更多信息（列出要收集什么）

### 决策清单（含判断辅助）

- [ ] 判断你的时间 horizon
  - 诊断：你目前的主要收入是否依赖这次决策的标的？
    - 是 → 短期
    - 否 → 继续问：你是否有 3 年以上的应急储备？
      - 是 → 可长期
      - 否 → 中期

- [ ] 判断你的风险偏好
  - 诊断：如果这次决策完全亏损，你的生活会受到什么影响？
    - 严重影响基本生活 → 保守
    - 影响生活质量但不影响基本生活 → 中性
    - 可承受完全亏损 → 激进

- [ ] 基于以上判断，选择 A 或 B
  - 短期 + 保守 → 倾向 A 派
  - 长期 + 激进 → 倾向 B 派
  - 其他组合 → 见主持人总结
```

---

## 4. temporal-protocol（时代演变协议，用于 temporal 冲突）

**用途**：对 temporal 冲突（新旧方法论更替），按情境选择新旧方法论，而非简单"优先用新版"。

```prompt
你是一个时代演变仲裁器。两个 skill 代表新旧方法论，你需要根据用户情境选择其一。

用户意图（原文）：{{USER_INTENT}}

用户意图（结构化）：{{INTENT_JSON}}

冲突信息：{{CONFLICT}}

skill A（旧方法论）：{{SKILL_A}}

skill B（新方法论）：{{SKILL_B}}

裁决规则：
1. **提取情境信号**：以下 4 个信号从用户意图文本（{{USER_INTENT}} 原文）中推断，不在 INTENT_JSON 的结构化字段中（intent-classifier 不输出这些字段）。推断不出时标记为"未知"：
   - 市场成熟度（market_maturity）：成熟市场 / 新兴市场 / 未知
   - 资源充足度（resource_constraint）：充足 / 受限 / 未知
   - 需求明确度（demand_clarity）：明确 / 模糊 / 未知
   - 技术稳定性（tech_stability）：稳定 / 快速变化 / 未知
2. 旧方法论适用条件：成熟市场 + 资源充足 + 需求明确 + 技术稳定
3. 新方法论适用条件：新兴市场 + 资源受限 + 需求模糊 + 技术快速变化
4. 信号不足时（≥2 个未知），先输出初步建议（基于已有信号，标注"中置信度"）+ 附补全提问（最多 1 轮）
5. 补全后仍无法判断，judgment=unresolvable，呈现新旧对比 + 各自适用场景

输出 JSON：
{
  "judgment": "old|new|unresolvable|needs_more_info",
  "chosen_skill": "...",
  "reason": "为什么选这个 skill",
  "why_not_the_other": "为什么另一个不适用",
  "boundary_note": "使用这个 skill 时需要注意的边界",
  "alternative_trigger": "在什么情况下应该改用另一个 skill",
  "clarification_needed": [],
  "clarification_question": "（如需补全）要问用户什么"
}

注意：
- 不要简单"优先用新版"。新旧方法论各有适用场景，按情境消解
- 信号不足时先输出初步建议 + 附补全提问（最多 1 轮）
- 补全后仍无法判断，judgment=unresolvable，呈现新旧对比

输出约束：必须是合法 JSON，不要包含 markdown 代码块标记或解释文字。所有字段必须存在，无法判断时用 null。
```

---

## 5. card-drafter（决策卡片起草器，属于阶段 6）

**用途**：对高频意图，把编排逻辑固化成决策卡片。

```prompt
你是一个决策卡片起草器。这个意图已被提出多次，需要固化成决策卡片。

意图：{{INTENT_JSON}}

参与的 skill 列表（JSON 数组，每条含 skill_id, role, source_book, one_line_reason）：{{PARTICIPATING_SKILLS}}

已知冲突：{{KNOWN_CONFLICTS}}

历史执行记录（可为空数组）：{{EXECUTION_HISTORY}}

按以下结构起草决策卡片（使用 DECISION_CARD.md.template 格式）：

1. 基本信息（card_id, scenario, intent_type, books_involved, conflict_level）
2. 适用边界（适用场景 / 不适用场景 / 超出边界时回退阶段 5）
3. 决策情境分类（五维度：可逆性/影响范围/时间压力/信息完备度/利益相关方）
4. 参与的 skill 列表（标注角色：前置/核心/校验/兜底）
5. 编排流程（mermaid DAG，支持回环）
6. 冲突仲裁规则（结构化 YAML，覆盖所有已知冲突场景）
7. 决策日志模板（含复盘触发条件）
8. 卡片进化段（累计回溯记录、仲裁规则准确率）

仲裁规则必须覆盖：
- 情境互补型冲突：按情境信号裁决（结构化 condition，字段名与 intent-classifier 输出一致）
- 范式对立型冲突：呈现多元视角，不强行消解
- temporal 冲突：按情境选择新旧方法论
- 兜底：核心结论不可靠时的降级方案

仲裁规则用结构化 YAML 表达，不要用自然语言 condition：
```yaml
arbitration_rules:
  - condition:
      field: time_horizon
      operator: in
      value: [短期, 紧急]
    prefer: "<book-slug>::<skill-slug>"
    reason: "..."
  - condition:
      field: time_horizon
      operator: equals
      value: 未知
    action: "触发诊断子流程"
    diagnostic_questions: [...]
    fallback: "诊断后仍无法判断 → 呈现两派观点"
```

输出：完整的决策卡片 markdown
```

---

## 6. self-rag-checker（Self-RAG 质检器）

**用途**：对多书协同的最终产出做质检。

**重要**：`{{OUTPUT}}` 可能是 markdown（来自 debate-protocol）或 JSON（来自 judge-protocol/temporal-protocol）。IsSup 检查规则针对两种格式分别说明。

```prompt
你是一个 Self-RAG 质检器。对多书协同的最终产出做质量检查。

用户意图：{{INTENT_JSON}}

最终产出（可能是 markdown 或 JSON）：{{OUTPUT}}

参与的 skill 内容：{{PARTICIPATING_SKILL_CONTENTS}}

检查五项：
1. [IsRel] 产出是否与用户意图相关？
2. [IsSup] 产出的每段建议是否有 skill 支撑（provenance）？
   - markdown 输出：检查每条建议后是否有 `[来自《X》]` 标注
   - JSON 输出：检查是否有 provenance 字段
3. [IsUse] 产出对用户是否有用（可执行）？
4. [IsConsistent] 产出内部是否自相矛盾（同一决策点给出相反建议）？
5. [NeedRecall] 是否需要重新召回？（产出质量不足时）

输出 JSON：
{
  "IsRel": true|false,
  "IsRel_reason": "...",
  "IsSup": true|false,
  "IsSup_reason": "...",
  "IsUse": true|false,
  "IsUse_reason": "...",
  "IsConsistent": true|false,
  "IsConsistent_reason": "...",
  "NeedRecall": true|false,
  "NeedRecall_reason": "...",
  "overall_pass": true|false,
  "confidence": 0.0-1.0,
  "pass_with_caveats": true|false,
  "caveats": ["保留意见1", "保留意见2"],
  "issues": ["问题1", "问题2"],
  "fix_suggestions": ["建议1", "建议2"]
}

判定逻辑（必须严格遵守，不得矛盾）：
- overall_pass = IsRel && IsSup && IsUse && IsConsistent
- confidence >= 0.7 才算 overall_pass=true
- confidence 0.5-0.7 → overall_pass=true, pass_with_caveats=true（通过但有保留意见）
- confidence < 0.5 → overall_pass=false
- NeedRecall 不影响 overall_pass 判定，单独触发重试

质检规则：
- IsRel=false → 产出跑题，需要重新理解意图（回到 intent-classifier，重试上限 1 次）
- IsSup=false → 有建议无来源，需要补充 provenance（不重召回，重试上限 2 次）
- IsUse=false → 产出不可执行，需要重写 E 段（重试上限 2 次）
- IsConsistent=false → 产出自相矛盾，需要重新走冲突消解（重试上限 1 次）
- NeedRecall=true → 召回质量不足，需要扩大召回范围到 top-20（重试上限 1 次，仍失败则标注低置信度）

输出约束：必须是合法 JSON，不要包含 markdown 代码块标记或解释文字。所有字段必须存在，无法判断时用 null。
```
