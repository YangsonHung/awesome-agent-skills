# Awesome Agent Skills

[![许可证](https://img.shields.io/badge/许可证-MIT-blue.svg)](LICENSE)
[![技能数](https://img.shields.io/badge/技能-6-green.svg)](skills)

[English](README.md) | **中文**

为 Claude Code 等智能助手提供专业领域能力的 AI Agent Skills 技能包集合。

## 特性

- **模块化设计** - 按需加载技能
- **中英双语** - 同时提供中文和英文版本
- **资源丰富** - 每个技能都有完整的参考资料和模板

## 可用技能

| 技能 | 语言 | 描述 | 核心功能 |
|------|------|------|----------|
| [novel-writer](skills/en/novel-writer/SKILL.md) | English | 专业小说写作助手，支持完整创作流程 | 创作小说、续写章节、角色设计、世界观构建 |
| [novel-writer-cn](skills/zh-cn/novel-writer-cn/SKILL.md) | 中文 | 专为中文小说创作设计的写作助手 | 创作中文小说、续写章节、角色设计、世界观构建 |
| [multi-lang-readme](skills/en/multi-lang-readme/SKILL.md) | English | 英文版多语言 README 翻译技能 | 将 README 翻译成多语言并保持结构 |
| [multi-lang-readme-cn](skills/zh-cn/multi-lang-readme-cn/SKILL.md) | 中文 | 中文版多语言 README 翻译技能 | 创建中英/多语言 README，统一命名与链接 |
| [conversation-json-to-md](skills/en/conversation-json-to-md/SKILL.md) | English | 将聊天导出 JSON 转换为一会话一文件的 Markdown | 自动识别格式、问答提取、标题规范化、导出后二次格式化 |
| [conversation-json-to-md-cn](skills/zh-cn/conversation-json-to-md-cn/SKILL.md) | 中文 | 中文版对话 JSON 转 Markdown 技能 | 自动识别结构、保留问答、统一回答区块、二次格式化 |

### 触发示例

**novel-writer:**
- "帮我写一部科幻小说"
- "给这个故事续写一章"
- "设计一个反派角色"
- "构建一个赛博朋克世界"

**novel-writer-cn:**
- "帮我写一部中文科幻小说"
- "继续这个故事，再写一章"
- "设计一个反派角色"
- "用中文构建一个赛博朋克世界"

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

## 快速开始

### 安装

使用以下任一命令安装：

```bash
npx skills add YangsonHung/awesome-agent-skills
```

```bash
bunx skills add YangsonHung/awesome-agent-skills
```

```bash
pnpm dlx skills add YangsonHung/awesome-agent-skills
```

也可以手动复制 `skills` 目录到 Claude Code 配置目录：

```bash
cp -r skills/ ~/.claude/skills/
```

### 使用

安装后，技能将自动在 Claude Code 中可用。只需向 Claude 提出与技能相关的任务请求，它会自动使用相应的技能。

## 贡献指南

欢迎贡献新技能！步骤如下：

1. Fork 本仓库
2. 在 `skills/en/` 或 `skills/zh-cn/` 下创建新目录
3. 包含以下文件：
   - `SKILL.md` - 带 frontmatter 的技能主定义文件
   - `README.md` - 技能说明（可选）
   - `scripts/` - 辅助脚本（可选）
   - `references/` - 参考资料（可选）
   - `assets/` - 模板与资源（可选）
4. 提交 Pull Request

### 测试 SKILL.md

提交 PR 前，请先在本地校验技能文件：

```bash
python3 scripts/validate_skills.py
node scripts/validate-skills.js
```

如需按 CI 标准（warning 也失败）检查，请运行严格模式：

```bash
python3 scripts/validate_skills.py --strict
node scripts/validate-skills.js --strict
```

以上命令都应返回退出码 `0`。

### Skill Format

```markdown
---
name: skill-name
description: Brief description of the skill and trigger examples
---

# Skill Name

Detailed skill instructions...
```

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
