# 阶段 5 — 多书协同编排（Multi-Book Orchestration）

## 目标

在单书蒸馏流水线（阶段 0-4）之上，叠加一层**意图驱动的编排层**，让用户能"提出意图 → 从多本书的 skills 中召回 → 整合产出"。

本阶段不产出新的 atomic skill，而是**编排已有的 atomic skills**。

## 前置条件

- 至少有 2 本已拆完的书（否则没有"多书"可协同）
- 已有 `library/GLOBAL_INDEX.md`（全局 skill 索引）
- 已有 `library/GLOSSARY_UNIFIED.md`（统一术语表）

这些文件由阶段 4.5（`methodology/09-stage4.5-library-build.md`）生成。

## 变量绑定契约

编排流程中每个 prompt 的输入变量从上游产出构造，统一约定如下：

| 变量 | 来源 | 取值方式 | 缺失时默认 |
|---|---|---|---|
| `{{INTENT_JSON}}` | intent-classifier 输出 | 完整 JSON | — |
| `{{GLOBAL_INDEX}}` | library/GLOBAL_INDEX.md | 文件全文 | 报错（前置条件） |
| `{{GLOSSARY_UNIFIED}}` | library/GLOSSARY_UNIFIED.md | 文件全文 | 跳过术语消解 |
| `{{KNOWN_CONFLICTS}}` | library/CONFLICTS.md | 文件全文 | 空字符串 |
| `{{CANDIDATES}}` | coarse-recall 输出 | JSON 数组 | 空数组→走兜底 |
| `{{TOP3}}` | fine-recall 输出 | top3 字段 | — |
| `{{TOP3_SKILL_CONTENTS}}` | top-3 的 SKILL.md | XML 标签包裹拼接 | — |
| `{{DETECTED_CONFLICTS}}` | conflict-detector 输出 | conflicts 数组 | 空数组 |
| `{{CONFLICT}}` | conflict-detector 输出 | conflicts[i] 单条 | — |
| `{{OUTPUT}}` | 上游产出 | markdown 或 JSON | — |

## 编排流程

### 步骤 0 — 决策卡片命中检查

用户提意图后，先扫描 `library/DECISION_CARDS/`：

- **命中已有卡片** → 直接按卡片的 DAG 执行，跳过粗召/精排
- **未命中** → 走正常阶段 5 流程（步骤 1 起）

命中判定标准：用户意图与卡片 `scenario` 字段语义匹配，且情境信号落在卡片适用边界内。

### 步骤 1 — 意图理解与分档

用户提出意图后，先用 `router/prompts.md` 中的 `intent-classifier` prompt 分档：

| 档位 | 含义 | 走法 |
|---|---|---|
| **A 档（简单）** | 单 skill 即可回答 | 直接路由到 top-1 skill，走原流程 |
| **B 档（单框架）** | 意图落在某本书的框架体系内，需组合该书 2-3 个 skill | 书内编排（用阶段 3 的 composes-with 关系） |
| **C 档（多框架冲突）** | 意图命中多本书的冲突观点 | 走完整流程（步骤 2-4 + 冲突消解） |

**A 档误判纠错机制**：A 档路由到 top-1 skill 前，先检查 `{{KNOWN_CONFLICTS}}` 中是否有涉及该 skill 的冲突记录：
- 有冲突 → 升级为 C 档，重新走完整流程
- 无冲突 → 正常执行 A 档

**意图模糊时**：触发澄清式提问（"你说的'这个事'是指决策类、分析类还是执行类？"），不猜测。

### 步骤 2 — 粗召（Recall）

对 A/B/C 档都需要（A 档只取 top-1）。

用 `router/prompts.md` 中的 `coarse-recall` prompt，从 `library/GLOBAL_INDEX.md` 中召回 top-10 候选 skill。

**召回信号**：
- 语义相关度（意图 vs skill 的 description + I 段）
- tags 硬过滤（意图领域 vs skill tags）
- source_book 权威性加权

**召回为空时**：走兜底（见步骤 4）。

### 步骤 3 — 精排与冲突检测（Rerank & Detect）

用 `router/prompts.md` 中的 `fine-recall` prompt 对 top-10 重排，取 top-3。

**精排特征**：
- 语义相关度
- B 段是否排除了当前场景（负向扣分）
- source_book 权威性
- skill 之间的冲突关系（来自 `library/CONFLICTS.md`）

**冲突检测**：对 top-3 两两做立场冲突检测（用 `resolver/prompts.md` 中的 `conflict-detector` prompt）。

**多对冲突处理**：top-3 最多产生 3 对冲突（C(3,2)=3）。如果检测到多对冲突：
- 按冲突类型优先级处理：situational > temporal > paradigmatic（可消解的优先消解）
- 同类型多对冲突：逐对调用对应的消解 prompt（judge-protocol / temporal-protocol / debate-protocol），结果合并到最终产出
- 如果冲突 skill 数量 ≥3（即 3 个 skill 互相冲突），CRAG 评估为 ambiguous，按最复杂的冲突类型处理

### 步骤 3.5 — CRAG 评估（质量关卡）

用 `router/prompts.md` 中的 `crag-evaluator` prompt 对精排结果做三档评估。**CRAG 评估的是召回质量，不是冲突可消解性**：

- **correct**（准确）：top-3 有高相关 skill → 进入步骤 4（冲突消解）
- **ambiguous**（模糊）：置信度不足 → 根据冲突类型走步骤 4 不同路径（不是 fallback）
- **incorrect**（错误）：召回不相关或为空 → 走兜底（步骤 4 路径 4）

**关键区分**：范式对立冲突如果召回质量高（correct），正常走步骤 4 路径 3（debate-protocol），**不是 fallback**。`fallback_type=unresolvable_conflict` 仅用于"补全提问后仍无法判断适用条件"的真正死局。

### 步骤 4 — 冲突消解与产出（Resolve & Output）

根据冲突检测结果，走不同路径：

#### 路径 1：无冲突（A 档或 B 档）

直接执行 skill 或书内组合，产出整合答案。

- **A 档**：直接路由到 top-1 skill，执行该 skill 的方法论，输出 2 段（答案 + provenance）
- **B 档**：编排层读取 top-3 skill 的完整 SKILL.md 内容，按意图整合多个 skill 的方法论。无冲突时不需要专门 prompt——编排层（执行 SKILL.md 的 agent）直接按意图组合 skill 的 R/I/A1/A2/E/B 段，输出 3 段（答案 + 编排逻辑 + provenance）。组合依据：top-3 skill 之间的 `composes-with` 关系（来自单书阶段 3 产出）

#### 路径 2：情境互补型冲突（可消解）

用 `resolver/prompts.md` 中的 `judge-protocol` prompt，根据用户意图的情境信号（时间 horizon、风险偏好等）选择其一，并说明为什么另一个不适用。

**信号不足时**：先给初步建议（标注"⚠️ 中置信度"）+ 附带补全提问，让用户立刻有收获。**最多 1 轮补全**，1 轮后仍不足 → 用已有信号给初步建议 + 标注"🔴 低置信度"。

**示例**：止损 vs 不止损
- 短线/投机 → 止损
- 长线/价值投资 → 不止损

#### 路径 3：范式对立型冲突（不可消解）

**不强行给单一答案**。用 `resolver/prompts.md` 中的 `debate-protocol` prompt，产出"两派观点对照表"+ 各自适用前提，把决策权交还用户。

**示例**：有效市场 vs 行为金融
- 输出两派立场 + 各自适用条件 + 决策清单

#### 路径 3.5：时代演变型冲突（temporal）

用 `resolver/prompts.md` 中的 `temporal-protocol` prompt，按情境选择新旧方法论：

- **旧方法论适用**：成熟市场 + 资源充足 + 需求明确
- **新方法论适用**：新兴市场 + 资源受限 + 需求模糊
- **信号不足时**：呈现新旧方法论对比 + 各自适用场景，让用户判断

#### 路径 4：兜底（召回为空 / 冲突不可消解 / 意图模糊）

兜底流程不需要专门 prompt——编排层（执行 SKILL.md 的 agent）按以下结构直接生成兜底消息，因为兜底是结构化输出而非方法论推理：

**召回为空**：
1. 明确告知"当前已拆的 N 本书里没有覆盖这个意图的 skill"
2. 推荐拆新书方向（如"建议拆《X》类书，它覆盖这个领域"），让用户知道下一步该做什么
3. 给出两个选项：(a) 用最接近的 top-3 skill 做降级回答（标注"非精确匹配"），(b) 拆一本新书补充覆盖

**冲突不可消解**（`fallback_type=unresolvable_conflict`，仅用于补全提问后仍无法判断适用条件的死局）：
1. 输出"两派观点 + 各自适用前提 + 决策清单"
2. 标注"🔴 低置信度"

**意图模糊**（`fallback_type=ambiguous_intent`）：
1. 触发澄清式提问
2. 不猜测

## ReAct 执行骨架

```
用户意图
   │
   ▼
[卡片命中检查] ──→ 命中 DECISION_CARDS？
   │
   ├─ 命中 → 按卡片 DAG 执行
   │
   ▼
[意图分类器] ──→ A/B/C 档位 + 情境信号
   │
   ├─ 意图模糊 → 兜底：澄清式提问
   │
   ▼
[粗召] ──→ top-10 候选（含术语消解）
   │
   ├─ 召回为空 → 兜底：告知 + 推荐拆新书方向
   │
   ▼
[精排] ──→ top-3
   │
   ▼
[冲突检测] ──→ 冲突图
   │
   ▼
[CRAG 评估] ──→ correct / ambiguous / incorrect
   │
   ├─ incorrect → 兜底：路径4
   │
   ▼
[冲突消解]
   ├─ 无冲突 → 路径1：直接执行
   ├─ 情境互补 → 路径2：裁判路由（信号不足先给初步建议+补全提问）
   ├─ 范式对立 → 路径3：多视角呈现
   ├─ 时代演变 → 路径3.5：temporal-protocol 按情境选新旧
   └─ 不可消解 → 路径4：兜底
   │
   ▼
[产出 + provenance]
   │
   ▼
[Self-RAG 质检] ──→ IsRel / IsSup / IsUse / IsConsistent / NeedRecall
   │
   ├─ 不通过 → 按失败项分级重试
   │
   ▼
[最终输出]
```

## 产出格式

产出按档位分级，避免 A 档简单问题输出冗余 6 段：

**A 档**（2 段）：
1. **答案**：直接回答 + provenance `[来自《X》skill-Y]`
2. **provenance**：来源 skill 列表

**B 档**（3 段）：
1. **答案**：整合答案 + provenance
2. **编排逻辑**：用了哪些 skill + 为什么这样组合
3. **provenance**：来源 skill 列表

**C 档**（完整 6 段）：
1. **意图回显**：复述用户意图 + 分档结果
2. **召回的 skill 列表**：标注每本书的 skill + 召回理由
3. **冲突标注**（如有）：冲突类型 + 涉及的 skill + 消解策略
4. **整合答案**：每段建议标注 `[来自《X》skill-Y]`
5. **决策清单**（如适用）：可执行的下一步
6. **不确定性标注**（如适用）：按三级不确定性标注

### 不确定性级别

- **高置信度**：rerank_score > 0.8 且 Self-RAG 全通过 → 无需标注
- **中置信度**：rerank_score 0.5-0.8 或 Self-RAG 重试 1 次后通过 → 标注"⚠️ 中置信度：[原因]"
- **低置信度**：rerank_score < 0.5 或 Self-RAG 重试 2 次仍不通过 → 标注"🔴 低置信度：[原因]，建议[下一步]"

### 步骤 5 — Self-RAG 质检（产出后关卡）

产出后，用 `resolver/prompts.md` 中的 `self-rag-checker` prompt 做质检：

| 检查项 | 含义 | 不通过时的动作 |
|---|---|---|
| **IsRel** | 产出是否与用户意图相关？ | 重新理解意图 |
| **IsSup** | 每段建议是否有 skill 支撑（provenance）？ | 补充 provenance 或重新召回 |
| **IsUse** | 产出对用户是否有用（可执行）？ | 重写执行步骤 |
| **IsConsistent** | 产出内部是否自相矛盾（同一决策点给出相反建议）？ | 重新走冲突消解 |
| **NeedRecall** | 是否需要重新召回？ | 扩大召回范围或拆新书 |

- `overall_pass = IsRel && IsSup && IsUse && IsConsistent`
- `confidence`: 0.0-1.0（>= 0.7 才算 pass）

**质检不通过时**：按失败项分级重试，不是统一"最多 2 次"：

| 失败项 | 重试范围 | 重试上限 |
|---|---|---|
| IsRel=false | 回到 intent-classifier 重新分档 | 1 次 |
| IsSup=false | 仅补充 provenance（不重召回） | 2 次 |
| IsUse=false | 仅重写产出 E 段 | 2 次 |
| IsConsistent=false | 重新走冲突消解 | 1 次 |
| NeedRecall=true | 扩大 coarse-recall 到 top-20 | 1 次，仍失败则标注低置信度 |

## 质量门

- [ ] 意图已被正确分档（A/B/C）+ 情境信号已提取
- [ ] 决策卡片命中检查已执行（步骤 0）
- [ ] A 档已做误判纠错（检查 KNOWN_CONFLICTS）
- [ ] 召回的 skill 都标注了来源书和召回理由
- [ ] CRAG 评估已执行（correct/ambiguous/incorrect）
- [ ] 冲突已被检测和标注（不能消音）
- [ ] 范式对立型冲突呈现了多元视角
- [ ] temporal 冲突已按情境选择新旧方法论
- [ ] 情境互补型冲突在信号不足时先给初步建议 + 补全提问（最多 1 轮）
- [ ] 产出按档位分级（A 档 2 段 / B 档 3 段 / C 档 6 段）
- [ ] 产出每段都有 provenance
- [ ] Self-RAG 质检已执行（IsRel/IsSup/IsUse/IsConsistent/NeedRecall）
- [ ] 兜底机制在召回为空/冲突不可消解时被触发，且引导行动

## 规模边界

当前规模（skill 数 < 500）无需分页，coarse-recall 直接做语义召回。

当 skill 数 > 500 时，coarse-recall 改为先按 tags 硬过滤缩小候选池（目标 ≤ 100 候选），再做语义召回。tags 过滤规则：
1. 从 intent-classifier 输出提取领域 tags
2. 硬过滤保留 tags 交集非空的 skill
3. 过滤后候选仍 > 100 时，按 source_book 权威性加权取 top-100

## 常见失败模式

1. **消音冲突** — 多书观点冲突时强行缝合，产出自相矛盾的建议。必须显式标注冲突。
2. **召回过宽** — top-10 里塞了不相关的 skill。精排要严格。
3. **意图误判** — 把 C 档（多框架冲突）误判为 A 档（简单），丢失多书视角。
4. **无兜底** — 召回为空时硬凑不相关的 skill。必须走兜底流程。
5. **无 provenance** — 产出不标注来源，用户无法追溯。每段必须有 `[来自《X》]`。
6. **CRAG 误用** — 把范式对立冲突归为 fallback。范式对立走 debate-protocol 是正常路径，不是 fallback。
