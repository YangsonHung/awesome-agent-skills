# Awesome Agent Skills

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-8-green.svg)](skills)

**English** | [中文](README.zh-CN.md)

A collection of AI Agent Skills that provide professional domain capabilities for intelligent assistants like Claude Code.

## Features

- **Modular Design** - Load skills on demand
- **Bilingual Support** - Available in both English and Chinese
- **Rich Resources** - Complete references and templates for each skill

## Available Skills

| Skill | Language | Description | Capabilities |
|-------|----------|-------------|--------------|
| [novel-writer](skills/en/novel-writer/SKILL.md) | English | Professional novel writing assistant for the entire creative process | Create novels, Continue chapters, Character design, Worldbuilding |
| [novel-writer-cn](skills/zh-cn/novel-writer-cn/SKILL.md) | 中文 | Chinese novel writing assistant | Create Chinese novels, Continue chapters, Character design, Worldbuilding |
| [multi-lang-readme](skills/en/multi-lang-readme/SKILL.md) | English | Create multilingual README translations | Translate README to English, German, Japanese, Korean, Chinese |
| [multi-lang-readme-cn](skills/zh-cn/multi-lang-readme-cn/SKILL.md) | 中文 | 中文版 README 多语言翻译技能 | 创建中英/多语言 README，保持 Markdown 结构与链接一致 |
| [conversation-json-to-md](skills/en/conversation-json-to-md/SKILL.md) | English | Convert chat-export JSON into one-conversation-per-file Markdown | Auto-detect formats, Q/A extraction, heading normalization, second-pass formatting |
| [conversation-json-to-md-cn](skills/zh-cn/conversation-json-to-md-cn/SKILL.md) | 中文 | 将聊天导出 JSON 转为一会话一 Markdown 文件 | 自动识别结构、问答提取、标题规范化、二次格式化 |
| [topic-bookmarks-reorganizer](skills/en/topic-bookmarks-reorganizer/SKILL.md) | English | Reorganize one topic folder from bookmarks export into clean importable HTML | Topic extraction, link regrouping, URL dedupe, browser-importable output |
| [topic-bookmarks-reorganizer-cn](skills/zh-cn/topic-bookmarks-reorganizer-cn/SKILL.md) | 中文 | 将书签导出中的主题目录重整为可导入 HTML | 主题提取、重分类、URL 去重、输出可导入文件 |

### Trigger Examples

**novel-writer:**
- "help me write a sci-fi novel"
- "write the next chapter"
- "design a villain character"
- "build a cyberpunk world"

**novel-writer-cn:**
- "help me write a Chinese sci-fi novel"
- "continue this story with one more chapter"
- "design an antagonist character"
- "build a cyberpunk world in Chinese"

**multi-lang-readme:**
- "create bilingual README"
- "translate README to Japanese"
- "add German README version"

**multi-lang-readme-cn:**
- "帮我创建中英 README"
- "帮我创建多语言 README"
- "把 README 翻译成日语"
- "新增 README.zh-CN.md"

**conversation-json-to-md:**
- "convert this chat-export json to markdown files"
- "one conversation per md file"
- "keep only user and assistant Q/A"
- "normalize output headings after export"

**conversation-json-to-md-cn:**
- "把这个聊天导出 json 转成多个 md"
- "一个会话一个 markdown 文件"
- "只保留用户和助手问答"
- "导出后再做一次二次格式化"

**topic-bookmarks-reorganizer:**
- "reorganize this bookmarks export and keep only the AI folder"
- "analyze links under one topic folder and regroup them"
- "dedupe repeated bookmark URLs and export importable html"

**topic-bookmarks-reorganizer-cn:**
- "把这个书签导出里的 AI 目录重新分门别类并导出 html"
- "只保留某个主题目录并整理链接结构"
- "去重重复书签链接并输出可导入浏览器的文件"

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

Or install manually by copying the `skills` directory:

```bash
cp -r skills/ ~/.claude/skills/
```

### Usage

Once installed, the skills will be automatically available in Claude Code. Simply ask Claude to perform a task related to a skill, and it will use the appropriate skill automatically.

## Contributing

Contributions are welcome! To add a new skill:

1. Fork this repository
2. Create a new directory under `skills/en/` or `skills/zh-cn/`
3. Include the following files:
   - `SKILL.md` - Main skill definition with frontmatter
   - `README.md` - Optional skill-level notes
   - `scripts/` - Optional helper scripts
   - `references/` - Optional reference materials
   - `assets/` - Optional templates and resources
4. Submit a pull request

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
