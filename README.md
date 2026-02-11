# Awesome Agent Skills

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-2-green.svg)](skills)

**English** | [中文](#中文)

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

专为中文小说创作设计的写作助手。

**支持类型：** 科幻、奇幻、悬疑、言情、武侠等

**功能：**
- 从零开始创作小说
- 续写现有章节
- 角色设计与塑造
- 世界观构建

**触发示例：**
- "帮我写一部科幻小说"
- "给这个故事续写一章"
- "设计一个反派角色"
- "构建一个赛博朋克世界"

[查看详情](skills/novel-writer-cn/README.md)

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

---

# 中文

[![许可证](https://img.shields.io/badge/许可证-MIT-blue.svg)](LICENSE)
[![技能数](https://img.shields.io/badge/技能-2-green.svg)](skills)

为 Claude Code 等智能助手提供专业领域能力的 AI Agent Skills 技能包集合。

## 特性

- **模块化设计** - 按需加载技能
- **中英双语** - 同时提供中文和英文版本
- **资源丰富** - 每个技能都有完整的参考资料和模板

## 包含的技能

### novel-writer-cn (中文版)

专为中文小说创作设计的专业写作助手。

**支持类型：** 科幻、奇幻、悬疑、言情、武侠等

**核心功能：**
- 从零开始创作小说
- 续写现有章节
- 角色设计与塑造
- 世界观构建

[查看详情](skills/novel-writer-cn/README.md)

### novel-writer (English)

Professional novel writing assistant.

[View Details](skills/novel-writer/README.md)

## 快速开始

### 安装

将 `skills` 目录复制到 Claude Code 配置目录：

```bash
cp -r skills/ ~/.claude/skills/
```

或克隆本仓库：

```bash
git clone https://github.com/yangson/awesome-agent-skills.git
```

### 使用

安装后，技能将自动在 Claude Code 中可用。只需向 Claude 提出与技能相关的任务请求，它会自动使用相应的技能。

## 目录结构

```
awesome-agent-skills/
├── skills/
│   ├── novel-writer/           # 英文版
│   └── novel-writer-cn/        # 中文版
├── LICENSE
└── README.md
```

## 贡献指南

欢迎贡献新技能！步骤如下：

1. Fork 本仓库
2. 在 `skills/` 下创建新目录
3. 包含必要文件：`SKILL.md`、`README.md`
4. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
