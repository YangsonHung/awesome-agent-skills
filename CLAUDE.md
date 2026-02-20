# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of AI Agent Skills for Claude Code. Each skill provides specialized domain capabilities (e.g., novel writing, multilingual README creation).

## Available Skills

- **novel-writer**: English novel-writing assistant (Sci-Fi, Fantasy, Mystery, Romance, Wuxia, etc.)
- **novel-writer-cn**: Chinese novel-writing assistant
- **multi-lang-readme**: English multilingual README translation skill
- **multi-lang-readme-cn**: Chinese multilingual README translation skill
- **conversation-json-to-md**: Convert chat-export JSON to one-conversation-per-file Markdown
- **conversation-json-to-md-cn**: Chinese version of chat-export JSON to Markdown conversion skill

## Commands

### Validate Skills

Before submitting a PR, run both validators:

```bash
python3 scripts/validate_skills.py
node scripts/validate-skills.js
```

For CI-level strict checks:

```bash
python3 scripts/validate_skills.py --strict
node scripts/validate-skills.js --strict
```

### Install Locally

```bash
cp -r skills/ ~/.claude/skills/
```

## Project Structure

```
skills/
├── novel-writer/
│   ├── SKILL.md           # Required: skill definition with YAML frontmatter
│   ├── references/        # Optional: reference documentation
│   └── assets/            # Optional: templates
├── novel-writer-cn/
├── multi-lang-readme/
├── multi-lang-readme-cn/
├── conversation-json-to-md/
│   ├── SKILL.md           # Required
│   └── scripts/           # Optional: executable helpers
└── conversation-json-to-md-cn/
```

## Skill Format

Every skill requires only `SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: Brief description and trigger examples
---

# Skill Name

Instructions...
```

- Folder names: `kebab-case`
- Optional files/folders (add only when needed): `README.md`, `scripts/`, `references/`, `assets/`
- Keep bilingual docs separate (English in `README.md`, Chinese in `README.zh-CN.md`)

## Contributing

Follow Conventional Commits:
- `feat(skills): add new skill`
- `docs(readme): update documentation`
- `chore: maintenance task`

Each skill should be self-contained under `skills/<skill-name>/`.
