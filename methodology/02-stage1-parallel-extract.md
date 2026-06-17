# 阶段 1 — 6 个 sub-agent 并行提取

## 目标

不用单一视角读一遍,而是**同时从 6 个不同角度扫描全书**,最大化候选单元覆盖率。

## 为什么要并行

- **覆盖**: 单一视角会漏。框架提取器找不到的"反例",反例提取器会找到。
- **速度**: Claude Code 的 Agent 工具支持并行,不用白不用。
- **独立性**: 每个 extractor 独立判断,避免互相污染 — 三重验证才能真正起作用 (V1 跨域要求"独立出现")

## 共享精读机制 ★ (成本优化)

**原方案**: 6 个 extractor 各读一遍全书 → 成本 O(6N)
**新方案**: 阶段 0 的 L2 通读产出 `reading_notes.md` (章节摘要 + 关键段落定位) → 6 个 extractor 共享这份笔记,只在需要时回查原文 → 成本 O(N + 6N_note)

extractor 的工作模式变为:
1. 先读 `BOOK_OVERVIEW.md` (全局上下文)
2. 读 `reading_notes.md` (章节摘要,定位候选单元)
3. 对定位到的候选单元,回查原文对应段落 (精读)
4. 提取并输出

**单本模式例外**: 如果 `reading_notes.md` 不存在 (单本模式跳过了 L2),extractor 仍需自己读全书。但建议单本模式也做 L2 通读。

## 6 个 sub-agent

每个 sub-agent 接收:
- `BOOK_OVERVIEW.md` (阶段 0 产出, 提供全局上下文)
- `reading_notes.md` (L2 通读产出, 共享上下文) ★
- 书本文本 (或文本路径, 用于回查)
- 对应的 extractor prompt (`extractors/<type>-extractor.md`)
- (多书模式) `library/GLOSSARY_UNIFIED.md` — 已有术语词典,避免重复提取 ★

并在一次调用中通过 Agent 工具 **同时 spawn 6 个**,不是串行。

| # | extractor | 查找对象 | 产出文件 |
|---|---|---|---|
| 1 | framework-extractor | 思维模型 / 决策框架 / 推理方法 | `candidates/frameworks.md` |
| 2 | principle-extractor | 原则 / 清单 / 规则 / 断言 | `candidates/principles.md` |
| 3 | case-extractor | 作者在书中亲自使用的实例 | `candidates/cases.md` |
| 4 | counter-example-extractor | 作者警告的失败 / 反例 / 陷阱 | `candidates/counter-examples.md` |
| 5 | glossary-extractor | 关键概念词典 | `candidates/glossary.md` |
| 6 | decision-extractor ★ | 决策场景 / 决策流程 / 决策陷阱 | `candidates/decisions.md` |

## 每个候选单元的最小字段

无论是哪个 extractor,产出的每条候选单元必须包含:

```yaml
id: f01                           # 类型缩写 + 序号
title: 逆向思维                    # 简短标题
type: framework                   # framework / principle / case / counter-example / term
source_chapter: 第三讲             # 书中位置
source_quote: |                   # 原文引用 ≤150 字
  "反过来想,总是反过来想..."
summary: |                        # 用自己的话,5-10 行
  ...
tags: [decision, mental-model]    # 便于后续链接
```

## 输出前的自检

每个 extractor 在提交候选之前自问:
1. 这个单元**在书中**有明确根据吗? (不是我脑补)
2. 它属于我这个 extractor 的职责范围吗? (不要越界)
3. 它是不是已经在别处被别的 extractor 提取过了? (重复不是问题,阶段 1.5 会合并)

## 不在本阶段做的事

- **不做筛选** — 宁错杀,留给阶段 1.5 三重验证
- **不写 skill** — 只出候选,不出 SKILL.md
- **不做跨单元链接** — 留给阶段 3
- **不做跨书链接** — 留给阶段 5 (多书协同层)

## 多书模式的术语复用 ★

glossary-extractor 在多书模式下:
1. 先读 `library/GLOSSARY_UNIFIED.md` (如果存在)
2. 已有术语直接标记 `existing: true`,不重复提取
3. 只提取新术语或本书有不同用法的已有术语
4. 输出时标注 `new / variant / existing` 三种状态

decision-extractor 在多书模式下:
1. 先读 `library/THEME_INDEX.md` (如果存在)
2. 已有决策场景标记 `existing: true`,只补充新场景
3. 对已有场景的新视角,标记 `adds_perspective_to: <existing_id>`
