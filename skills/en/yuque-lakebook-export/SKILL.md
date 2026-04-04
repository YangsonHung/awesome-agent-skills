---
name: yuque-lakebook-export
description: Export Yuque knowledge bases, Yuque documents, or .lakebook files into local Markdown folders for Obsidian. Use when users want to export Yuque, convert lakebook to Markdown, migrate a Yuque knowledge base to Obsidian, batch-convert multiple .lakebook files, or fix Yuque export issues such as missing images, cropped image mismatches, broken internal links, wrong folder hierarchy, and Markdown table rendering problems.
license: MIT
---

# Yuque Lakebook Export

Convert one or more Yuque `.lakebook` files into local Markdown folders, with images and internal document links prepared for Obsidian.

## When to Use

Use this skill when the user asks for:

- Exporting one or more Yuque `.lakebook` files
- Converting a Yuque knowledge base into Markdown
- Migrating Yuque content into Obsidian
- Fixing Yuque export issues around images, cropped images, internal links, hierarchy, or tables

## Do not use

Do not use this skill for:

- Generic Markdown editing that does not involve Yuque or `.lakebook`
- Website scraping tasks
- Export tasks that already come from a non-Yuque format

## Instructions

1. Prefer non-interactive execution so the agent can run deterministically.
2. Before first use, install dependencies:

```bash
python3 -m pip install -r scripts/requirements.txt
```

3. Standard single-file execution:

```bash
python3 scripts/cli.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

4. Standard batch execution:

```bash
python3 scripts/cli.py -l "/path/to/your_file_1.lakebook" "/path/to/your_file_2.lakebook" -o "/target/root"
```

5. Only use interactive mode when the user explicitly wants terminal selection:

```bash
python3 scripts/cli.py
```

6. After export, verify:
- `.md` files exist
- sibling `.assets` folders exist
- internal links are relative Markdown paths
- images render in Obsidian

7. If export fails, inspect the batch log written next to the input `.lakebook` files.

For detailed behavior, troubleshooting, and output rules, read `references/usage.md`.
