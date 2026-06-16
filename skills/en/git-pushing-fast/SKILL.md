---
name: git-pushing-fast
description: Use when committing and pushing current changes on one branch with a Conventional Commit message.
---

# Git Pushing Fast

## Overview

Commit and push the current repository's local changes on the current branch with a fast, safe single-branch workflow.

The default output is one focused Conventional Commit plus a push to the tracked remote branch. For non-trivial changes, write a segmented commit body so reviewers can quickly see what changed by topic.

This workflow handles ordinary single-branch handoff requests such as saving current work to the remote, without branch merging, history rewriting, or PR creation.

## When to Use

Use this skill when the user asks to:
- Commit and push the current work
- Push this, save to remote, or finish a normal single-branch handoff
- Create one Conventional Commit from staged and unstaged changes
- Include a readable commit body that groups changes by feature area, UI area, tests, docs, or validation

## Do Not Use

Do not use this skill for:
- Multi-branch flows that merge a work branch into a primary branch
- Force-push, rebase, squash, amend, or history-rewrite requests
- Pull request creation unless the user explicitly asks for it after the push
- Code review, release notes, weekly reports, or changelog generation
- Destructive commands such as `git reset --hard` or `git checkout -- <file>`

## Instructions

Follow this workflow in order. Stop and report the blocker instead of guessing when the target repository, branch, or push destination is unclear.

1. Inspect the repository.
   - Run `git status --short`, `git branch --show-current`, and `git remote -v`.
   - Check the upstream with `git rev-parse --abbrev-ref --symbolic-full-name @{u}` when possible.
   - Review the staged diff with `git diff --cached --stat`; if nothing is staged, review `git diff --stat`.
   - Never discard or revert user changes.

2. Stage changes.
   - If the user asked to commit everything, run `git add -A`.
   - If the user requested a narrower scope, stage only that scope.
   - Re-run `git status --short` and verify the intended files are staged.

3. Build the commit message.
   - Use Conventional Commits: `type(scope): concise summary` in the repository's existing commit language.
   - Choose the type from the actual diff: usually `fix`, `feat`, `docs`, `refactor`, `test`, `chore`, or `ci`.
   - Keep the subject under 72 characters when practical.
   - For non-trivial changes, include a segmented body with 2-5 short sections.
   - Each section title should name the affected area, followed by bullet points.
   - Include a `Tests:` or localized equivalent section when tests, validators, hooks, or manual verification ran.

Example segmented body:

```text
fix(module): update component behavior

Behavior:
- Adjust the default state for the affected component.
- Keep existing behavior unchanged for unsupported input.

Implementation:
- Move repeated logic into a small helper.
- Update related configuration to use the new helper.

Tests:
- Add coverage for the updated behavior.
- Run the relevant validator before pushing.
```

4. Commit.
   - Use `git commit` with multiple `-m` arguments or an editor-free equivalent so the body is preserved.
   - Do not use `--no-verify`.
   - If hooks or validation fail, fix the failure and retry the commit.

5. Push.
   - If the current branch has an upstream, run `git push`.
   - If there is no upstream, run `git push -u origin <current_branch>` unless the repository or user specifies another remote.
   - If the push is rejected because the remote moved, run `git fetch` and inspect before retrying.
   - Do not force-push unless the user explicitly requested force-push and the risk has been confirmed.

6. Report.
   - Keep the final response concise.
   - Include the commit hash, branch, remote push result, and validation that ran.
   - If the host app supports Git directives, emit them only after the matching action succeeds.
