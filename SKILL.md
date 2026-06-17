---
name: book2skill
description: Distill a book into a coherent set of executable skills. Use when the user asks to "拆书" / "蒸馏一本书" / "把 XX 书做成 skill" / "把书变成技能" / "拆解这本书" / "提取书里的方法论" / "turn a book into skills" / "distill book into skills" / "extract skills from book" / "book to skill" — i.e. wants a book's frameworks, principles, and methodologies extracted into atomic, reusable Claude skills that an agent can invoke in real-world situations. Supports both single-book mode and multi-book mode (融合打通多本书形成决策知识网络). NOT for simple summarization, book reviews, or role-playing as the author (that is nuwa-skill's job).
---

# book2skill — 把一本书或一组书蒸馏成可执行 skills 的元 skill

## 使命

把一本书或一组书里沉淀的方法论,拆解成**原子化、可被 agent 在真实场景下调用**的 skills,让读者真正用起来。

**边界**:
- ✅ 做: 方法论 / 决策框架 / 清单 / 原则 / 概念体系的蒸馏
- ✅ 做 (多书模式): 跨书主题聚合 / 决策场景反向索引 / 方法论对比矩阵 / 冲突记录
- ❌ 不做: 书摘 / 读后感 / 作者人设角色扮演 (后者请用 nuwa-skill)

## 两种模式

### 单本模式 (默认)
一本书 → 一组 atomic skills。适用于单本蒸馏。

### 多书模式 ★ (新增)
多本书 → 跨书知识网络 → 决策导向工具集。适用于"融合打通多本书形成知识指导决策"。

**多书模式触发信号**:
- 用户说"多本书" / "批量" / "融合打通" / "形成一个知识体系"
- 用户给出 2+ 本书的路径
- 用户说"指导决策"且书单跨领域

## 核心方法论: RIA-TV++ (单本) + Library Layer (多书)

单本流水线沿用 RIA-TV++,多书模式在单本流水线之上增加 Library Layer 和 Decision Layer。

```
单本流水线 (每本书独立执行):
  阶段 -1: 快速扫描 (多书模式)     → SCAN_NOTES.md
  阶段 0:  Adler 整书理解          → BOOK_OVERVIEW.md + reading_notes.md
  阶段 1:  6 个 agent 并行提取     → 候选方法论单元池
  阶段 1.5: 三重验证筛选           → 通过的单元
  阶段 2:  RIA++ 构造 skill        → 每个 skill 的 SKILL.md
  阶段 3:  Zettelkasten 链接       → INDEX.md
  阶段 4:  压力测试 (darwin 兼容)  → test-prompts.json + 回炉淘汰

多书协同层 (所有单本完成后执行):
  阶段 5:  多书协同层              → LIBRARY_OVERVIEW + THEME_INDEX + GLOSSARY_UNIFIED + CONFLICTS
  阶段 6:  决策导向产出            → DECISION_INDEX + DECISION_CARDS + COMPARISON_MATRIX
```

详见 `methodology/00-overview.md`。

## 何时调用此 skill

用户说类似:
- "帮我拆《穷查理宝典》" → 单本模式
- "把毛选蒸馏成 skill" → 单本模式
- "distill this book into skills: <path>" → 单本模式
- "我想把这本书的方法论做成可用的 skill" → 单本模式
- "我有 5 本书,想融合打通形成知识体系" → 多书模式 ★
- "这些书需要通读,整理内容指导决策" → 多书模式 ★
- "批量蒸馏这些书" → 多书模式 ★

## 输入要求

在开始前**必须**从用户处确认:
1. **书的文本来源**: PDF / EPUB / TXT / DOCX 文件路径, 或可访问的纯文本。**不要**在没有文本的情况下"凭记忆"拆书 — 宁可停下来问用户要。
2. **书名 + 作者 + 出版年**: 用于目录命名和审计。
3. **模式选择**: 单本还是多书? (多书模式需要 2+ 本书)
4. **决策导向** (多书模式): 用户主要想指导什么类型的决策? (商业/投资/管理/个人成长/...)
5. **是否首次试点**: 如果用户是第一次用 book2skill,建议先拆 1 本验证流程再批量。

## 输出结构

### 单本模式

```
books/<book-slug>/
├── BOOK_OVERVIEW.md           # 阶段 0 产出: 主旨/骨架/术语/批判
├── reading_notes.md           # 阶段 0 产出: L2 通读笔记 (extractor 共享上下文) ★
├── SCAN_NOTES.md              # 阶段 -1 产出: 快速扫描 (多书模式才有)
├── INDEX.md                   # 阶段 3 产出: skill 总览 + 引用图
├── candidates/                # 阶段 1 产出: 原始候选池 (审计用)
├── rejected/                  # 阶段 1.5 淘汰的单元 + 原因 (审计用)
├── <skill-slug-1>/
│   ├── SKILL.md
│   └── test-prompts.json      # darwin-skill 兼容格式
├── <skill-slug-2>/
│   └── ...
```

### 多书模式 ★

```
library/                        # 多书协同层
├── LIBRARY_OVERVIEW.md         # 知识库主旨、书单、覆盖矩阵
├── THEME_INDEX.md              # 跨书主题聚合
├── DECISION_INDEX.md           # ★ 决策场景反向索引 (核心)
├── GLOSSARY_UNIFIED.md         # 跨书统一术语词典
├── CONFLICTS.md                # 跨书冲突记录
├── COMPARISON_MATRIX.md        # 同主题方法论对比矩阵
├── DECISION_CARDS/             # 决策卡片 (一页纸压缩版)
│   ├── {{decision-1}}.md
│   └── ...
└── books/                      # 每本书独立的单本产出
    ├── <book-1-slug>/
    │   └── ... (单本结构)
    ├── <book-2-slug>/
    │   └── ...
    └── ...
```

## 执行流程

### 单本模式流程 (严格按顺序)

#### 阶段 0 — 整书理解

1. 读取用户提供的书本文本。大文件按 `methodology/01-stage0-adler.md` 的分层阅读策略处理。
2. 执行 `methodology/01-stage0-adler.md` 中的 Adler 四步 (结构 / 解释 / 批判 / 应用)。
3. 按 `templates/BOOK_OVERVIEW.md.template` 填充,写入 `books/<slug>/BOOK_OVERVIEW.md`。
4. 同时产出 `reading_notes.md` (章节摘要,供阶段 1 的 extractor 共享使用)。
5. 把产出展示给用户确认:"骨架我理解对了吗?有没有你希望重点突出的方向?" 得到确认再进入阶段 1。

#### 阶段 1 — 6 个 sub-agent 并行提取

**并行** spawn 6 个 Task sub-agents(使用 Agent 工具,一次调用中发起 6 个):

| sub-agent | 读取的 prompt | 产出 |
|---|---|---|
| 框架提取器 | `extractors/framework-extractor.md` | 决策框架 / 思维模型 |
| 原则提取器 | `extractors/principle-extractor.md` | 原则 / 清单 / 规则 |
| 案例提取器 | `extractors/case-extractor.md` | 作者在书中亲自使用过的实例 |
| 反例提取器 | `extractors/counter-example-extractor.md` | 书中警告的失败模式 |
| 术语提取器 | `extractors/glossary-extractor.md` | 关键概念词典 |
| 决策提取器 ★ | `extractors/decision-extractor.md` | 决策场景 / 决策流程 / 决策陷阱 |

每个 sub-agent 共享 `BOOK_OVERVIEW.md` 和 `reading_notes.md`,独立提取、独立输出到 `books/<slug>/candidates/<type>.md`。

#### 阶段 1.5 — 三重验证筛选

读取 `methodology/03-stage1.5-triple-verify.md`,对每个候选单元执行:

- **V1 跨域**: 书中至少 2 个独立段落有佐证?
- **V2 预测力**: 能用它回答一个书里没明说的新问题吗?
- **V3 独特性**: 不是任何聪明人都会说的常识吗?

通过的进入阶段 2。不通过的写入 `books/<slug>/rejected/` 并附原因。

**检查点 ★**: 展示候选池汇总 (通过数/淘汰数/各类型分布),询问用户:"筛选结果合理吗?有没有想强制保留或淘汰的?" 得到确认再进入阶段 2。

#### 阶段 2 — RIA++ 构造 skill

对每个通过的单元,按 `templates/SKILL.md.template` 填充 R/I/A1/A2/E/B 六段。细则见 `methodology/04-stage2-ria-plus.md`。

**检查点 ★**: 第一个 skill 构造完成后,展示给用户:"这个 skill 的 RIA++ 结构对吗?边界条件 B 段写得准吗?" 得到确认再批量构造剩余 skill。

#### 阶段 3 — Zettelkasten 链接

按 `methodology/05-stage3-zettelkasten.md` 建立 skill 间链接,生成 `INDEX.md`。

#### 阶段 4 — 压力测试 (darwin 兼容)

按 `methodology/06-stage4-pressure-test.md` 设计测试 prompt,未过的回炉重做阶段 2。

**检查点 ★**: 压力测试完成后,展示通过率和不通过原因,询问用户:"要不要回炉重做失败的 skill,还是直接淘汰?"

---

### 多书模式流程 ★ (新增)

#### 步骤 1 — 批量快速扫描 (阶段 -1)

对所有书执行快速扫描 (见 `methodology/01-stage0-adler.md` 的阶段 -1 部分):
1. 每本书读目录/序言/结语/章节首尾
2. 产出 `books/<slug>/SCAN_NOTES.md`
3. 汇总到 `library/LIBRARY_OVERVIEW.md` (初版,只含书单和定位)
4. 与用户确认:"这些书的定位我理解对了吗?优先级排序合理吗?"

#### 步骤 2 — 按优先级逐本执行单本流水线

按 LIBRARY_OVERVIEW 的优先级排序,逐本执行阶段 0-4:
1. 第 1 本 (最高优先级) 完整跑完阶段 0-4
2. 第 2 本开始,extractor 读取 `library/GLOSSARY_UNIFIED.md` (如果已有) 做术语复用
3. 每本完成后,增量更新 `library/GLOSSARY_UNIFIED.md` 和 `library/THEME_INDEX.md`
4. 发现跨书冲突时,立即记录到 `library/CONFLICTS.md`

**不要并行跑多本书的单本流水线** — 顺序执行,确保每本都能复用前面的产出。

#### 步骤 3 — 多书协同层 (阶段 5)

所有单本完成后,执行 `methodology/07-stage5-multi-book-library.md`:
1. 完善 `LIBRARY_OVERVIEW.md` (覆盖矩阵、推荐顺序)
2. 完善 `THEME_INDEX.md` (跨书主题聚合 + 跨书关系集中维护)
3. 完善 `GLOSSARY_UNIFIED.md` (术语冲突解决)
4. 完善 `CONFLICTS.md` (跨书冲突记录)
5. **不回填单本 SKILL.md** — 跨书关系集中在 library/ 层维护,保持单本 SKILL.md 纯净

#### 步骤 4 — 决策导向产出 (阶段 6) ★

执行 `methodology/08-stage6-decision-index.md`:
1. 收集决策场景 (从 decision-extractor 产出 + 用户实际需求)
2. 构建 `DECISION_INDEX.md` (决策场景 → skill 组合反向索引)
3. 生成 `DECISION_CARDS/` (一页纸决策卡片)
4. 生成 `COMPARISON_MATRIX.md` (同主题方法论对比)
5. **用户验证**: 拿 2-3 个真实决策场景让用户走一遍,看流程是否跑得通

## 质量红线 (违反则阻止输出)

### 单本红线
1. 每个 skill 必须通过**全部**三重验证
2. 每个 skill 必须有完整的 R / I / A1 / A2 / E / B 六段
3. 原文引用 ≤150 字/段
4. 每个 skill 必须有 `test-prompts.json`,且包含诱饵测试
5. `description` 字段必须明确 trigger 条件

### 多书红线 ★
6. `DECISION_INDEX` 必须按决策场景组织 (不按书、不按主题)
7. 每个决策场景至少组合 2 个 skill
8. `CONFLICTS.md` 不选边站,只记录差异和适用条件
9. `GLOSSARY_UNIFIED.md` 保留 per_book_usage,不抹平差异
10. 跨书 `related_skills` 必须有 note 说明价值

## 与 nuwa-skill / darwin-skill 的生态定位

- **nuwa-skill**: 蒸馏人 (思维方式 / 表达 DNA)
- **book2skill** (本 skill): 蒸馏书 (方法论 / 框架 / 原则), 支持单本和多书
- **darwin-skill**: 进化任意 skill

三者咬合: 本 skill 输出的 `test-prompts.json` 严格遵循 darwin-skill 格式;多书模式的 DECISION_INDEX 可作为 nuwa-skill 蒸馏"决策者人设"的素材。

## 调用惯例

### 单本模式
- **永远先试点 1 本** — 除非用户明确说"批量"
- **阶段之间主动汇报进度** — 不要静默跑完再 dump 结果
- **不凭记忆拆书** — 没文本就停下来问
- **保留审计轨迹** — candidates/ 和 rejected/ 都要留

### 多书模式 ★
- **先扫描全部,再精读** — 不要拿到书单就开始精读第一本
- **顺序执行,不并行** — 每本要复用前面的产出
- **冲突立即记录** — 发现跨书冲突时立即写入 CONFLICTS.md,不要等最后
- **决策导向验证** — 阶段 6 完成后必须用真实场景验证
- **增量更新** — 每本完成后更新 library/,不要等所有书都跑完

## 异常处理与边界条件

### 文本输入异常

| 异常 | 检测 | 处理 |
|---|---|---|
| PDF 提取失败 / 文本为空 | 阶段0读取后字数 < 1000 | 停下告知用户，建议用 OCR (scripts/ocr_pdf.py) 或换格式 |
| 书太长 (>50万字) | 阶段0字数统计 | 切换分层阅读：先读目录/序言/章节首尾，按需深读，不全文通读 |
| OCR 质量差 (乱码率>30%) | 阶段0抽样检查 | 停下告知用户，建议人工校对关键章节或换源 |
| 格式不支持 (非PDF/EPUB/TXT/DOCX) | 输入检查 | 停下要求用户转为支持的格式 |

### Extractor 异常

| 异常 | 检测 | 处理 |
|---|---|---|
| 某个 extractor 输出为空 | 阶段1产出检查 | 不报错，记录到 candidates/<type>.md 标注"无候选"，继续其他 extractor |
| extractor 输出重复率高 | 阶段1.5去重检查 | 合并重复项，保留最完整的版本 |
| 三重验证全部不通过 | 阶段1.5结果 | 停下告知用户"本书未提取到可技能化的方法论"，询问是否调整验证标准 |

### 执行流程异常

| 异常 | 检测 | 处理 |
|---|---|---|
| 用户中途取消 | 用户明确叫停 | 保存当前进度到 candidates/，告知用户可从哪个阶段恢复 |
| 阶段2 RIA++ 构造卡住 | 单个 skill 构造超过3次失败 | 跳过该候选，记入 rejected/，继续下一个 |
| 压力测试连续失败 | 阶段4 同一 skill 3次不过 | 回炉阶段2重写，仍不过则淘汰记入 rejected/ |
| 多书模式中书单变化 | 用户中途增删书 | 重新执行阶段-1扫描，已完成的单本产出保留 |

### Fallback 路径

1. **文本源 fallback**: PDF→OCR→人工转录→换源
2. **extractor fallback**: 单个 extractor 失败不影响其他5个，最终汇总时补齐
3. **阶段恢复**: 任何阶段中断后，可从该阶段重新开始（candidates/ 保留中间产出）
