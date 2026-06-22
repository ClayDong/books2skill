# Books2Skill

> A generator workflow for turning books into reusable AI skills — single-book distillation (RIA-TV++) + multi-book orchestration (intent-driven recall, conflict resolution, decision cards).

Forked from [cangjie-skill](https://github.com/kangarooking/cangjie-skill) by kangarooking.

## What It Does

**Single-book distillation** (push): Feed a book → extract atomic, agent-invocable skills via the RIA-TV++ pipeline (stages 0-4).

**Multi-book orchestration** (pull): State an intent → recall skills from multiple books → resolve conflicts → produce integrated output (stages 5-6).

## Quick Start

```bash
# Install
pip install -e .

# Distill a book
books2skill distill path/to/book.pdf

# Multi-book orchestration
books2skill orchestrate "Should I cut my losses?"

# Validate system consistency
books2skill validate

# Update global indices
books2skill index-update

# System status
books2skill status
```

## Pipeline

```
=== Single-book distillation (push) ===
Stage 0: Adler whole-book understanding  → BOOK_OVERVIEW.md
Stage 1: 5 parallel extractors            → Candidate methodology units
Stage 1.5: Triple verification            → Verified units
Stage 2: RIA++ skill construction         → SKILL.md per skill
Stage 3: Zettelkasten linking             → INDEX.md
Stage 4: Pressure testing (darwin-compatible) → test-prompts.json

=== Multi-book orchestration (pull, v2.0) ===
Stage 4.5: Global index aggregation       → library/GLOBAL_INDEX.md
Stage 5: Multi-book orchestration          → Intent classification + recall + conflict resolution
Stage 6: Decision card construction        → library/DECISION_CARDS/<scenario>.md
```

## Project Structure

```
books2skill/
├── CLAUDE.md              # Project rules (highest priority)
├── SKILL.md               # Meta-skill definition
├── methodology/            # RIA-TV++ methodology docs
├── extractors/             # 5 parallel extractors
├── templates/              # Skill & index templates
├── router/                 # Intent-driven routing
├── resolver/               # Conflict resolution
├── library/                # Multi-book orchestration output
├── books2skill/            # Python package (CLI + pipeline)
├── scripts/                # Utility scripts
└── tests/                  # Test suite
```

## License

MIT License — Copyright (c) 2026 ClayDong
