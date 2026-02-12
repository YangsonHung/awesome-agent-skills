# Awesome Agent Skills

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-2-green.svg)](skills)

**English** | [中文](README.zh-CN.md)

A collection of AI Agent Skills that provide professional domain capabilities for intelligent assistants like Claude Code.

## Features

- **Modular Design** - Load skills on demand
- **Bilingual Support** - Available in both English and Chinese
- **Rich Resources** - Complete references and templates for each skill

## Available Skills

### novel-writer (English)

Professional novel writing assistant supporting the entire creative process.

**Supported Genres:** Sci-Fi, Fantasy, Mystery, Romance, Wuxia, and more

**Capabilities:**
- Create novels from scratch
- Continue existing chapters
- Character design and development
- Worldbuilding

**Trigger Examples:**
- "help me write a sci-fi novel"
- "write the next chapter"
- "design a villain character"
- "build a cyberpunk world"

[View Details](skills/novel-writer/README.md)

### novel-writer-cn (中文)

A writing assistant designed for Chinese novel creation.

**Supported Genres:** Sci-Fi, Fantasy, Mystery, Romance, Wuxia, and more

**Capabilities:**
- Create Chinese novels from scratch
- Continue existing chapters
- Character design and development
- Worldbuilding

**Trigger Examples:**
- "help me write a Chinese sci-fi novel"
- "continue this story with one more chapter"
- "design an antagonist character"
- "build a cyberpunk world in Chinese"

[View Details](skills/novel-writer-cn/README.md)

## Quick Start

### Installation

Copy the `skills` directory to your Claude Code configuration directory:

```bash
cp -r skills/ ~/.claude/skills/
```

Or clone this repository:

```bash
git clone https://github.com/yangson/awesome-agent-skills.git
```

### Usage

Once installed, the skills will be automatically available in Claude Code. Simply ask Claude to perform a task related to a skill, and it will use the appropriate skill automatically.

## Project Structure

```
awesome-agent-skills/
├── skills/
│   ├── novel-writer/           # English version
│   │   ├── SKILL.md            # Skill definition
│   │   ├── README.md           # Documentation
│   │   ├── references/         # Reference materials
│   │   │   ├── story-structure.md
│   │   │   ├── character-development.md
│   │   │   ├── worldbuilding.md
│   │   │   ├── writing-techniques.md
│   │   │   └── genre-guides.md
│   │   └── assets/
│   │       └── templates/      # Writing templates
│   │           ├── outline.md
│   │           ├── character-card.md
│   │           ├── world-bible.md
│   │           └── chapter.md
│   └── novel-writer-cn/        # Chinese version
│       └── ... (same structure)
├── LICENSE
└── README.md
```

## Contributing

Contributions are welcome! To add a new skill:

1. Fork this repository
2. Create a new directory under `skills/`
3. Include the following files:
   - `SKILL.md` - Main skill definition with frontmatter
   - `README.md` - Documentation
   - `references/` - Reference materials (optional)
   - `assets/` - Templates and resources (optional)
4. Submit a pull request

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
