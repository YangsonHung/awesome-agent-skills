---
name: yuque-lakebook-export-cn
description: 将语雀知识库、语雀文档或 .lakebook 文件导出并转换为本地 Markdown 目录，适配 Obsidian 使用。适用于导出语雀、把 lakebook 转成 Markdown、迁移语雀知识库到 Obsidian、批量转换多个 .lakebook、处理语雀导出后的图片与附件、裁剪图片、内部文档链接、目录结构、Markdown 表格渲染等问题。当用户提到 语雀、lakebook、导出 Markdown、导入 Obsidian、知识库迁移、批量转换、图片不显示、链接丢失、裁剪失效、目录层级不对、表格显示异常 等场景时触发。
license: MIT
---

# 语雀 Lakebook 导出

将一个或多个语雀 `.lakebook` 文件导出为本地 Markdown 目录，并优先适配 Obsidian。

## 何时使用

当用户需要以下能力时使用本技能：

- 导出一个或多个语雀 `.lakebook`
- 将语雀知识库转换为 Markdown
- 将语雀内容迁移到 Obsidian
- 修复语雀导出后的图片、裁剪图、内部链接、目录层级、表格渲染问题

## 不要使用

不要将本技能用于：

- 与语雀或 `.lakebook` 无关的普通 Markdown 编辑
- 网页抓取任务
- 非语雀来源的导出转换任务

## 使用说明

1. 优先使用非交互模式，便于 Agent 稳定执行。
2. 如果系统 Python 被 PEP 668 限制，或无法直接安装依赖，统一使用固定缓存虚拟环境，不要在任务目录里临时创建环境。
3. 优先复用下面这个固定环境：

```bash
~/.agents/cache/yuque-lakebook-export/.venv
```

4. 只有在它不存在时才创建，并把依赖装进去：

```bash
python3 -m venv ~/.agents/cache/yuque-lakebook-export/.venv
~/.agents/cache/yuque-lakebook-export/.venv/bin/python -m pip install -r scripts/requirements.txt
```

5. 优先使用下面这个包装入口，它会自动处理固定缓存虚拟环境：

```bash
python3 scripts/run_export.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

6. 如果当前 Python 环境允许直接安装依赖，也可以直接执行：

```bash
python3 -m pip install -r scripts/requirements.txt
```

7. 不要在当前工作目录、用户下载目录、或 skill 目录下创建 `.venv`、`.yuque-export-venv` 这类临时环境。
8. 单文件执行：

```bash
python3 scripts/run_export.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

9. 批量执行：

```bash
python3 scripts/run_export.py -l "/path/to/your_file_1.lakebook" "/path/to/your_file_2.lakebook" -o "/target/root"
```

10. 如果使用固定缓存虚拟环境直接执行，就用它的 Python 来运行：

```bash
~/.agents/cache/yuque-lakebook-export/.venv/bin/python scripts/cli.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

11. 只有在用户明确要求终端交互选择时，才运行：

```bash
python3 scripts/run_export.py
```

12. 导出完成后检查：
- `.md` 文件是否生成
- 同名 `.assets` 目录是否生成
- 内部链接是否转为相对 Markdown 路径
- 图片是否能在 Obsidian 中正常显示

13. 如果导出失败，优先查看输入 `.lakebook` 同目录下生成的批量日志。

详细行为、输出规则和排查说明见 `references/usage.md`。
