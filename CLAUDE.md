# CLAUDE.md

> 藏经阁项目 (cangjie-skill / book2skill) 专属工作规则
> 本文件给 AI 助手(Claude/Trae) 阅读,约束在该项目目录下的所有行为

---

## 一、项目是什么

**藏经阁 = 多本书 → 跨书知识网络 → 决策支持系统**

- 输入: 一本/多本书(PDF/EPUB/DOCX)
- 输出: 一组 atomic skill + 跨书整合层 + 决策路由
- 用户: 给自己用,核心场景是投资决策 + 人生决策

**当前状态(v1.0)**:
- 3 本书已完成 (炒股的智慧 / 周易 / 大师兄)
- 20 个 skill
- 1 个元 skill (skill-router)
- 2 本书等 OCR (曼昆经济学 / 共同富裕)

---

## 二、目录结构约定

```
cangjie-skill/
├── SKILL.md                    # book2skill 元 skill 描述
├── README.md / README.en.md / README.ja.md
├── GITHUB_REPO.md              # GitHub 仓库元信息
├── LICENSE
│
├── extractors/                 # 6 个提取器(框架/原则/案例/反例/术语/决策)
├── methodology/                # 8 阶段方法论(00-08)
├── templates/                  # 所有 .md 模板
├── scripts/                    # 工具脚本 (ocr / extract / check)
│
├── library/                    # ★ 跨书整合层 (藏经阁核心)
│   ├── LIBRARY_OVERVIEW.md     # 跨书整合总览
│   ├── QUICK_START.md          # 快速使用
│   ├── STATUS_REPORT.md        # 状态报告
│   ├── DEMO_DECISION_REPORT.md # 决策报告样例
│   ├── SCAN_NOTES.md           # 阅读笔记
│   ├── skill-router/           # 元 skill
│   └── books/                  # 每本书一个目录
│       └── <书名>/
│           ├── BOOK_OVERVIEW.md       # 阶段0 产出
│           ├── verified.md            # 阶段1.5 验证后清单
│           ├── rejected.md            # 阶段1.5 拒绝清单
│           ├── SKILL_INDEX.md         # 阶段3 索引
│           ├── pressure-test.md       # 阶段4 压力测试
│           ├── EXTRACTION_LOG.md      # 完整流程日志
│           ├── candidates/            # 阶段1 候选(6 个文件)
│           └── skills/                # 阶段2 产出(每 skill 一个目录)
│               └── <skill-name>/
│                   └── SKILL.md
│
└── tests/                      # 测试用例
```

---

## 三、命名约定

### 书籍目录
- 用书名,不加任何前缀
- 例: `炒股的智慧/` `周易决策智慧精要/` `大师兄/`

### skill 命名
- 格式: `<书前缀>-<核心概念>`
- 书前缀映射:
  - 炒股的智慧 → `stock-`
  - 周易 → `i-ching-`
  - 大师兄 → `dashixiong-`
  - 曼昆经济学 → `econ-` (待用)
  - 共同富裕 → `policy-` (待用)
- 例: `stock-trend-judgment`, `i-ching-time-position`, `dashixiong-keep-one-bite`

### 跨书 skill
- 命名: 不带书前缀,用功能命名
- 例: `skill-router`

---

## 四、工作流约定 (每本书)

按 `methodology/` 目录的 8 个阶段执行:

1. **阶段0 - Adler 分析**: 读 BOOK_OVERVIEW.md.template, 产出 BOOK_OVERVIEW.md
2. **阶段1 - 并行提取**: 5-6 个 extractors 并行, 写到 `candidates/`
3. **阶段1.5 - 三重验证**: 验证+拒绝, 写到 `verified.md` + `rejected.md`
4. **阶段2 - RIA++ 构造**: 用 SKILL.md.template, 每个 skill 一个目录
5. **阶段3 - Zettelkasten 链接**: 找出 skill 间关系, 写到 SKILL_INDEX.md
6. **阶段4 - 压力测试**: 写到 pressure-test.md
7. **阶段5 - 跨书整合**: 写到 LIBRARY_OVERVIEW.md (Library Layer)
8. **阶段6 - 决策索引**: 决策场景反向索引 (DECISION_INDEX)

每个阶段都要写日志到 `EXTRACTION_LOG.md`。

---

## 五、OCR 规则

- **纯文本 PDF**: 用 pdfplumber 直接提取
- **扫描版 PDF**: 用 PaddleOCR (PaddleOCR<3, paddlepaddle<3.3.1)
- **DOCX**: 用 python-docx
- **EPUB**: 用 ebooklib

### OCR 输出约定

- 输出文件: `<书名>.txt`, 跟 PDF 同目录
- 中间文件: `<书名>.txt.tmp`, 每页处理完就追加,中断不会丢
- DPI: 150 (提速)
- 不跳过已处理: 加 `--no-skip` 才不跳

### OCR 命令

```bash
python scripts/ocr_pdf.py <pdf_path> <output_txt> --dpi 150
```

---

## 六、用户偏好 (来自全局)

- **不做的事**:
  - 不要谄媚、不要说"很好的问题"
  - 不要重复用户说过的话
  - 不要预估时间
  - 不要问"你确定吗" (除非有真实风险)
- **要做的事**:
  - 第一性原理思考
  - 结论先行
  - 遇到模糊需求先给最合理方案
  - 中文为主,代码/命令/变量用英文
  - 改完主动跑验证
  - commit message 用英文

---

## 七、决策原则 (来自全局)

1. **约束先行**: 改任何约定前先改文档
2. **UX 优先**: 后端可以复杂,用户碰到的必须丝滑
3. **避免过度工程**: 只做被请求的事
4. **避免向后兼容 hack**: 直接改不要 shim

---

## 八、Git 约定

- 仓库: `https://github.com/ClayDong/books2skill.git`
- 默认分支: `main`
- 推送: 仅用户明确指令才推 (跨设备同步用)
- commit message: 英文, 简洁描述变更意图
- **不推大文件**:
  - `.tmp` (OCR 中间文件)
  - `*.pdf`
  - OCR 输出文件 (`*.txt`, 在 D:\我的资料\书籍\ 不在本仓库)
  - `__pycache__/`
  - `.DS_Store`

---

## 九、与全局 CLAUDE.md 的关系

- 全局 `d:\常用脚本\CLAUDE.md` 是项目集合的总规
- 本 `CLAUDE.md` 是藏经阁项目的专属规
- 冲突时: 本文件优先 (项目级覆盖)
- 一致时: 严格遵守全局规则

---

## 十、常见任务速查

### 加新书

1. 创建 `library/books/<书名>/`
2. 跑阶段0-4 (见 `methodology/`)
3. 同步更新 `LIBRARY_OVERVIEW.md` 和 `QUICK_START.md`
4. 同步更新 `STATUS_REPORT.md`

### 改进 skill

1. 读 `SKILL.md` 看现状
2. 跑阶段4 压力测试找问题
3. 修 SKILL.md
4. 跑阶段3 链接更新

### 启动 OCR

```bash
# 曼昆
python scripts/ocr_pdf.py "D:\我的资料\书籍\经济学原理(第8版) 微观经济学分册（曼昆著）.pdf" "D:\我的资料\书籍\曼昆经济学.txt" --dpi 150

# 共同富裕
python scripts/ocr_pdf.py "D:\我的资料\书籍\共同富裕.pdf" "D:\我的资料\书籍\共同富裕.txt" --dpi 150
```

---

## 元数据

- **创建日期**: 2026-06-17
- **版本**: v1.0
- **作者**: 用户 + Trae AI
- **全局规则**: `d:\常用脚本\CLAUDE.md`
