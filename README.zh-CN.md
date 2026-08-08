# Awesome Agent Skills

[![许可证](https://img.shields.io/badge/许可证-MIT-blue.svg)](LICENSE)
[![技能数](https://img.shields.io/badge/技能-17-green.svg)](skills)

[English](README.md) | **中文**

**项目地址**：https://github.com/YangsonHung/awesome-agent-skills

为 Claude Code 等智能助手提供专业领域能力的 AI Agent Skills 技能包集合。

## 特性

- **模块化设计** - 按需加载技能
- **中英双语** - 每个技能都必须同时提供英文版和中文版
- **语言守卫** - 英文版 `SKILL.md` 不允许出现中文或其他汉字字符，`multi-lang-readme` 的语言名称示例除外
- **资源丰富** - 每个技能都有完整的参考资料和模板

## 可用技能

| 技能 | 语言 | 描述 | 核心功能 |
|------|------|------|----------|
| [novel-writer-cn](skills/zh-cn/novel-writer-cn/SKILL.md) | 中文 | 专为中文小说创作设计的写作助手 | 创作中文小说、续写章节、角色设计、世界观构建 |
| [multi-lang-readme-cn](skills/zh-cn/multi-lang-readme-cn/SKILL.md) | 中文 | 中文版多语言 README 翻译技能 | 创建中英/多语言 README，统一命名与链接 |
| [conversation-json-to-md-cn](skills/zh-cn/conversation-json-to-md-cn/SKILL.md) | 中文 | 中文版对话 JSON 转 Markdown 技能 | 自动识别结构、保留问答、统一回答区块、二次格式化 |
| [topic-bookmarks-reorganizer-cn](skills/zh-cn/topic-bookmarks-reorganizer-cn/SKILL.md) | 中文 | 主题书签重整技能（中文版） | 提取主题目录、链接重分类、URL 去重、导出可导入 HTML |
| [wechat-theme-extractor-cn](skills/zh-cn/wechat-theme-extractor-cn/SKILL.md) | 中文 | 从微信公众号文章中提取样式并生成主题配置 | 抽取文章 HTML、分析样式、生成主题、写入工具配置 |
| [weixin-article-to-obsidian-cn](skills/zh-cn/weixin-article-to-obsidian-cn/SKILL.md) | 中文 | 将微信公众号文章保存为 Obsidian Markdown 并本地化图片 | opencli 下载、HTML 兜底解析、图片本地化、Obsidian 资源双链 |
| [mac-software-storage-cleanup-cn](skills/zh-cn/mac-software-storage-cleanup-cn/SKILL.md) | 中文 | 审计 macOS 软件占用并执行分级清理 | 软件清单盘点、空间统计、安全清理、回收建议 |
| [ui-layout-analyzer-cn](skills/zh-cn/ui-layout-analyzer-cn/SKILL.md) | 中文 | 分析界面截图并输出布局与功能说明 | 界面结构识别、交互分析、元素清单、布局说明 |
| [yuque-lakebook-export-cn](skills/zh-cn/yuque-lakebook-export-cn/SKILL.md) | 中文 | 将语雀 `.lakebook` 导出为适配 Obsidian 的 Markdown 目录 | 语雀导出、lakebook 转换、Obsidian 迁移、图片附件处理、裁剪图支持 |
| [tweetclaw-twitter-automation-cn](skills/zh-cn/tweetclaw-twitter-automation-cn/SKILL.md) | 中文 | 使用 TweetClaw 安全执行用户批准的 X/Twitter 自动化 | 推文抓取、回复搜索、粉丝导出、用户查询、媒体、私信、监控、Webhook、抽奖、批准后的发帖/回复 |
| [git-weekly-report-cn](skills/zh-cn/git-weekly-report-cn/SKILL.md) | 中文 | 将 Git 提交日志汇总为结构化周报 | 多仓库提取、日期范围过滤、提交分类、周报生成 |
| [git-push-secondary-merge-primary-cn](skills/zh-cn/git-push-secondary-merge-primary-cn/SKILL.md) | 中文 | 提交并推送副分支，再合并到主分支并推送，最后切回副分支 | 双分支同步、分支自动识别、Conventional Commits、保留合并提交、安全推送 |
| [git-pushing-fast-cn](skills/zh-cn/git-pushing-fast-cn/SKILL.md) | 中文 | 快速执行单分支提交推送，并为非简单改动生成分段提交正文 | 状态检查、暂存改动、Conventional Commits、分段正文、安全推送 |
| [git-commit-only-cn](skills/zh-cn/git-commit-only-cn/SKILL.md) | 中文 | 只创建一个本地 Conventional Commit，不推送 | 状态检查、暂存改动、Conventional Commits、分段正文、不推送 |
| [frontend-quality-guardrails-cn](skills/zh-cn/frontend-quality-guardrails-cn/SKILL.md) | 中文 | 前端 UI 文本、布局、视觉和浏览器验证质量守门技能 | 超长文本处理、溢出修复、视觉规范、代码审查、响应式验证 |
| [react-component-hook-guidelines-cn](skills/zh-cn/react-component-hook-guidelines-cn/SKILL.md) | 中文 | 按职责边界审视并拆分 React 组件与 Hook | 职责边界、props 设计、状态流转、分支控制、页面编排 |
| [logo-design-board-cn](skills/zh-cn/logo-design-board-cn/SKILL.md) | 中文 | 用设计师人格蒸馏委员会设计和评审 Logo 概念 | 品牌简报、设计师镜片、概念方向、生图提示词、Logo 质量评分 |
| [linkedin-cn](skills/zh-cn/linkedin-cn/SKILL.md) | 中文 | 通过 linkedin 命令行工具自动化操作 LinkedIn | 主页/公司获取与搜索、私信、连接请求、发布动态、点赞评论、数据提取 |
| [feature-doc-splitter-cn](skills/zh-cn/feature-doc-splitter-cn/SKILL.md) | 中文 | 将初版功能需求拆成总览、前端和后端落地文档 | 代码梳理、前后端职责拆分、Mermaid 流程图、接口契约、可选设计稿占位 |
| [routerbase-api-integration-cn](skills/zh-cn/routerbase-api-integration-cn/SKILL.md) | 中文 | 将应用接入 [routerbase](https://routerbase.com/) OpenAI 兼容网关 | SDK 迁移、base URL 配置、流式输出、tool calling、安全 API Key |
| [routerbase-model-routing-cn](skills/zh-cn/routerbase-model-routing-cn/SKILL.md) | 中文 | 规划 [routerbase](https://routerbase.com/) 模型路由、fallback、成本和延迟策略 | 模型选择、fallback 链路、上线验证、路由假设 |
| [routerbase-media-generation-cn](skills/zh-cn/routerbase-media-generation-cn/SKILL.md) | 中文 | 构建 [routerbase](https://routerbase.com/) 图片、音频和视频生成流程 | 端点选择、重试轮询、资产管理、安全检查 |
| [x-twitter-scraper-cn](skills/zh-cn/x-twitter-scraper-cn/SKILL.md) | 中文 | 使用 Xquik 规划 X/Twitter 数据工作流 | 推文搜索、账号时间线、粉丝导出、媒体下载、监控、Webhook、MCP |
| [ax-extract-workflow-cn](skills/zh-cn/ax-extract-workflow-cn/SKILL.md) | 中文 | 根据本机 ax 会话证据复盘已交付成果 | 会话查找、工具与技能追踪、决策复原、可复用流程摘要 |
| [tree-ring-memory-cn](skills/zh-cn/tree-ring-memory-cn/SKILL.md) | 中文 | 使用 Tree Ring Memory 管理本地优先的 AI Agent 记忆生命周期 | 召回、证据化经验、隐私安全记录、审计、脱敏、遗忘 |

### 触发示例

**linkedin-cn:**
- "给这个 LinkedIn 主页发送连接请求"
- "在 LinkedIn 上给这个人发私信"
- "在 LinkedIn 上搜索市场经理并提取主页信息"
- "把这条动态发布到我的 LinkedIn"
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

**weixin-article-to-obsidian-cn:**
- "把这个微信公众号文章抓成 Obsidian Markdown"
- "下载这篇 mp.weixin.qq.com 文章的正文和图片"
- "把这篇微信文章放到知识库合适目录，并本地化图片"

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

**tweetclaw-twitter-automation-cn:**
- "用 TweetClaw 抓取推文"
- "搜索这条推文的回复"
- "通过 OpenClaw 发布这条已确认的推文"
- "导出粉丝并总结结果"

**git-weekly-report-cn:**
- "帮我生成一份周报"
- "总结我这周的 Git 提交"
- "汇总多个项目的工作生成周报"
- "回顾上周的代码提交记录"

**git-push-secondary-merge-primary-cn:**
- "提交推送副分支，然后合并到主分支并推送"
- "提交推送 dev，然后合并到 main"
- "把 develop 合到 master 上推送，最后切回 develop"
- "把工作分支推上去再合到主分支并切回来"

**git-pushing-fast-cn:**
- "提交推送"
- "把当前改动提交并推送"
- "推上去，提交正文按模块分段说明"
- "commit and push these changes"

**git-commit-only-cn:**
- "只提交不推送"
- "提交当前改动"
- "创建一个本地提交"
- "commit current changes without pushing"

**frontend-quality-guardrails-cn:**
- "检查这个 React 组件的超长文本和布局溢出问题"
- "修复这个仪表盘在移动端的溢出和对齐问题"
- "打磨这个表单并验证响应式状态"
- "检查这个表格的截断、换行和浏览器布局踩坑点"

**react-component-hook-guidelines-cn:**
- "评审这个 React 组件该怎么拆"
- "把这个 God Component 拆成 Hook 和展示组件"
- "重构这个页面，减少 props 和状态耦合"
- "检查这个 Hook 是否该把逻辑移到 utils"

**logo-design-board-cn:**
- "为这个 AI 笔记产品设计一个 Logo"
- "用设计师委员会方法生成品牌标识方向"
- "评审这几个 Logo 概念并选出最强方向"
- "把这份品牌简报转成 Logo 提示词和矢量重绘说明"

**feature-doc-splitter-cn:**
- "把这份初版需求拆成总览、前端、后端文档"
- "结合代码把功能需求整理成可开发文档"
- "分别写前端和后端实现说明"
- "补充 Mermaid 流程图，并询问是否预留设计稿占位"

**routerbase-api-integration-cn:**
- "把这段 OpenAI SDK 调用迁移到 RouterBase"
- "把 RouterBase 配成 OpenAI 兼容 endpoint"
- "写一个安全的 RouterBase API 接入示例"

**routerbase-model-routing-cn:**
- "为这个工作负载选择 RouterBase 模型"
- "设计 RouterBase fallback 链路"
- "写一套兼顾成本的模型路由规则"

**routerbase-media-generation-cn:**
- "构建 RouterBase 图片生成流程"
- "处理 RouterBase 视频生成轮询"
- "给生成媒体资产加安全检查"
**x-twitter-scraper-cn:**
- "搜索包含这个关键词的 X 推文"
- "导出这个账号的粉丝"
- "设置一个带 Webhook 的 X 监控"
- "帮我选择合适的 Xquik 接口"
**ax-extract-workflow-cn:**
- "复盘这个功能是怎么交付的"
- "从这个提交提取工作流"
- "这个 PR 当时为什么能跑通"
- "把昨天 demo 背后的流程整理出来"
**tree-ring-memory-cn:**
- "修改这个仓库前先召回之前的决策"
- "把这条经验连同证据一起记住"
- "发布前审计一下项目记忆"
- "脱敏或遗忘这个任务里的过时记忆"

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
5. 英文版 `skills/en/**/SKILL.md` 不得包含中文或其他汉字字符；中文示例、触发语和本地化表达只写入对应 `skills/zh-cn/**/SKILL.md`。例外是 `skills/en/multi-lang-readme/SKILL.md`，其中的语言切换示例可以展示语言原生名称。
6. 保持 frontmatter `description` 简洁，因为它是模型选择技能的路由入口：
   - 英文版 description 必须以 `Use when ...` 开头
   - 中文版 description 使用自然中文触发句式，例如 `当用户……时使用。`，不要用英文 `Use when` 开头
   - description 不要指定某个智能体，例如不要写 `Use when Codex is asked ...`，只描述用户需求或任务场景
   - 较长的目标、能力范围、产出和边界说明放到 `## Overview`
7. 提交 Pull Request

### 测试 SKILL.md

提交 PR 前，请先在本地校验技能文件。校验会检查技能结构、中英文配对，以及英文版 `SKILL.md` 的语言规则：

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

### Git Hooks

在本地启用仓库 pre-commit hook：

```bash
git config core.hooksPath .githooks
```

该 hook 会在每次提交前运行严格模式技能校验脚本，包括英文版技能语言检查。

### Skill Format

```markdown
---
name: skill-name
description: 当用户需要执行某个简洁明确的任务场景时使用。
---

# Skill Name

## Overview

说明技能目标、能力范围、产出和边界。

## 何时使用

当用户提出以下需求时使用本技能：
- 具体触发示例
- 另一个支持的任务
```

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。
