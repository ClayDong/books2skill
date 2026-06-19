# CLAUDE.md — cangjie-skill 项目工作规则

> 本文件是本项目的最高工作约束。任何迭代都必须遵守。

## 项目定位

cangjie-skill 是一个 **book2skill 元 skill 框架**：把书蒸馏成可被 agent 调用的 atomic skills。

- **单书蒸馏**（v1.0，已稳定）：RIA-TV++ 流水线，阶段 0-4
- **多书协同**（v2.0，本次新增）：意图驱动编排层，阶段 5-6

## 架构原则（不可违反）

### 1. 编排层不破坏原子层

- atomic skill（单书产出）遵守原子性不变量：一个 skill 只做一个方法论单元
- orchestrator（多书编排）是 atomic skill 之上的调度抽象，不是新类型 skill
- 已有的 14 个 skill packs 必须保持向后兼容

### 2. 推式与拉式分离

- **推式（push）= 单书蒸馏**：用户给书 → 产出 skills。走阶段 0-4
- **拉式（pull）= 多书协同**：用户给意图 → 召回多书 skills → 整合产出。走阶段 5-6
- 两条流水线解耦，不互相阻塞

### 3. 冲突不消音

- 多书观点冲突时，不强行给单一答案
- 区分三类冲突：情境互补型（可消解）/ 范式对立型（保留分歧）/ 时代演变型（标注时间线）
- 范式对立型必须呈现多元视角，让用户决策

### 4. 失败必须引导

- 召回为空：告知 + 推荐最接近的 top-3 + 建议拆新书
- 冲突不可消解：输出多视角对照表 + 各自适用前提
- 意图模糊：触发澄清式提问，不猜测

## 目录结构（v2.0）

```
cangjie-skill/
├── CLAUDE.md                    ← 本文件
├── SKILL.md                     ← 元 skill 定义
├── methodology/                 ← 方法论文档
│   ├── 00-overview.md           ← RIA-TV++ 总览
│   ├── 01-stage0-adler.md       ← 阶段0：整书理解
│   ├── 02-stage1-parallel-extract.md
│   ├── 03-stage1.5-triple-verify.md
│   ├── 04-stage2-ria-plus.md
│   ├── 05-stage3-zettelkasten.md
│   ├── 06-stage4-pressure-test.md
│   ├── 07-stage5-multi-book-orchestration.md  ← 新增：多书协同编排
│   ├── 08-stage6-decision-cards.md            ← 新增：决策卡片构造
│   └── 09-stage4.5-library-build.md           ← 新增：全局索引汇聚（文件名编号虽在最后，执行顺序在阶段 4 和阶段 5 之间）
├── extractors/                  ← 5 个并行提取器
│   ├── framework-extractor.md
│   ├── principle-extractor.md
│   ├── case-extractor.md
│   ├── counter-example-extractor.md
│   └── glossary-extractor.md
├── templates/                   ← 模板
│   ├── SKILL.md.template
│   ├── BOOK_OVERVIEW.md.template
│   ├── INDEX.md.template
│   ├── test-prompts.json.template
│   ├── DECISION_CARD.md.template              ← 新增
│   ├── orchestration-test-prompts.json.template  ← 新增
│   ├── GLOBAL_INDEX.md.template               ← 新增
│   ├── GLOSSARY_UNIFIED.md.template           ← 新增
│   └── CONFLICTS.md.template                  ← 新增
├── router/                      ← 新增：意图驱动路由层
│   └── prompts.md
├── resolver/                    ← 新增：冲突消解层
│   └── prompts.md
└── library/                     ← 新增：多书协同产出层（运行时生成）
    ├── GLOBAL_INDEX.md
    ├── GLOSSARY_UNIFIED.md
    ├── CONFLICTS.md
    └── DECISION_CARDS/
```

**library/ 保护机制**：
- 自动生成段用 `<!-- AUTO-GEN START -->` / `<!-- AUTO-GEN END -->` 标记
- 用户自定义段在标记外，自动汇聚时保留

## 工作流（v2.0，9 阶段）

### 单书蒸馏流水线（push，阶段 0-4）

不变，见 `methodology/00-overview.md`。

### 阶段 4.5 — 全局索引汇聚（push→pull 桥梁）

- **触发时机**：每拆完一本新书后自动触发，无需用户干预
- **产出**：`library/GLOBAL_INDEX.md` + `GLOSSARY_UNIFIED.md` + `CONFLICTS.md`
- **外部 skill packs 汇聚**：v1.0 的 14 个 packs 是独立仓库，通过 `library/external-packs.json` 清单文件纳入汇聚。清单格式：`[{git_url, book-slug, skills: [skill-slug list]}]`
- 详见 `methodology/09-stage4.5-library-build.md`

### 多书协同流水线（pull，阶段 5-6）

#### 阶段 5 — 多书协同编排

1. **意图理解**：用户提出意图 → 意图分类器分档（A 简单 / B 单框架 / C 多框架冲突）
2. **粗召**：从全局 skill 索引中按语义 + tags 召回 top-10 候选
3. **精排**：cross-encoder / LLM-as-judge 按意图相关度重排，取 top-3
4. **冲突检测**：对 top-3 两两做立场冲突检测
5. **冲突消解**：按冲突类型（情境互补 / 范式对立 / 时代演变）走不同策略
6. **兜底**：召回为空 / 冲突不可消解 / 意图模糊时走兜底流程

详见 `methodology/07-stage5-multi-book-orchestration.md`。

#### 阶段 6 — 决策卡片构造

对高频决策场景（如"该不该止损""该不该跳槽"），产出决策卡片：
- 决策情境分类（五维度）：
  - **可逆性**：不可逆 / 高成本可逆 / 低成本可逆（三档）
  - **影响范围**：仅自己 / 涉及他人 / 组织级
  - **时间压力**：紧急 / 充裕
  - **信息完备度**：充分 / 不足
  - **利益相关方**：仅自己 / 涉及他人 / 需他人执行
  - 维度优先级：可逆性 > 利益相关方 > 信息完备度 > 时间压力
- 参与的 skill 列表（标注角色：前置 / 核心 / 校验 / 兜底）
- 编排流程（DAG 图）
- 冲突仲裁规则
- 决策日志模板

详见 `methodology/08-stage6-decision-cards.md`。

## 质量红线（v2.0）

### 单书蒸馏红线（不变）

1. 每个 skill 必须通过三重验证
2. 每个 skill 必须有完整的 R/I/A1/A2/E/B 六段
3. 原文引用 ≤150 字/段
4. 每个 skill 必须有 test-prompts.json，含诱饵测试
5. description 字段必须明确 trigger 条件

### 多书协同红线（新增）

6. 编排层必须显式声明编排逻辑，不能是简单堆叠
7. 冲突必须被检测和标注，不能消音
8. 范式对立型冲突必须呈现多元视角
9. 每张决策卡片必须有冲突仲裁规则
10. 召回为空时必须走兜底流程，不能幻觉编造

## 命名规范

- 物理 slug（SKILL.md frontmatter name、test-prompts.json skill、书内 INDEX.md）：`<skill-slug>`（无前缀，v1.0 兼容，不变）
- 逻辑 skill_id（GLOBAL_INDEX、CONFLICTS、DECISION_CARD、router/resolver）：`<book-slug>::<skill-slug>`（跨书唯一，双冒号分隔）
- v1.0 已有的 14 个 skill packs 无需修改物理 slug，阶段 4.5 汇聚时自动拼接逻辑 skill_id
- 决策卡片：`<scenario-slug>.md`（如 `stop-loss.md`）
- 冲突编号：`C01`、`C02`...
- 意图分档：A（简单）/ B（单框架）/ C（多框架冲突）

## 版本

- v1.0：单书蒸馏（RIA-TV++ 阶段 0-4）
- v2.0：新增多书协同（阶段 5-6 + router/ + resolver/ + library/）
