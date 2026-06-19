# 阶段 4.5 — 全局索引汇聚（Library Build）

## 目标

在单书蒸馏流水线（阶段 0-4）之后、多书协同流水线（阶段 5-6）之前，把多本书的产出**汇聚成全局索引层**，让阶段 5 的粗召/精排有东西可查。

本阶段是单书 → 多书的**桥梁**。

## 触发时机

- 每拆完一本新书后（阶段 4 通过后），自动触发本阶段
- 或用户手动触发"更新全局索引"

## 前置条件

- 至少有 1 本已拆完的书（`books/<book-slug>/INDEX.md` 存在）

## 产出

```
library/
├── GLOBAL_INDEX.md          # 全局 skill 索引（所有书的 skill 扁平列表）
├── GLOSSARY_UNIFIED.md      # 统一术语表（跨书术语消解）
├── CONFLICTS.md             # 跨书冲突列表（已知冲突沉淀）
├── external-packs.json      # 外部 skill packs 清单
└── DECISION_CARDS/          # 决策卡片目录（阶段 6 产出）
```

### library/ 保护机制

library/ 文件支持用户自定义修改，自动生成段与用户自定义段分离：

- 自动生成段用 `<!-- AUTO-GEN START -->` / `<!-- AUTO-GEN END -->` 标记
- 自动汇聚只覆盖 AUTO-GEN 段，保留标记外的用户自定义段
- 每个 library/ 文件的 frontmatter 增加 `auto_gen: true` 标记
- 增量追加段用 `<!-- AUTO-GEN INCREMENTAL START -->` / `<!-- AUTO-GEN INCREMENTAL END -->` 标记

## 三步汇聚流程

### 步骤 1 — 汇聚全局 skill 索引

读取所有 `books/*/INDEX.md`，按 `templates/GLOBAL_INDEX.md.template` 填充 `library/GLOBAL_INDEX.md`。

**汇聚规则**：
1. 每本书的每个 skill 提取：skill_id、source_book、description、tags、source_chapter
   - **物理 slug**：从 SKILL.md frontmatter `name` 字段提取（无前缀，v1.0 兼容）
   - **逻辑 skill_id**：由阶段 4.5 汇聚时拼接 `<book-slug>::<物理 slug>`
   - **source_book**：从 SKILL.md frontmatter 提取，**不从 test-prompts.json 提取**
   - v1.0 已有的 packs 无需修改物理 slug
2. 按主题分组（tags 聚类）
3. 标注跨书关系（来自各书的 `related_skills` 字段，跨书的用 `cross-book: true` 标记）
4. 生成全局 mermaid 引用图

### 外部 skill packs 汇聚

v1.0 的 14 个 packs 是独立仓库，通过 `library/external-packs.json` 清单文件纳入汇聚：

```json
[
  {
    "git_url": "https://github.com/xxx/yyy-pack",
    "book-slug": "yyy",
    "skills": ["skill-a", "skill-b"],
    "authority_tier": "B"
  }
]
```

阶段 4.5 读取此清单，把外部 packs 的 skill 纳入 GLOBAL_INDEX（skill_id 同样用 `<book-slug>::<skill-slug>` 格式）。

### 步骤 2 — 汇聚统一术语表

读取所有 `books/*/candidates/glossary.md`（阶段 1 产出），按 `templates/GLOSSARY_UNIFIED.md.template` 填充 `library/GLOSSARY_UNIFIED.md`。

**降级策略**：如果 GLOSSARY_UNIFIED.md 为空或不存在，跳过术语消解步骤，不报错。阶段 5 的 coarse-recall 在 `{{GLOSSARY_UNIFIED}}` 缺失时默认跳过术语消解。

**术语消解规则**：
1. **同名异义**：多本书用同一个词但含义不同 → 保留各自定义，标注 `conflicts_with`
2. **异名同义**：不同词但含义相同 → 合并为一条，标注 `aliases`
3. **跨书映射**：每本书的术语映射到全局术语 ID（`maps_to_global`）

### 步骤 3 — 检测跨书冲突

读取所有 `books/*/BOOK_OVERVIEW.md` 的批判段 + 所有 skill 的 B 段（Boundary），按 `templates/CONFLICTS.md.template` 填充 `library/CONFLICTS.md`。

**冲突检测规则**：
1. 扫描所有 skill 的 B 段，找"作者警告的失败模式"
2. 交叉对比：A 书的正面 skill 是否被 B 书的反例/批判所限制？
3. 对每个检测到的冲突，分类：
   - `situational`（情境互补型）：可消解
   - `paradigmatic`（范式对立型）：不可消解
   - `temporal`（时代演变型）：按时间线标注
4. 编号：C01、C02、...
5. 每条冲突记录：涉及的 skill（用 `<book-slug>::<skill-slug>` 格式）、冲突类型、各自立场、消解提示、`last_verified_date`

**CONFLICTS.md 全量 vs 增量明确**：
- **主"冲突列表"段**：全量重建（基于最新 B 段），用 `<!-- AUTO-GEN START -->` / `<!-- AUTO-GEN END -->` 标记
- **"冲突检测日志"段**：增量追加（保留历史轨迹），用 `<!-- AUTO-GEN incremental START -->` / `<!-- AUTO-GEN incremental END -->` 标记
- 运行时新冲突先写入日志段，下次阶段 4.5 全量重建时合并到主列表

**CONFLICTS.md 与运行时 conflict-detector 的关系**：
- CONFLICTS.md 是**历史冲突沉淀**（已知冲突的静态记录），用于阶段 5 精排阶段做 hint 加权
- `resolver/prompts.md` 的 `conflict-detector` 是**运行时新冲突检测**（检测召回 skill 之间的即时冲突）
- 运行时检测到的新冲突应**回写**进 CONFLICTS.md 的日志段（增量更新）

### 冲突重检触发条件

不是只有拆新书才重检冲突，以下场景都触发：

- **(a) 拆新书后**：全量重检（重跑步骤 3）
- **(b) darwin 进化后**：增量重检（只重检被进化 skill 相关的冲突）
- **(c) 用户手动修改 B 段后**：重检该 skill 相关的冲突

在 CONFLICTS.md 每条冲突增加 `last_verified_date` 字段，用于判断是否需要重检。

### 引用完整性检查（独立工具）

引用完整性检查（全局引用图无断链）不只在阶段 4.5 执行，而是**独立工具**，可在任意时刻调用：

- darwin 进化后（skill 内容变更可能导致引用失效）
- skill 重命名后（slug 变更会导致引用断链）
- 阶段 4.5 汇聚后（常规检查）

调用方式：检查所有 `related_skills`、`conflicts_with`、`composes-with` 引用都能找到目标 skill。

### skill slug 变更同步

**推荐策略**：禁止重命名 atomic skill 的物理 slug（一旦发布就锁定），只能新增/废弃。

如果必须重命名：
1. 跑"slug 迁移"工具，更新所有引用（GLOBAL_INDEX、CONFLICTS、DECISION_CARDS、related_skills）
2. 重新跑引用完整性检查
3. 在 CONFLICTS.md 日志段记录 slug 变更

## 质量门

- [ ] GLOBAL_INDEX.md 包含所有已拆书的 skill（无遗漏）
- [ ] GLOBAL_INDEX.md 的 skill_id 用 `<book-slug>::<skill-slug>` 格式
- [ ] 外部 packs 已通过 external-packs.json 纳入 GLOBAL_INDEX
- [ ] GLOSSARY_UNIFIED.md 对每个同名异义术语标注了 `conflicts_with`（或降级跳过）
- [ ] CONFLICTS.md 对每个冲突标注了类型、消解提示、`last_verified_date`
- [ ] CONFLICTS.md 主列表（全量）与日志段（增量）分离，用 AUTO-GEN 标记
- [ ] library/ 文件的 AUTO-GEN 段与用户自定义段分离
- [ ] 全局引用图无断链（所有 `related_skills`、`conflicts_with`、`composes-with` 引用都能找到目标）

## 常见失败模式

1. **术语消解过松** — 把含义相近但实质不同的术语合并。宁可保留分歧也不要强行合并。
2. **冲突检测漏报** — 只检测正面 skill 之间的冲突，忽略了反例/批判段隐含的冲突。
3. **索引不更新** — 拆完新书后忘记重新汇聚。每次拆完新书必须重跑本阶段。
4. **AUTO-GEN 段覆盖用户修改** — 全量重建时未用 AUTO-GEN 标记保护用户自定义段，导致修改丢失。
5. **slug 变更未同步** — 重命名 skill 后未跑 slug 迁移，导致引用断链。
