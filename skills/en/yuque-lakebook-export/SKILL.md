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
2. If the system Python is blocked by PEP 668 or cannot install dependencies directly, use a fixed cache virtual environment instead of creating a task-local environment.
3. Reuse this environment when it already exists:

```bash
~/.agents/cache/yuque-lakebook-export/.venv
```

4. Create it only when missing, then install dependencies into it:

```bash
python3 -m venv ~/.agents/cache/yuque-lakebook-export/.venv
~/.agents/cache/yuque-lakebook-export/.venv/bin/python -m pip install -r scripts/requirements.txt
```

5. Prefer using the wrapper script below. It handles the cached virtual environment automatically:

```bash
python3 scripts/run_export.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

6. If direct installation is allowed, installing dependencies into the active Python environment is acceptable:

```bash
python3 -m pip install -r scripts/requirements.txt
```

7. Do not create `.venv`, `.yuque-export-venv`, or similar temporary environments inside the current working directory, the user's download directory, or the skill directory.
8. Standard single-file execution:

```bash
python3 scripts/run_export.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

9. Standard batch execution:

```bash
python3 scripts/run_export.py -l "/path/to/your_file_1.lakebook" "/path/to/your_file_2.lakebook" -o "/target/root"
```

10. When using the cached virtual environment directly, invoke the script with that interpreter:

```bash
~/.agents/cache/yuque-lakebook-export/.venv/bin/python scripts/cli.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

11. Only use interactive mode when the user explicitly wants terminal selection:

```bash
python3 scripts/run_export.py
```

12. After export, verify:
- `.md` files exist
- sibling `.assets` folders exist
- internal links are relative Markdown paths
- images render in Obsidian

13. If export fails, inspect the batch log written next to the input `.lakebook` files.

For detailed behavior, troubleshooting, and output rules, read `references/usage.md`.
