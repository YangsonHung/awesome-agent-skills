# Usage

## Inputs

- One or more `.lakebook` files
- One output root directory

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

- Missing `bs4`: install `scripts/requirements.txt`
- Missing images in Obsidian: check generated `.assets` paths and URL encoding
- Wrong table rendering: re-export with the bundled parser because it normalizes Markdown spacing
- Broken internal links: ensure the source `.lakebook` includes complete toc metadata
