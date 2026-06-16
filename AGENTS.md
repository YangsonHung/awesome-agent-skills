# Repository Guidelines

## Project Structure & Module Organization
This repository is a skill pack for AI agents, organized by skill directories under `skills/`.

- `skills/en/`: all English skills
  - `skills/en/novel-writer/`
  - `skills/en/multi-lang-readme/`
  - `skills/en/conversation-json-to-md/`
  - `skills/en/topic-bookmarks-reorganizer/`
  - `skills/en/wechat-theme-extractor/`
  - `skills/en/mac-software-storage-cleanup/`
  - `skills/en/ui-layout-analyzer/`
  - `skills/en/yuque-lakebook-export/`
  - `skills/en/git-weekly-report/`
  - `skills/en/git-push-secondary-merge-primary/`
  - `skills/en/git-pushing-fast/`
  - `skills/en/frontend-quality-guardrails/`
  - `skills/en/feature-doc-splitter/`
- `skills/zh-cn/`: all Chinese skills
  - `skills/zh-cn/novel-writer-cn/`
  - `skills/zh-cn/multi-lang-readme-cn/`
  - `skills/zh-cn/conversation-json-to-md-cn/`
  - `skills/zh-cn/topic-bookmarks-reorganizer-cn/`
  - `skills/zh-cn/wechat-theme-extractor-cn/`
  - `skills/zh-cn/mac-software-storage-cleanup-cn/`
  - `skills/zh-cn/ui-layout-analyzer-cn/`
  - `skills/zh-cn/yuque-lakebook-export-cn/`
  - `skills/zh-cn/git-weekly-report-cn/`
  - `skills/zh-cn/git-push-secondary-merge-primary-cn/`
  - `skills/zh-cn/git-pushing-fast-cn/`
  - `skills/zh-cn/frontend-quality-guardrails-cn/`
  - `skills/zh-cn/feature-doc-splitter-cn/`
- `README.md`: default English project overview
- `README.zh-CN.md`: Chinese overview
- `LICENSE`, `.gitignore`: repository-level metadata

When adding a new skill, you must add both language variants together: `skills/en/<skill-name>/` and `skills/zh-cn/<skill-name>-cn/`. Single-language submissions are not accepted.

## Build, Test, and Development Commands
This repository has no compile/build pipeline. Typical contributor commands are:

- `git status` — inspect local changes before committing
- `git diff` — review exact content changes
- `python3 scripts/validate_skills.py --strict` — validate skill structure, bilingual counterparts, and English skill language rules
- `node scripts/validate-skills.js --strict` — run the legacy/alternative strict validator
- `git config core.hooksPath .githooks` — enable the local pre-commit validation hook
- `cp -r skills/ ~/.claude/skills/` — install skills locally for manual validation
- `find skills -maxdepth 3 -type f` — quick structure check before PR

## Coding Style & Naming Conventions
Use concise, instructional Markdown with clear headings.

- File names: `kebab-case` for skill folders (for example, `novel-writer-cn`)
- Skill command naming:
  - English skills use the base command name with no `-en` suffix
  - Chinese skills append `-cn`
  - Keep the folder name and `SKILL.md` frontmatter `name` aligned with the command name
  - Every skill must have both English and Chinese variants, and the pair must stay aligned in purpose, structure, and trigger coverage
  - English `skills/en/**/SKILL.md` files must not contain Chinese/Han characters; put Chinese examples, triggers, and localized wording in the matching `skills/zh-cn/**/SKILL.md`. The only exception is `skills/en/multi-lang-readme/SKILL.md`, where language-switch examples may show native language names.
- Skill metadata and opening structure:
  - Treat frontmatter `description` as routing metadata for model skill selection. Keep it short and focused on when the skill should be used.
  - English skill descriptions must start with `Use when ...`.
  - Chinese skill descriptions must use natural Chinese trigger wording, such as `当用户……时使用。`; do not start Chinese descriptions with English `Use when`.
  - Do not mention a specific agent in descriptions, such as `Use when Codex is asked ...`; describe the user need or task instead.
  - Move longer purpose, capabilities, outputs, and boundaries into the first body section, `## Overview`.
  - Keep `## When to Use` / `## 何时使用` as the concrete trigger checklist after `## Overview` so validators and readers can find usage rules.
- Required skill file: `SKILL.md`
- Optional files/folders (add only when needed): `README.md`, `scripts/`, `references/`, `assets/`
- Keep bilingual docs separated (English default in `README.md`, Chinese in `README.zh-CN.md`)

Prefer short sections, bullet lists, and copy-pastable examples.

## Testing Guidelines
Testing is documentation-driven and manual:

1. Verify links and paths in all edited Markdown files.
2. Validate trigger examples are clear and actionable.
3. If skill logic changes, install locally and run at least one prompt per trigger example.
4. Run both strict validators before committing: `python3 scripts/validate_skills.py --strict` and `node scripts/validate-skills.js --strict`.

The `.githooks/pre-commit` hook runs strict skill validation, including the English skill language rule, when `core.hooksPath` points to `.githooks`.

## Commit & Pull Request Guidelines
Follow Conventional Commits as seen in project history:

- `docs(readme): split bilingual docs with English as default`
- `chore(git): add .gitignore for macOS metadata`

PRs should include:

- A short summary of what changed and why
- Affected paths (for example, `skills/en/novel-writer/SKILL.md`)
- Screenshots only when visual docs/rendering are relevant
- Linked issue/task if available

Keep each PR focused on one logical change.

## Skill Directory Maintenance

When a skill is added or removed, update the following locations to keep the directory in sync:

1. This file (`AGENTS.md`) — Project Structure & Module Organization section
2. `README.md` — Available Skills table and Trigger Examples section
3. `README.zh-CN.md` — 可用技能 table and 触发示例 section
4. Badge count in `README.md` and `README.zh-CN.md`
