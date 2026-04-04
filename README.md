# Awesome Agent Skills

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-8-green.svg)](skills)

**English** | [中文](README.zh-CN.md)

A collection of AI Agent Skills that provide professional domain capabilities for intelligent assistants like Claude Code.

## Features

- **Modular Design** - Load skills on demand
- **Bilingual Support** - Every skill is maintained as an English and Chinese pair
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

Install a specific English skill only:

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export
```

```bash
bunx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export
```

```bash
pnpm dlx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export
```

Install a specific Chinese skill only:

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn
```

```bash
bunx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn
```

```bash
pnpm dlx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn
```

Or install manually by copying the English skills only:

```bash
cp -r skills/en/* ~/.claude/skills/
```

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
5. Submit a pull request

### Test SKILL.md

Before opening a PR, validate skill files locally:

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
