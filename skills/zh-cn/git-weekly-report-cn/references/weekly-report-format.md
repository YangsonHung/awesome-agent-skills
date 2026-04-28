# 周报分类指南

## Conventional Commit 映射

将提交前缀映射到周报分类：

| 前缀 | 分类 |
|------|------|
| `feat:` | 新增功能 |
| `fix:` | 问题修复 |
| `refactor:` | 代码重构 |
| `docs:` | 文档更新 |
| `chore:` | 日常维护 |
| `test:` | 测试相关 |
| `perf:` | 性能优化 |
| `style:` | 代码风格 |
| `ci:` | CI/CD |
| `build:` | 构建系统 |

## 非 Conventional Commit

当提交缺少 conventional 前缀时，从关键词推断分类：

- **新增功能**: add, implement, create, introduce, support, enable, 新增, 实现
- **问题修复**: fix, resolve, repair, patch, workaround, hotfix, 修复, 解决
- **代码重构**: refactor, restructure, reorganize, simplify, clean up, migrate, 重构, 迁移
- **文档更新**: docs, readme, guide, comment, document, 文档
- **日常维护**: update, upgrade, bump, deps, dependency, config, chore, 更新, 升级
- **测试相关**: test, spec, coverage, verify, assert, 测试
- **性能优化**: optimize, speed, fast, slow, latency, memory, 优化

## 分组策略

1. 先按项目（仓库名）分组
2. 项目内按分类分组
3. 分类内按时间排序（最新在前）
4. 合并相似提交（如多条 "docs(readme)" 提交 → 一条加数量标注）

## 进行中工作识别信号

识别可能仍在进行中的工作：

- 主题包含：WIP, TODO, draft, partial, temp, workaround, 临时, 待办
- 正文包含："still need to", "remaining", "follow-up", "next step", "还需要", "后续"
- 尚未合并到主分支的功能分支

## 重要事项识别信号

识别值得特别标注的提交：

- 主题包含：breaking, BREAKING, security, critical, important, milestone, 重要, 关键
- 正文包含："breaking change", "security fix", "migration required", "破坏性变更", "安全修复"
- 大范围变更（单条提交修改文件数 > 10）
- 实现重大功能的首条提交
