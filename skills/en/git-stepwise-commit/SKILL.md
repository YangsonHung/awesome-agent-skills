---
name: git-stepwise-commit
description: Use when planning or creating logical commits, or committing and pushing; exclude push-only, history rewriting, and explicitly single-commit requests.
---

# Git Stepwise Commit

## Overview

Organize authorized changes into a sequence of appropriately sized commits with explicit dependencies. Start with technical boundaries, then group by business module and purpose. Each commit expresses one complete intent.

One request is one batch. Every subject in that batch shares the same short topic, even when commits cover different modules.

## When to Use

- The user asks to commit changes, split commits by module or frontend/backend, or commit and push.
- If the user asks only for splitting advice, present a plan without committing.

## Do Not Use

Do not use for pushing existing commits only, rewriting history, or an explicitly requested single commit.

## Scope

- A commit request includes analysis and execution; do not ask again solely to confirm the grouping after showing the plan.
- Default to local commits; push only when requested, after the commit chain has been checked. Do not add branch creation, merging, PR creation, release, or history rewriting.
- User-specified scope, grouping, and order take precedence. One complete unit may produce one commit; do not manufacture extra commits.
- When another commit skill also applies, this skill owns grouping, order, and the fixed-topic series of subjects. Reuse applicable checks and delivery requirements without adopting its default single-commit behavior.

## Splitting Criteria

Technical boundaries are the starting point; business intent and dependencies determine the final grouping:

| Boundary | Default grouping |
| --- | --- |
| Database | Business domain, including structure, migrations, and corresponding schema mappings |
| Backend | Service, business module, or independent use case |
| Frontend | Application, business module, or independent interaction |
| Configuration and engineering | Independent build, dependency, deployment, or CI purpose |
| Shared packages and other stacks | Package, consumers, and responsibility |
| Independent documentation | Topic; implementation notes normally accompany the implementation |

Separate frontend and backend by default, as well as unrelated modules within each. Judge responsibility rather than file extension. Each commit should have a concrete one-sentence explanation, complete behavioral or structural meaning, a clear rollback boundary, and be buildable and verifiable with its predecessors present.

- Split changes that mix unrelated goals, business modules, or independently deliverable refactoring and features.
- Combine file-level style, import, type, or test changes that lack independent meaning. An independent one-line fix may still be its own commit.
- Do not impose limits based on file count, line count, or a fixed number of commits; many generated files may form one unit.

Keep necessary atomic combinations together:

- Implementation, corresponding behavioral tests, and necessary notes; dependency declarations and lockfiles; minimum configuration needed to run the implementation.
- Baseline and incremental migrations, pure schema mappings, and migration tests for the same database change. Separate independent backend use cases.
- Generated inputs and outputs that must stay synchronized. Assign generated code to its actual service or consumer, without creating stale contracts.
- Split independent changes within a file by hunk where possible. If shared types, renames, or cross-file dependencies cannot be separated, combine the smallest necessary scope and explain why.

## Subject Format

Use `type(scope): [number]batch topic：specific description`, for example `feat(database): [1]Order payment：add payment status and migration`.

- **Standard prefix:** Follow repository requirements first; otherwise use Conventional Commits. Choose type per change and scope for its boundary or module. They may vary between commits; neither the batch topic nor the number replaces the prefix, and unrelated changes must not be forced into one type.
- **Fixed topic:** Choose one short business name, `batch_topic`, from the complete delivery goal during planning. Reuse it verbatim across the batch, including database, frontend, backend, configuration, and different modules. Put module names and differences in the scope or specific description.
- **Numbering:** Put `[1]`, `[2]`, `[3]` after the prefix and before the fixed topic, consecutively in actual commit order across the batch. Failed retries do not consume a number. When continuing the same batch, recover the topic and next number from successful subjects. Only an explicit request for a separate batch permits a new topic and numbering; do not rewrite existing history.
- **Punctuation and spacing:** Use an ASCII colon and a space after the standard prefix, and a fullwidth colon immediately after the topic. Follow the repository's explicit subject format if it differs.

For a batch covering home-page sending and thinking state, choose `batch_topic = Conversation experience`:

```text
fix(commercial): [1]Conversation experience：prevent duplicate home-page sends
feat(commercial): [2]Conversation experience：show thinking and streaming feedback
```

Subjects using different topics for the two modules are invalid even if their numbering and Conventional Commit prefixes are correct. Verify the entire `[number]fixed topic：` portion when using the default format; otherwise verify the equivalent portion in the repository's required format.

## Instructions

### 1. Determine Scope

Read repository and affected-directory `AGENTS.md` files, delivery rules, and relevant submodule rules. Inspect the branch and operation state, `git status --short`, the complete staged and unstaged diffs, and untracked files from `git ls-files --others --exclude-standard` that may be included.

- User-specified scope is the limit. If no scope is specified and changes are staged, default to the original staged changes only. Otherwise use the current task to determine scope without including unrelated work.
- Record the initial HEAD and staged boundary. Before reorganizing the index, save the original staged diff as a binary patch or equivalent snapshot outside the repository, preserving the exact contents of partially staged files.
- If a merge, rebase, or cherry-pick is incomplete or conflicts exist, follow the corresponding workflow without changing its state arbitrarily. Exclude real credentials and private local configuration.

### 2. Group and Order

Plan commit units using the splitting criteria and actual dependencies: a commit must not reference types, fields, packages, or configuration introduced only later. Cyclic dependencies usually mean the units are too small; combine the smallest complete unit instead of refactoring business logic just to split it.

Choose the single `batch_topic` before execution. Generate all proposed subjects from it and show a brief table of order, complete subjects, files or hunks, and prerequisites, plus key validation. No in-repository plan document is needed. Check that every topic is identical and numbering consecutive. Freeze the topic after the first successful commit; later changes to the plan may adjust only scopes, descriptions, and the order of uncommitted units.

Plan submodule commits separately but share the batch topic and numbering across the delivery. Complete submodule commits first, then handle the parent repository pointer and push order according to project rules.

### 3. Validate the Commit Chain

Run applicable project checks, including required review tools, tests, review rounds, and applicable exceptions. Do not impose a fixed number of rounds or extra tools on your own.

- Review may cover the full proposed chain, with valid findings reused for individual commits. Recheck affected areas when content or hunk splits change intermediate semantics.
- Whole-worktree validation does not prove each commit snapshot works. If later uncommitted content could hide a missing dependency, validate intermediate states in an isolated worktree or equivalent snapshot; adjust grouping or dependencies on failure.
- Do not add tests solely for splitting or operate a real database to validate migrations. Report checks not covered. Resolve failed required checks or findings meeting the project's blocking criteria before committing affected units and their dependents.

### 4. Commit Each Unit

For each unit:

1. Isolate staged content using explicit paths, hunks, or precise patches. Adjust only the index, not the worktree. Do not stage an entire partially staged file or sweep later units in with `git add -A`.
2. Inspect the complete `git diff --cached` and `git diff --cached --check`, confirming scope, dependencies, and valid review coverage. Do not create an empty commit.
3. Compose the subject from the frozen `batch_topic` and next number; do not regenerate the topic from the current module. Verify the exact topic, consecutive number, and separator required by the applicable format before committing; single-subject commitlint cannot replace this batch check. For non-trivial changes, describe purpose, main changes, actual validation, and project-required diagnostics in the body. Pass multiline messages safely, for example with a temporary file and `git commit -F`.
4. Commit normally without bypassing hooks. After success, inspect `git log -1 --format=%s` against the plan, then advance the number and check the actual patch and hash. If a hook or concurrent edit changes content, recheck the affected scope before continuing. On failure, inspect index and worktree changes, fix the cause, and recheck rather than retrying blindly.

Finally, check every actual subject in order for the exact `batch_topic` and consecutive numbers, then compare the cumulative diff and remaining changes against the authorized scope. If subject consistency fails, do not mark the batch complete or push. When stopping, preserve uncommitted content and original staging ownership; report boundaries that could not be restored. Do not automatically amend, reset, or squash. Push normally only if authorized; investigate rejection before retrying and do not force-push automatically.

## Delivery

List commit hashes, subjects, and modules in order. Summarize actual checks, remaining changes, and push status. If partially completed, identify the unfinished units and why.
