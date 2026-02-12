# Awesome Agent Skills

[![许可证](https://img.shields.io/badge/许可证-MIT-blue.svg)](LICENSE)
[![技能数](https://img.shields.io/badge/技能-2-green.svg)](skills)

[English](README.md) | **中文**

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
