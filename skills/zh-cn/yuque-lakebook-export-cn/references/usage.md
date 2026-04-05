# 使用说明

## 输入

- 一个或多个 `.lakebook` 文件
- 一个目标根目录
- 优先使用入口：`uv run python scripts/cli.py ...`

## 输出

假设文档名为 `your_document`，输出结构为：

```text
your_document.md
your_document.assets/
```

- `your_document.md` 保存正文
- `your_document.assets/` 保存图片和附件

## 支持行为

- 语雀内部链接转换为相对 Markdown 链接
- 标题中的 `/` 和 `\` 会自动清洗
- 没有子文档的页面直接导出为单个 `.md`
- 有子文档的页面会创建同名目录，并保留同名页面文件
- 如果图片卡片包含裁剪信息，会下载裁剪后的图片版本
- 批量执行时单个文件失败不会中断整个批次

## 排查

- 先切换到当前已安装 skill 的工具目录，再执行 `uv sync` 同步依赖；这个目录应包含 `SKILL.md`、`pyproject.toml`、`uv.lock` 和 `scripts/`
- `uv sync` 和 `uv run python scripts/cli.py ...` 都必须在该 skill 工具目录执行，不要在 `.lakebook` 所在目录、输出目录或用户当前工作区根目录执行
- 不要在用户当前工作目录、下载目录或任意任务目录下手动创建临时虚拟环境
- 缺少 `bs4`：执行 `uv sync`
- Obsidian 图片不显示：检查 `.assets` 路径和链接编码
- 表格渲染异常：重新导出，脚本会做 Markdown 规范化
- 内部链接失效：确认源 `.lakebook` 包含完整目录元数据
