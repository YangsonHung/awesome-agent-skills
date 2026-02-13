---
name: multi-lang-readme
description: Create multilingual README files by translating existing README.md into target languages. Use when user asks to create bilingual README (e.g., "帮我创建中英 README", "帮我创建多语言 README") or convert README to different language. Supports English, German (de), Japanese (ja), Korean (ko), and Chinese (zh-CN).
---

# Multi-Lang README

Create multilingual README files by translating existing README.md content.

## Supported Languages

| Code  | Language |
|-------|----------|
| en    | English  |
| de    | German   |
| ja    | Japanese |
| ko    | Korean   |
| zh-CN | Chinese  |

## Workflow

### Step 1: Detect README

Find README.md in current project:
- Check root directory for `README.md`
- If multiple READMEs exist (e.g., in subdirectories), ask user which one to translate

### Step 2: Read README Content

Read the full content of README.md, including:
- Title
- Badges
- All sections (Features, Installation, Usage, Contributing, License, etc.)
- Code blocks
- Links

### Step 3: Confirm Target Language

Ask user which language to translate to. If user says "create bilingual README" without specifying, assume:
- If current README is in Chinese → translate to English
- If current README is in English → translate to Chinese

### Step 4: Translate with AI

Translate content using Claude's built-in translation capability:
- Preserve markdown formatting
- Keep code blocks unchanged
- Translate section titles to target language
- Keep internal links (relative paths) as-is
- For external links, use target language anchor text if appropriate

### Step 5: Create Translated README

Create new file with locale suffix:
- English: README.md (or keep existing)
- German: README.de.md
- Japanese: README.ja.md
- Korean: README.ko.md
- Chinese: README.zh-CN.md

### Step 6: Add Language Switcher

Update original README to include language switcher at the top:

```markdown
**English** | [中文](README.zh-CN.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md)
```

Add below the title or badges, before the main content.

### Step 7: Update Translated README

Add reciprocal link in the translated README:

```markdown
**[Original](README.md)** | [中文](README.zh-CN.md)
```

## Language Code Reference

```
en    → no suffix (README.md)
de    → README.de.md
ja    → README.ja.md
ko    → README.ko.md
zh-CN → README.zh-CN.md
```

## Common Triggers

- "帮我创建中英 README"
- "帮我创建多语言 README"
- "create bilingual README"
- "create English and Chinese README"
- "translate README to Japanese"
- "add German version of README"
