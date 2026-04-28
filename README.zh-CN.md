# Awesome Agent Skills

[![许可证](https://img.shields.io/badge/许可证-MIT-blue.svg)](LICENSE)
[![技能数](https://img.shields.io/badge/技能-9-green.svg)](skills)

[English](README.md) | **中文**

为 Claude Code 等智能助手提供专业领域能力的 AI Agent Skills 技能包集合。

## 特性

- **模块化设计** - 按需加载技能
- **中英双语** - 每个技能都必须同时提供英文版和中文版
- **资源丰富** - 每个技能都有完整的参考资料和模板

## 可用技能

| 技能 | 语言 | 描述 | 核心功能 |
|------|------|------|----------|
| [novel-writer-cn](skills/zh-cn/novel-writer-cn/SKILL.md) | 中文 | 专为中文小说创作设计的写作助手 | 创作中文小说、续写章节、角色设计、世界观构建 |
| [multi-lang-readme-cn](skills/zh-cn/multi-lang-readme-cn/SKILL.md) | 中文 | 中文版多语言 README 翻译技能 | 创建中英/多语言 README，统一命名与链接 |
| [conversation-json-to-md-cn](skills/zh-cn/conversation-json-to-md-cn/SKILL.md) | 中文 | 中文版对话 JSON 转 Markdown 技能 | 自动识别结构、保留问答、统一回答区块、二次格式化 |
| [topic-bookmarks-reorganizer-cn](skills/zh-cn/topic-bookmarks-reorganizer-cn/SKILL.md) | 中文 | 主题书签重整技能（中文版） | 提取主题目录、链接重分类、URL 去重、导出可导入 HTML |
| [wechat-theme-extractor-cn](skills/zh-cn/wechat-theme-extractor-cn/SKILL.md) | 中文 | 从微信公众号文章中提取样式并生成主题配置 | 抽取文章 HTML、分析样式、生成主题、写入工具配置 |
| [mac-software-storage-cleanup-cn](skills/zh-cn/mac-software-storage-cleanup-cn/SKILL.md) | 中文 | 审计 macOS 软件占用并执行分级清理 | 软件清单盘点、空间统计、安全清理、回收建议 |
| [ui-layout-analyzer-cn](skills/zh-cn/ui-layout-analyzer-cn/SKILL.md) | 中文 | 分析界面截图并输出布局与功能说明 | 界面结构识别、交互分析、元素清单、布局说明 |
| [yuque-lakebook-export-cn](skills/zh-cn/yuque-lakebook-export-cn/SKILL.md) | 中文 | 将语雀 `.lakebook` 导出为适配 Obsidian 的 Markdown 目录 | 语雀导出、lakebook 转换、Obsidian 迁移、图片附件处理、裁剪图支持 |
| [git-weekly-report-cn](skills/zh-cn/git-weekly-report-cn/SKILL.md) | 中文 | 将 Git 提交日志汇总为结构化周报 | 多仓库提取、日期范围过滤、提交分类、周报生成 |

### 触发示例

**novel-writer-cn:**
- "帮我写一部中文科幻小说"
- "继续这个故事，再写一章"
- "设计一个反派角色"
- "用中文构建一个赛博朋克世界"

**multi-lang-readme-cn:**
- "帮我创建中英 README"
- "帮我创建多语言 README"
- "把 README 翻译成日语"
- "新增 README.zh-CN.md"

**conversation-json-to-md-cn:**
- "把这个聊天导出 json 转成多个 md"
- "一个会话一个 markdown 文件"
- "只保留用户和助手问答"
- "导出后再做一次二次格式化"

**topic-bookmarks-reorganizer-cn:**
- "把这个书签导出里的 AI 目录重新分门别类并导出 html"
- "只保留某个主题目录并整理链接结构"
- "去重重复书签链接并输出可导入浏览器的文件"

**wechat-theme-extractor-cn:**
- "从这个微信公众号文章链接提取主题样式"
- "帮我生成一个 markdown-wechat-converter 主题"
- "把这个微信文章风格写入 markdown-to-wechat.html"

**mac-software-storage-cleanup-cn:**
- "检查我 Mac 上安装的软件都占了多少空间"
- "列出可以优先清理的缓存和模拟器数据"
- "给我一个 macOS 软件存储清理建议"

**ui-layout-analyzer-cn:**
- "分析这个界面截图"
- "描述这个界面的布局结构"
- "这个 UI 是做什么的"
- "输出这个界面的布局和功能说明"

**yuque-lakebook-export-cn:**
- "把这个语雀 lakebook 导出成 markdown"
- "把语雀知识库迁移到 Obsidian"
- "批量转换多个 .lakebook 文件"
- "修复语雀导出后的图片、裁剪图和内部链接问题"

**git-weekly-report-cn:**
- "帮我生成一份周报"
- "总结我这周的 Git 提交"
- "汇总多个项目的工作生成周报"
- "回顾上周的代码提交记录"

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

列出本仓库可安装的技能：

```bash
npx skills add YangsonHung/awesome-agent-skills --list
```

```bash
bunx skills add YangsonHung/awesome-agent-skills --list
```

```bash
pnpm dlx skills add YangsonHung/awesome-agent-skills --list
```

只安装某一个技能：

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn
```

```bash
bunx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn
```

```bash
pnpm dlx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn
```

全局安装某一个技能：

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn -g
```

将某一个技能安装到指定 Agent：

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn -a claude-code
```

安装某一个技能并跳过确认：

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn -y
```

全局安装到指定 Agent 并跳过确认：

```bash
npx skills add YangsonHung/awesome-agent-skills --skill yuque-lakebook-export-cn -g -a claude-code -y
```

也可以只手动复制中文技能到 Claude Code 配置目录：

```bash
cp -r skills/zh-cn/* ~/.claude/skills/
```

更多命令使用方式参考：

https://github.com/vercel-labs/skills/blob/main/README.md

### 使用

安装后，技能将自动在 Claude Code 中可用。只需向 Claude 提出与技能相关的任务请求，它会自动使用相应的技能。

## 贡献指南

欢迎贡献新技能！步骤如下：

1. Fork 本仓库
2. 同时在 `skills/en/` 和 `skills/zh-cn/` 下创建成对的新目录
3. 包含以下文件：
   - `SKILL.md` - 带 frontmatter 的技能主定义文件
   - `README.md` - 技能说明（可选）
   - `scripts/` - 辅助脚本（可选）
   - `references/` - 参考资料（可选）
   - `assets/` - 模板与资源（可选）
4. 确保中英文两个技能一起提交，且内容和触发场景保持同步
5. 提交 Pull Request

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
