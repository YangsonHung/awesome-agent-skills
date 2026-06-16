# Awesome Agent Skills

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-13-green.svg)](skills)

**English** | [中文](README.zh-CN.md)

**Repository**: https://github.com/YangsonHung/awesome-agent-skills

A collection of AI Agent Skills that provide professional domain capabilities for intelligent assistants like Claude Code.

## Features

- **Modular Design** - Load skills on demand
- **Bilingual Support** - Every skill is maintained as an English and Chinese pair
- **Language Guardrails** - English `SKILL.md` files stay English-only, except native language names in `multi-lang-readme`
- **Rich Resources** - Complete references and templates for each skill

## Available Skills

| Skill | Language | Description | Capabilities |
|-------|----------|-------------|--------------|
| [novel-writer](skills/en/novel-writer/SKILL.md) | English | Professional novel writing assistant for the entire creative process | Create novels, Continue chapters, Character design, Worldbuilding |
| [multi-lang-readme](skills/en/multi-lang-readme/SKILL.md) | English | Create multilingual README translations | Translate README to English, German, Japanese, Korean, Chinese |
| [conversation-json-to-md](skills/en/conversation-json-to-md/SKILL.md) | English | Convert chat-export JSON into one-conversation-per-file Markdown | Auto-detect formats, Q/A extraction, heading normalization, second-pass formatting |
| [topic-bookmarks-reorganizer](skills/en/topic-bookmarks-reorganizer/SKILL.md) | English | Reorganize one topic folder from bookmarks export into clean importable HTML | Topic extraction, link regrouping, URL dedupe, browser-importable output |
| [wechat-theme-extractor](skills/en/wechat-theme-extractor/SKILL.md) | English | Extract theme styles from WeChat articles and update converter config | WeChat HTML extraction, style analysis, theme generation, config injection |
| [mac-software-storage-cleanup](skills/en/mac-software-storage-cleanup/SKILL.md) | English | Audit macOS software storage usage and run prioritized cleanup | Installed software inventory, storage audit, safe cleanup, reclaim recommendations |
| [ui-layout-analyzer](skills/en/ui-layout-analyzer/SKILL.md) | English | Analyze UI screenshots and describe layout plus functional structure | UI structure recognition, interaction analysis, element inventory, layout explanation |
| [yuque-lakebook-export](skills/en/yuque-lakebook-export/SKILL.md) | English | Export Yuque `.lakebook` files into Markdown folders for Obsidian | Yuque export, lakebook conversion, Obsidian migration, image/assets handling, cropped image support |
| [git-weekly-report](skills/en/git-weekly-report/SKILL.md) | English | Summarize git commit logs into structured weekly reports | Multi-repo extraction, date range filtering, commit categorization, weekly report generation |
| [git-push-secondary-merge-primary](skills/en/git-push-secondary-merge-primary/SKILL.md) | English | Commit & push secondary branch, then merge into the primary branch | Two-branch sync, branch detection, conventional commit, merge commit preservation, safe push |
| [git-pushing-fast](skills/en/git-pushing-fast/SKILL.md) | English | Fast single-branch commit and push workflow with segmented commit body | Status inspection, staging, Conventional Commits, segmented body, safe push |
| [frontend-quality-guardrails](skills/en/frontend-quality-guardrails/SKILL.md) | English | Build and review frontend UI with text, layout, visual, and browser QA guardrails | Long text handling, overflow fixes, visual standards, code review, responsive verification |
| [feature-doc-splitter](skills/en/feature-doc-splitter/SKILL.md) | English | Split rough feature notes into overview, frontend, and backend implementation docs | Codebase inspection, frontend/backend separation, Mermaid flows, API contracts, optional design placeholders |

### Trigger Examples

**novel-writer:**
- "help me write a sci-fi novel"
- "write the next chapter"
- "design a villain character"
- "build a cyberpunk world"

**multi-lang-readme:**
- "create bilingual README"
- "translate README to Japanese"
- "add German README version"

**conversation-json-to-md:**
- "convert this chat-export json to markdown files"
- "one conversation per md file"
- "keep only user and assistant Q/A"
- "normalize output headings after export"

**topic-bookmarks-reorganizer:**
- "reorganize this bookmarks export and keep only the AI folder"
- "analyze links under one topic folder and regroup them"
- "dedupe repeated bookmark URLs and export importable html"

**wechat-theme-extractor:**
- "extract a theme from this WeChat article URL"
- "generate a markdown-wechat-converter theme from this article"
- "write the extracted style into markdown-to-wechat.html"

**mac-software-storage-cleanup:**
- "audit installed software sizes on my Mac"
- "show safe cache and simulator cleanup candidates"
- "give me a macOS storage cleanup plan"

**ui-layout-analyzer:**
- "analyze this UI screenshot"
- "describe this interface layout"
- "what does this UI do"
- "output the layout and function description of this UI"

**yuque-lakebook-export:**
- "export this Yuque .lakebook to markdown"
- "convert my lakebook into an Obsidian folder"
- "batch convert multiple .lakebook files"
- "fix missing images and broken internal links from Yuque export"

**git-weekly-report:**
- "generate a weekly report from my git commits"
- "summarize what I did this week across my projects"
- "create a weekly report from recent git activity"
- "review commits by project from last week"

**git-push-secondary-merge-primary:**
- "commit and push dev, then merge it into main and push"
- "push the work branch then merge to master"
- "merge develop into main, push both branches, and switch back to develop"
- "finish the work branch and sync it to the primary branch"

**git-pushing-fast:**
- "commit and push these changes"
- "push this work to the current branch"
- "save this work to remote"
- "commit with a segmented body and push"

**frontend-quality-guardrails:**
- "review this React component for long text and layout overflow"
- "fix the mobile overflow and alignment issues in this dashboard"
- "polish this form and verify responsive UI states"
- "check this table for truncation, wrapping, and browser layout pitfalls"

**feature-doc-splitter:**
- "split this rough feature doc into overview, frontend, and backend docs"
- "turn this initial product note into implementation documents"
- "read the codebase and write frontend/backend build docs"
- "add Mermaid flows and ask whether to reserve design placeholders"

## Quick Start

### Installation

Install with one of the following commands:

```bash
npx skills add YangsonHung/awesome-agent-skills
```

```bash
bunx skills add YangsonHung/awesome-agent-skills
```

```bash
pnpm dlx skills add YangsonHung/awesome-agent-skills
```

List available skills in this repository:

```bash
npx skills add YangsonHung/awesome-agent-skills --list
```

```bash
bunx skills add YangsonHung/awesome-agent-skills --list
```

```bash
pnpm dlx skills add YangsonHung/awesome-agent-skills --list
```

Install a specific skill:

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export
```

```bash
bunx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export
```

```bash
pnpm dlx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export
```

Install a specific skill globally:

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export -g
```

Install a specific skill to a specific agent:

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export -a claude-code
```

Install a specific skill without confirmation prompts:

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export -y
```

Install a specific skill globally for a specific agent without prompts:

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export -g -a claude-code -y
```

Or install manually by copying the English skills only:

```bash
cp -r skills/en/* ~/.claude/skills/
```

More command usage examples:

https://github.com/vercel-labs/skills/blob/main/README.md

### Usage

Once installed, the skills will be automatically available in Claude Code. Simply ask Claude to perform a task related to a skill, and it will use the appropriate skill automatically.

## Contributing

Contributions are welcome! To add a new skill:

1. Fork this repository
2. Create both paired directories under `skills/en/` and `skills/zh-cn/`
3. Include the following files:
   - `SKILL.md` - Main skill definition with frontmatter
   - `README.md` - Optional skill-level notes
   - `scripts/` - Optional helper scripts
   - `references/` - Optional reference materials
   - `assets/` - Optional templates and resources
4. Ensure both language variants are added together and kept in sync
5. Keep English `SKILL.md` files free of Chinese/Han characters; add Chinese examples and localized wording only to the paired `skills/zh-cn/` skill. The exception is `skills/en/multi-lang-readme/SKILL.md`, where language-switch examples may show native language names.
6. Submit a pull request

### Test SKILL.md

Before opening a PR, validate skill files locally. The validators check skill structure, bilingual counterparts, and the English `SKILL.md` language rule:

```bash
python3 scripts/validate_skills.py
node scripts/validate-skills.js
```

For CI-level checks (fail on warnings), run strict mode:

```bash
python3 scripts/validate_skills.py --strict
node scripts/validate-skills.js --strict
```

Both commands must exit with code `0`.

### Git Hooks

Enable the repository pre-commit hook locally:

```bash
git config core.hooksPath .githooks
```

The hook runs strict skill validators, including the English skill language check, before each commit.

### Skill Format

```markdown
---
name: skill-name
description: Brief description of the skill and trigger examples
---

# Skill Name

Detailed skill instructions...
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
