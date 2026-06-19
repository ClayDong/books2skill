---
name: book2skill
description: Distill a book into a coherent set of executable skills. Use when the user asks to "拆书" / "蒸馏一本书" / "把 XX 书做成 skill" / "turn a book into skills" — i.e. wants a book's frameworks, principles, and methodologies extracted into atomic, reusable Claude skills that an agent can invoke in real-world situations. NOT for simple summarization, book reviews, or role-playing as the author (that is nuwa-skill's job).
---

# book2skill — 把一本书蒸馏成一组可执行 skills 的元 skill

## 使命

把一本书里沉淀的方法论,拆解成一组**原子化、可被 agent 在真实场景下调用**的 skills,让读者真正用起来。

**边界**:
- ✅ 做: 方法论 / 决策框架 / 清单 / 原则 / 概念体系的蒸馏
- ❌ 不做: 书摘 / 读后感 / 作者人设角色扮演 (后者请用 nuwa-skill)

## 核心方法论: RIA-TV++ + 多书协同

**单书蒸馏**（v1.0）：四阶段 + 并行提取 + 三重验证 + darwin 兼容测试的流水线。详见 `methodology/00-overview.md`。

**多书协同**（v2.0 新增）：意图驱动编排层，让用户"提出意图 → 从多本书召回 → 整合产出"。详见 `methodology/07-stage5-multi-book-orchestration.md`。

```
=== 单书蒸馏流水线（push）===
阶段 0: Adler 整书理解     → BOOK_OVERVIEW.md
阶段 1: 5 个 agent 并行提取 → 候选方法论单元池
阶段 1.5: 三重验证筛选       → 通过的单元
阶段 2: RIA++ 构造 skill     → 每个 skill 的 SKILL.md
阶段 3: Zettelkasten 链接    → INDEX.md
阶段 4: 压力测试 (darwin 兼容) → test-prompts.json + 回炉淘汰

=== 多书协同流水线（pull，v2.0 新增）===
阶段 5: 多书协同编排         → 意图分档 + 粗召 + 精排 + 冲突消解
阶段 6: 决策卡片构造         → library/DECISION_CARDS/<scenario>.md
```

## 何时调用此 skill

**单书蒸馏**（用户说类似）:
- "帮我拆《穷查理宝典》"
- "把毛选蒸馏成 skill"
- "distill this book into skills: <path>"
- "我想把这本书的方法论做成可用的 skill"

**多书协同**（v2.0 新增，用户说类似）:
- "我该不该止损？"（决策类，可能命中多本书的冲突观点）
- "用多本书的方法论帮我分析这个决策"
- "我已经拆了 N 本书，现在遇到问题想综合调用"
- "这个意图需要跨书整合"

## 输入要求

**单书蒸馏**在开始前**必须**从用户处确认:
1. **书的文本来源**: PDF / EPUB / TXT 文件路径, 或可访问的纯文本。**不要**在没有文本的情况下"凭记忆"拆书 — 宁可停下来问用户要。
2. **书名 + 作者 + 出版年**: 用于目录命名和审计。
3. **是否首次试点**: 如果用户是第一次用 book2skill,建议先拆 1 本验证流程再批量。

**多书协同**（v2.0 新增）在开始前**必须**确认:
1. **用户意图**: 用户要解决什么问题（决策 / 分析 / 执行 / 学习）
2. **已拆书目**: 至少 2 本已拆完的书（否则没有"多书"可协同）
3. **情境信号**（如适用）: 时间 horizon、风险偏好、可逆性等（用于冲突仲裁）

## 输出结构

### 单书蒸馏产出

```
books/<book-slug>/
├── BOOK_OVERVIEW.md           # 阶段 0 产出: 主旨/骨架/术语/批判
├── INDEX.md                   # 阶段 3 产出: skill 总览 + 引用图
├── candidates/                # 阶段 1 产出: 原始候选池 (审计用)
├── rejected/                  # 阶段 1.5 淘汰的单元 + 原因 (审计用)
├── <skill-slug-1>/
│   ├── SKILL.md
│   └── test-prompts.json      # darwin-skill 兼容格式
├── <skill-slug-2>/
│   └── ...
```

### 多书协同产出（v2.0 新增）

```
library/                       # 多书协同层
├── GLOBAL_INDEX.md            # 全局 skill 索引（所有书的 skill 扁平列表）
├── GLOSSARY_UNIFIED.md        # 统一术语表（跨书术语消解）
├── CONFLICTS.md               # 跨书冲突矩阵
└── DECISION_CARDS/            # 决策卡片目录
    └── <scenario-slug>.md     # 如 stop-loss.md

router/                        # 意图驱动路由层
└── prompts.md                 # 意图分类器 + 粗召 + 精排 + CRAG 评估

resolver/                      # 冲突消解层
└── prompts.md                 # 冲突检测 + 裁判协议 + debate 协议 + 决策卡片起草
```

## 执行流程 (严格按顺序)

### 阶段 0 — 整书理解

1. 读取用户提供的书本文本。大文件分块阅读。
2. 执行 `methodology/01-stage0-adler.md` 中的 Adler 四步 (结构 / 解释 / 批判 / 应用)。
3. 按 `templates/BOOK_OVERVIEW.md.template` 填充,写入 `books/<slug>/BOOK_OVERVIEW.md`。
4. 把产出展示给用户确认:"骨架我理解对了吗?有没有你希望重点突出的方向?" 得到确认再进入阶段 1。

### 阶段 1 — 5 个 sub-agent 并行提取

**并行** spawn 5 个 Task sub-agents(使用 Agent 工具,一次调用中发起 5 个):

| sub-agent | 读取的 prompt | 产出 |
|---|---|---|
| 框架提取器 | `extractors/framework-extractor.md` | 决策框架 / 思维模型 |
| 原则提取器 | `extractors/principle-extractor.md` | 原则 / 清单 / 规则 |
| 案例提取器 | `extractors/case-extractor.md` | 作者在书中亲自使用过的实例 |
| 反例提取器 | `extractors/counter-example-extractor.md` | 书中警告的失败模式 |
| 术语提取器 | `extractors/glossary-extractor.md` | 关键概念词典 |

每个 sub-agent 独立读书、独立提取、独立输出到 `books/<slug>/candidates/<type>.md`。

### 阶段 1.5 — 三重验证筛选

读取 `methodology/03-stage1.5-triple-verify.md`,对每个候选单元执行:

- **V1 跨域**: 书中至少 2 个独立段落有佐证?
- **V2 预测力**: 能用它回答一个书里没明说的新问题吗?
- **V3 独特性**: 不是任何聪明人都会说的常识吗?

通过的进入阶段 2。不通过的写入 `books/<slug>/rejected/` 并附原因 — 保留审计轨迹,也允许用户事后捞回。

### 阶段 2 — RIA++ 构造 skill

对每个通过的单元,按 `templates/SKILL.md.template` 填充:

- **R (Reading)**: 原文引用 ≤150 字/段
- **I (Interpretation)**: 用自己的话重写方法论骨架 (避免照搬译本)
- **A1 (Past Application)**: 书中作者用过的案例
- **A2 (Future Trigger)** ★: 用户在什么情境下会需要这个 → skill 的 `description` 字段
- **E (Execution)**: 1-2-3 可执行步骤
- **B (Boundary)**: 什么时候不适用 / 来自阶段 0 批判阶段的作者盲点

细则见 `methodology/04-stage2-ria-plus.md`。

### 阶段 3 — Zettelkasten 链接

按 `methodology/05-stage3-zettelkasten.md`:
1. 找出 skill 之间的引用关系 (A 依赖 B / A 对比 B / A 组合 B)
2. 在每个 SKILL.md 末尾补"相关 skills"段
3. 按 `templates/INDEX.md.template` 生成 `INDEX.md` (含引用图 mermaid)

### 阶段 4 — 压力测试 (darwin 兼容)

对每个 skill 按 `methodology/06-stage4-pressure-test.md`:
1. 设计 5–10 条测试 prompt,按 `templates/test-prompts.json.template` 写入 `test-prompts.json`
2. 至少包括 3 类: **应调用** / **不应调用 (诱饵)** / **边界模糊**
3. 本地跑一遍,**未过的回炉重做阶段 2** — 不做"表面修补"
4. 全部通过后,按已拆书目数量动态通知用户:
   - **拆完第 1 本**:「✅ 《X》拆解完成。后台正在更新全局索引。再拆 1 本即可解锁**多书协同**——你可以直接提意图（如"我该不该止损"），系统会跨书召回并整合多本书的方法论。也可喂给 darwin-skill 进化单书 skill。」
   - **拆完第 2 本**:「✅ 《X》拆解完成。多书协同已就绪（基础模式）。你可以试试提一个跨书意图。再拆 1 本可解锁冲突消解与决策卡片。」
   - **拆完第 3+ 本**:「✅ 《X》拆解完成。多书协同已就绪（完整模式），支持跨书冲突消解与决策卡片。」

### 阶段 4.5 — 全局索引汇聚（自动）

**触发时机**: 每拆完一本新书后自动触发,**无需用户干预**。

按 `methodology/09-stage4.5-library-build.md`,汇聚 `library/` 下的:
- `GLOBAL_INDEX.md` — 全局 skill 索引（所有书的 skill 扁平列表,使用逻辑 skill_id `<book-slug>::<skill-slug>`）
- `GLOSSARY_UNIFIED.md` — 统一术语表（跨书术语消解）
- `CONFLICTS.md` — 跨书冲突矩阵（检测并标注冲突类型）

汇聚时遵守 `library/` 保护机制:自动生成段用 `<!-- AUTO-GEN START -->` / `<!-- AUTO-GEN END -->` 标记,标记外的用户自定义段保留。

### 阶段 5 — 多书协同编排 (v2.0 新增)

**前置条件**: 至少有 2 本已拆完的书 + `library/GLOBAL_INDEX.md` 已生成。

按 `methodology/07-stage5-multi-book-orchestration.md`:

**步骤 0 — 决策卡片命中检查**: 用户提意图后,先扫描 `library/DECISION_CARDS/`。若命中已有卡片 → 直接按卡片的 DAG 执行,跳过粗召/精排。若未命中 → 走以下步骤 1-7。

1. **意图分档 + 情境信号提取**: 用 `router/prompts.md` 的 intent-classifier 分档 (A 简单 / B 单框架 / C 多框架冲突),同时提取情境信号（时间 horizon、风险偏好、可逆性等）
2. **粗召（含术语消解）**: 从全局索引召回 top-10 候选 skill,先用 `GLOSSARY_UNIFIED.md` 做跨书术语消解
3. **精排 top-3**: cross-encoder / LLM-as-judge 按意图相关度重排,取 top-3
4. **冲突检测（两两检测）**: 对 top-3 两两做立场冲突检测,输出 `{{DETECTED_CONFLICTS}}`
5. **CRAG 评估**: 对召回结果做 CRAG 分档评估 — `correct`（精确相关）/ `ambiguous`（部分相关）/ `incorrect`（不相关）
6. **冲突消解**: 按冲突类型走不同路径:
   - 无冲突 → 直接执行
   - 情境互补（situational）→ judge-protocol 裁决
   - 范式对立（paradigmatic）→ debate-protocol 多视角呈现
   - 时代演变（temporal）→ temporal-protocol 按情境选择新旧方法论
   - 兜底 → 多视角对照表
7. **Self-RAG 质检**: 对产出做 5 项检查 — IsRel（相关）/ IsSup（有佐证）/ IsUse（有用）/ IsConsistent（一致）/ NeedRecall（需重召）。`overall_pass = IsRel && IsSup && IsUse && IsConsistent`,confidence ≥ 0.7 才算 pass

**产出分级**（按意图档位）:
- **A 档**: 只输出「答案 + provenance」2 段
- **B 档**: 输出「答案 + 编排逻辑 + provenance」3 段
- **C 档**: 输出完整 6 段（意图回显 / 召回列表 / 冲突标注 / 整合答案 / 决策清单 / 不确定性标注）

**provenance 标注格式**: `[来自《X》—— skill 的人类可读名]`（不再用 skill-Y 编号）

**不确定性级别**:
- 高置信度: rerank_score > 0.8 且 Self-RAG 全通过 → 无需标注
- 中置信度: rerank_score 0.5-0.8 或 Self-RAG 重试 1 次后通过 → 标注"⚠️ 中置信度：[原因]"
- 低置信度: rerank_score < 0.5 或 Self-RAG 重试 2 次仍不通过 → 标注"🔴 低置信度：[原因]，建议[下一步]"

**失败兜底** (必须实现,引导行动而非只报告问题):
- 召回为空 → 告知 + 推荐最接近的 top-3（标注"非精确匹配"）+ 建议拆新书（给出具体书目推荐方向）
- 召回不相关 → 降级用 top-3 做非精确匹配回答,标注"🔴 低置信度：召回结果与意图相关度不足,建议补充情境或拆新书"
- 冲突不可消解 → 输出多视角对照表 + 各自适用前提 + 决策清单
- 意图模糊 → 触发澄清式提问（单次只问 1 个问题,用选择题形式,不开放式追问）

### 阶段 6 — 决策卡片构造 (v2.0 新增)

**何时构造**: 同一类意图被提出 ≥3 次, 或涉及跨书冲突, 或涉及不可逆决策。

**何时使用**: 用户提意图时,阶段 5 步骤 0 会先扫描 `library/DECISION_CARDS/`。命中已有卡片 → 直接按卡片的 DAG 执行,跳过粗召/精排。

按 `methodology/08-stage6-decision-cards.md`:
1. 识别高频意图
2. 召回参与 skill, 标注角色 (前置/核心/校验/兜底)
3. 按五维度分类决策情境:
   - **可逆性**: 不可逆 / 高成本可逆 / 低成本可逆（三档）
   - **影响范围**: 仅自己 / 涉及他人 / 组织级
   - **时间压力**: 紧急 / 充裕
   - **信息完备度**: 充分 / 不足
   - **利益相关方**: 仅自己 / 涉及他人 / 需他人执行
   - 维度优先级: 可逆性 > 利益相关方 > 信息完备度 > 时间压力
4. 设计编排 DAG
5. 定义冲突仲裁规则
6. 用 `templates/orchestration-test-prompts.json.template` 压力测试
7. 写入 `library/DECISION_CARDS/<scenario-slug>.md`

## 质量红线 (违反则阻止输出)

### 单书蒸馏红线

1. 每个 skill 必须通过**全部**三重验证
2. 每个 skill 必须有完整的 R / I / A1 / A2 / E / B 六段
3. 原文引用 ≤150 字/段
4. 每个 skill 必须有 `test-prompts.json`,且包含诱饵测试 (不应调用的场景)
5. `description` 字段必须明确 trigger 条件,不能只是"一个关于 X 的 skill"

### 多书协同红线 (v2.0 新增)

6. 编排层必须显式声明编排逻辑,不能是简单堆叠
7. 冲突必须被检测和标注,**不能消音**
8. 范式对立型冲突必须呈现多元视角,不强行给单一答案
9. 每张决策卡片必须有冲突仲裁规则
10. 召回为空时必须走兜底流程,**不能幻觉编造**

## 与 nuwa-skill / darwin-skill 的生态定位

- **nuwa-skill**: 蒸馏人 (思维方式 / 表达 DNA)
- **book2skill** (本 skill): 蒸馏书 (方法论 / 框架 / 原则)
- **darwin-skill**: 进化任意 skill

三者咬合: 本 skill 输出的 `test-prompts.json` 严格遵循 darwin-skill 格式,以便产出的 skill 可直接接入 darwin 做自动进化。

### nuwa-skill 边界判断规则

当用户需求模糊时,按以下规则判断走 book2skill 还是 nuwa-skill:
- **走 book2skill**: 用户要的是"书里的方法论 / 框架 / 清单"
- **走 nuwa-skill**: 用户要的是"用 X 的语气 / 风格 / 表达 DNA 说话"
- **两者都可**: 看源材料形态——有书 → book2skill；只有访谈 / 语录 → nuwa-skill

### 元 skill 自举性声明

本 skill 不能蒸馏自己（自举会导致无限递归）。如需优化本 skill 的方法论,请用 darwin-skill 直接进化。

## 调用惯例

- **永远先试点 1 本** — 除非用户明确说"批量"
- **阶段之间主动汇报进度** — 不要静默跑完再 dump 结果
- **不凭记忆拆书** — 没文本就停下来问
- **保留审计轨迹** — candidates/ 和 rejected/ 都要留
