# Novel Writer

一个用于 Claude Code 的小说写作技能（Skill），提供专业的小说创作支持，涵盖构思、规划、写作到修改的全流程。

## 功能

- **新建小说** - 从零开始创作，提供结构化的大纲指导
- **章节续写** - 基于现有内容续写新章节
- **角色设计** - 创建深度角色，包括欲望、恐惧、弧线
- **世界观构建** - 构建完整的故事世界

## 支持的类型

- 科幻小说
- 奇幻小说
- 悬疑推理
- 言情/都市
- 历史/武侠
- 恐怖/惊悚

## 安装

将此技能复制到 Claude Code 的 skills 目录：

```bash
cp -r . ~/.claude/skills/novel-writer
```

或者下载 `.skill` 文件并导入。

## 使用

安装后，Claude 会自动识别以下请求：

- "帮我写一部科幻小说"
- "给这个故事续写一章"
- "帮我设计一个反派角色"
- "构建一个魔法体系"

## 结构

```
novel-writer/
├── SKILL.md                      # 核心指导文件
├── references/                   # 参考文档
│   ├── story-structure.md        # 故事结构（三幕结构、英雄之旅等）
│   ├── character-development.md  # 角色发展（原型、维度、弧线）
│   ├── worldbuilding.md          # 世界观构建
│   ├── writing-techniques.md     # 写作技巧（视角、场景、对话等）
│   └── genre-guides.md           # 类型指南
└── assets/templates/             # 模板文件
    ├── outline.md                # 小说大纲模板
    ├── character-card.md         # 角色卡模板
    ├── world-bible.md            # 世界观设定模板
    └── chapter.md                # 章节规划模板
```

## 许可证

MIT
