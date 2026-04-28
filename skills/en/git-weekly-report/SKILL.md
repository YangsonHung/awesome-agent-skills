---
name: git-weekly-report
description: Summarize git commit logs into a structured weekly or daily report (周报, 日报) with sections for completed work, in-progress items, highlights, plans, and risks. Use when the user asks to generate a weekly report, daily report, summarize yesterday's git commits, review what they did today/this week, summarize recent git activity, or categorize commits by project. Triggers on keywords like git log, commit history, daily standup, work summary, 周报, 日报, 昨天做了什么, 今天的工作, 总结昨天, 本周工作, git活动, 提交记录.
---

# Git Weekly Report

Extract git commit logs and generate a structured weekly or daily report.

## When to Use

Use this skill when the user asks for:
- Generating a weekly report (周报) or daily report (日报) from git commits
- Summarizing yesterday's or today's git activity
- Summarizing recent git activity across one or more repositories
- Reviewing what work was done over a date range
- Compiling commit history into a categorized report
- Preparing a daily standup summary from commits

## Do not use

Do not use this skill for:
- Code review of specific changes (use code-reviewer instead)
- Inspecting a single commit in detail
- Git operations other than log extraction (branching, merging, etc.)
- Non-git-related report generation

## Instructions

1. Determine the date range and report type:
   - **Daily report (日报)**: if user says "yesterday", "today", "昨天", "今天", "日报" — default `--since` to yesterday, `--until` to today
   - **Weekly report (周报)**: if user says "this week", "本周", "周报" — default `--since` to last Monday, `--until` to today
   - Otherwise: default to last 7 days. Accept user overrides.
2. Determine the author filter if the user specifies one. Default: all authors.
3. Determine repository path(s). Default: current working directory. If the user mentions multiple projects, collect all paths.
4. Run the script:

```bash
python3 scripts/git_weekly_report.py --since <YYYY-MM-DD> --until <YYYY-MM-DD> [--author <name>] [--repo <path1> <path2> ...]
```

5. Read the JSON output. The script provides structured commit data grouped by repository.
6. Use [weekly-report-format.md](references/weekly-report-format.md) as the categorization guide to classify commits by type.
7. Use [weekly-report-template.md](assets/templates/weekly-report-template.md) as the output structure when generating the final report.
8. For "next-week plans" and "risks" sections: ask the user if they have items to add, since these are not derivable from git logs. For daily reports, omit these sections unless the user requests them.
9. Present the final Markdown report. Save to a file if the user requests it.

## Script Usage

```bash
# Default: last 7 days, current directory
python3 scripts/git_weekly_report.py

# Specific date range
python3 scripts/git_weekly_report.py --since 2026-04-21 --until 2026-04-28

# With author filter
python3 scripts/git_weekly_report.py --since 2026-04-21 --author "Yang"

# Multiple repositories
python3 scripts/git_weekly_report.py --since 2026-04-21 --repo /path/to/project-a /path/to/project-b

# Save output to file
python3 scripts/git_weekly_report.py --since 2026-04-21 --output /tmp/weekly.json

# Include merge commits
python3 scripts/git_weekly_report.py --since 2026-04-21 --merges
```

## JSON Output Structure

The script outputs JSON with this structure:

- `date_range`: `{ since, until }` — the queried date range
- `author_filter`: string or null — applied author filter
- `repositories`: array of `{ path, name, commit_count, commits }`
- `total_commits`: total across all repositories

Each commit has: `hash`, `short_hash`, `author`, `date`, `subject`, `body`, `refs`.

## Report Generation

When commits exceed 50 per repository, summarize by category rather than listing every commit individually. Always preserve short hashes for traceability.

For the "In Progress" section, look for signals like: WIP, TODO, partial implementations, or incomplete feature branches.

For the "Highlights" section, identify: breaking changes, security fixes, major features, or commits touching critical paths.
