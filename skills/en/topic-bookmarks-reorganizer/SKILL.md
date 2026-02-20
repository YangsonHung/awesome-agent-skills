---
name: topic-bookmarks-reorganizer
description: Reorganize exported browser bookmarks under one target topic folder (for example AI) into cleaner categories, remove duplicate URLs, and generate an importable Netscape HTML file. Use when users ask to analyze a bookmarks export, extract one topic directory, regroup links/subfolders, and output a browser-importable HTML file.
risk: safe
source: YangsonHung/awesome-agent-skills
license: MIT
---

# Topic Bookmarks Reorganizer

Reorganize one topic folder from a browser bookmarks export into a cleaner importable file.

## When to Use

Use this skill when the user asks for one or more of these tasks:
- Analyze one bookmarks export file and find a topic folder (for example `AI`)
- Re-classify links and subfolders under that topic
- Remove duplicate links by URL
- Output a new HTML file that can be imported into a browser
- Keep only the target topic folder in the output

## Do not use

Do not use this skill when:
- The input is not a bookmarks export HTML file
- The user only wants manual writing help with no file processing
- The user asks for unrelated JSON/PDF/Docx transformations

## Instructions

1. Ask for required input:
- Export file path
- Target topic folder name (default `AI`)
- Output file path

2. Run the script in report mode first:

```bash
python3 scripts/reorganize_topic_bookmarks.py \
  --input /path/to/bookmarks.html \
  --output /tmp/topic-preview.html \
  --topic-folder "AI" \
  --mode auto \
  --lang en \
  --report /tmp/topic-report.json \
  --print-report
```

3. Confirm final options with user only if needed:
- `--mode ai` for AI-focused mapping
- `--mode generic` for general-topic mapping
- `--no-dedupe-url` to keep duplicate URLs

4. Generate final output:

```bash
python3 scripts/reorganize_topic_bookmarks.py \
  --input /path/to/bookmarks.html \
  --output /path/to/topic-bookmarks-reorganized.html \
  --topic-folder "AI" \
  --mode auto \
  --lang en
```

5. Validate and report:
- Confirm output file exists
- Report input links, output links, and removed duplicate count
- Confirm output contains exactly one top-level folder: the target topic

## Output Expectations

- Output format is Netscape bookmarks HTML and is browser-importable
- Output contains only the target topic folder
- Links keep original `<A ...>` attributes (for example add-date/icon)
- Folder structure is reorganized into high-level categories
