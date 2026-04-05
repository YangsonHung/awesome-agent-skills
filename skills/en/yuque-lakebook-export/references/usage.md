# Usage

## Inputs

- One or more `.lakebook` files
- One output root directory
- Preferred entry point: `uv run python scripts/cli.py ...`

## Outputs

For a document named `your_document`:

```text
your_document.md
your_document.assets/
```

- `your_document.md` contains the Markdown body
- `your_document.assets/` stores downloaded images and attachments

## Supported behavior

- Yuque internal links become relative Markdown links
- Titles containing `/` or `\` are sanitized
- Pages without children stay as a direct `.md` file
- Pages with children create a same-name folder and keep the page as `same-name.md`
- Images preserve Yuque crop settings when crop metadata exists
- Batch execution continues after individual file failures

## Troubleshooting

- First switch into the installed skill tool directory, then run `uv sync`; this is the directory that contains `SKILL.md`, `pyproject.toml`, `uv.lock`, and `scripts/`
- Both `uv sync` and `uv run python scripts/cli.py ...` must be executed from that skill tool directory, not from the `.lakebook` source directory, the output directory, or the user's current workspace root
- Avoid creating task-local virtual environments under the user's working directory, download directory, or any task directory
- Missing `bs4`: run `uv sync`
- Missing images in Obsidian: check generated `.assets` paths and URL encoding
- Wrong table rendering: re-export with the bundled parser because it normalizes Markdown spacing
- Broken internal links: ensure the source `.lakebook` includes complete toc metadata
