# Repository Guidelines

## Project Structure & Module Organization
This repository is a skill pack for AI agents, organized by skill directories under `skills/`.

- `skills/en/`: all English skills
  - `skills/en/novel-writer/`
  - `skills/en/multi-lang-readme/`
  - `skills/en/conversation-json-to-md/`
  - `skills/en/topic-bookmarks-reorganizer/`
- `skills/zh-cn/`: all Chinese skills
  - `skills/zh-cn/novel-writer-cn/`
  - `skills/zh-cn/multi-lang-readme-cn/`
  - `skills/zh-cn/conversation-json-to-md-cn/`
  - `skills/zh-cn/topic-bookmarks-reorganizer-cn/`
- `README.md`: default English project overview
- `README.zh-CN.md`: Chinese overview
- `LICENSE`, `.gitignore`: repository-level metadata

When adding a new skill, place it under `skills/en/<skill-name>/` or `skills/zh-cn/<skill-name>/` and keep a minimal self-contained structure.

## Build, Test, and Development Commands
This repository has no compile/build pipeline. Typical contributor commands are:

- `git status` — inspect local changes before committing
- `git diff` — review exact content changes
- `cp -r skills/ ~/.claude/skills/` — install skills locally for manual validation
- `find skills -maxdepth 3 -type f` — quick structure check before PR

## Coding Style & Naming Conventions
Use concise, instructional Markdown with clear headings.

- File names: `kebab-case` for skill folders (for example, `novel-writer-cn`)
- Required skill file: `SKILL.md`
- Optional files/folders (add only when needed): `README.md`, `scripts/`, `references/`, `assets/`
- Keep bilingual docs separated (English default in `README.md`, Chinese in `README.zh-CN.md`)

Prefer short sections, bullet lists, and copy-pastable examples.

## Testing Guidelines
Testing is documentation-driven and manual:

1. Verify links and paths in all edited Markdown files.
2. Validate trigger examples are clear and actionable.
3. If skill logic changes, install locally and run at least one prompt per trigger example.

There is currently no automated test framework or coverage gate.

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
