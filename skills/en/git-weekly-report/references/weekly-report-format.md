# Weekly Report Categorization Guide

## Conventional Commit Mapping

Map commit prefixes to report categories:

| Prefix | Category |
|--------|----------|
| `feat:` | New Features |
| `fix:` | Bug Fixes |
| `refactor:` | Refactoring |
| `docs:` | Documentation |
| `chore:` | Maintenance |
| `test:` | Testing |
| `perf:` | Performance |
| `style:` | Code Style |
| `ci:` | CI/CD |
| `build:` | Build System |

## Non-Conventional Commits

When commits lack conventional prefixes, infer category from keywords:

- **New Features**: add, implement, create, introduce, support, enable
- **Bug Fixes**: fix, resolve, repair, patch, workaround, hotfix
- **Refactoring**: refactor, restructure, reorganize, simplify, clean up, migrate
- **Documentation**: docs, readme, guide, comment, document
- **Maintenance**: update, upgrade, bump, deps, dependency, config, chore
- **Testing**: test, spec, coverage, verify, assert
- **Performance**: optimize, speed, fast, slow, latency, memory

## Grouping Strategy

1. Group by project first (repository name)
2. Within each project, group by category
3. Within each category, list commits chronologically (newest first)
4. Merge similar commits (e.g., multiple "docs(readme)" commits → one entry with count)

## In-Progress Detection Signals

Identify work that may still be in progress:

- Subject contains: WIP, TODO, draft, partial, temp, workaround
- Body contains: "still need to", "remaining", "follow-up", "next step"
- Feature branches not yet merged to main

## Highlight Detection Signals

Identify commits worth highlighting:

- Subject contains: breaking, BREAKING, security, critical, important, milestone
- Body contains: "breaking change", "security fix", "migration required"
- Large scope changes (files changed > 10 in a single commit)
- First commit implementing a major feature
