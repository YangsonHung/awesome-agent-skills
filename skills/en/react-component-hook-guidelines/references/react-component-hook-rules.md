# React Component and Hook Development Guidelines

## Contents

1. [Scope](#1-scope)
2. [Core Principles](#2-core-principles)
3. [File and Naming Conventions](#3-file-and-naming-conventions)
4. [Component Responsibility Boundaries](#4-component-responsibility-boundaries)
5. [Props Design Standards](#5-props-design-standards)
6. [Complexity Control](#6-complexity-control)
7. [Branching and Pattern Expansion Standards](#7-branching-and-pattern-expansion-standards)
8. [Split Suggestions for Hooks, Utils, and Components](#8-split-suggestions-for-hooks-utils-and-components)
9. [Recommended Layering](#9-recommended-layering)
10. [Biome Coordination](#10-biome-coordination)
11. [Code Review Checklist](#11-code-review-checklist)
12. [Exception Rules](#12-exception-rules)
13. [Implementation Suggestions](#13-implementation-suggestions)
14. [One-Sentence Summary](#14-one-sentence-summary)

This document applies to React + TypeScript + Biome frontend projects. Its goal is to standardize how components, Hooks, page orchestration, and business logic are split, reduce coupling, control complexity, and provide a reusable code organization convention across projects.

## 1. Scope

- Applies to page components, business components, shared UI components, custom Hooks, and page orchestration Hooks.
- Applies to common frontend directory structures such as `features/`, `components/`, `hooks/`, `pages/`, and `routes/`.
- This standard primarily addresses mixed responsibilities, overly wide interfaces, branch spread, and component bloat.

## 2. Core Principles

### 2.1 Single Responsibility First

- One component should keep only one core responsibility.
- One component should do one main thing.
- One Hook should encapsulate one concern.
- File length is not the root problem; mixed responsibility is.

### 2.2 Composition Over Piling On

- Anything above a certain level of complexity must be split into child components or custom Hooks.
- When business logic is heavy, split into a Hook first instead of piling hundreds of lines into a component.
- Extract complex event handling into custom Hooks or action functions.
- For complex branching, prefer mapping tables, strategy objects, or child components instead of more `if/else`.

### 2.3 Separate Presentation from Orchestration

- Page components assemble.
- Business Hooks handle state.
- Pure components handle rendering.
- Keep presentation components and container logic separate.
- UI components should not directly couple API, routing, caching, modal, or analytics responsibilities.

### 2.4 Minimize Interfaces

- Keep props small; do not pass a "large state object".
- Do not pass an entire page-level large state into a child component; children should receive the minimum props.
- Children should depend only on the data and callbacks they actually need. Do not send the whole page result just for convenience.

## 3. File and Naming Conventions

### 3.1 Component Files

- Each file should export only one main component.
- A file should export only one main component.
- A file should define only one main component.
- The component file name and component name should match.
- File names should follow the project'"'"'s existing naming style; for React components, the file name should clearly reflect the component responsibility.

### 3.2 Same-File Helper Components

- Up to 1 to 3 small helper components used only by the current component may live in the same file.
- Such helpers are allowed only when they are tightly coupled to the main component and not reusable.
- If a helper component starts to be reused by multiple files, it must be promoted to its own file.
- If a helper component has its own state, standalone testing value, or its own styling semantics, split it out.

### 3.3 Hook Files

- A Hook file should preferably export only one main Hook.
- The file name should match the Hook name, for example `use-user-profile.ts` for `useUserProfile`.
- Small internal helpers tightly coupled to the Hook may live in the same file; general-purpose utilities must move to `lib/` or `utils/`.

## 4. Component Responsibility Boundaries

### 4.1 Presentation Components

- Only render and handle light interaction.
- Do not send requests directly.
- Do not depend on route navigation directly.
- Do not manipulate cache directly.
- Do not decide complex business flows directly.

### 4.2 Container Components / Page Orchestration Components

- Assemble page structure.
- Call business Hooks.
- Coordinate data flow between child components.
- Handle route, query parameter, cache refresh, modal orchestration, and other page-level behaviors.

## 5. Props Design Standards

### 5.1 Minimum Props Principle

- Props should not exceed 8.
- If props exceed 8, evaluate whether the responsibility is too broad or the boundary is unclear.
- Prefer explicit fields and explicit behaviors; do not pass vague objects.

### 5.2 When Passing Objects Is Allowed

- Domain objects may be passed, such as `conversation`, `message`, or `user`.
- Do not pass the full return value of a page-level Hook or a universal state bundle.

## 6. Complexity Control

### 6.1 Component Length

- One component should ideally be under 100 lines.
- Components over 150 lines must be evaluated for splitting.

### 6.2 Function Length

- One function should ideally be under 30 lines.
- Functions over 50 lines must be evaluated for splitting.

### 6.3 Hook Complexity

- One Hook should not cover more than 3 concerns.

### 6.4 JSX Nesting Depth

- JSX nesting should not exceed 3 levels.

## 7. Branching and Pattern Expansion Standards

### 7.1 if/else Control

- When pattern branches exceed 3 `if/else` branches, prefer a strategy mapping.

### 7.2 New Pattern Integration

- New patterns should be added through new strategies whenever possible, rather than changing multiple old branches.

## 8. Split Suggestions for Hooks, Utils, and Components

### 8.1 When to Extract a Hook

- State management logic is used by multiple components.
- The component contains long side effects or event orchestration.
- The state flow needs separate testing.

### 8.2 When to Extract utils / lib

- Pure functions.
- Logic unrelated to the React lifecycle.
- Logic that needs to be reused across components.

### 8.3 When to Split Child Components

- JSX nesting is too deep.
- Conditional rendering blocks are long.
- List item structures are complex.

## 9. Recommended Layering

1. Page component: route entry, page layout, and module assembly.
2. Page orchestration Hook: aggregate business Hooks, but do not output an unbounded large object.
3. Business Hook: a single business workflow.
4. Presentation component: consumes only minimum props.
5. Shared UI component: no business semantics.
6. `lib/utils`: pure functions and stateless helper logic.

## 10. Biome Coordination

- Biome handles formatting, basic readability, and some complexity hints.
- Responsibility boundaries, prop width, and God Components / God Hooks still require manual review.

## 11. Code Review Checklist

- Does the file export only one main component?
- Do the component file name and component name match?
- Is there mixed responsibility?
- Does the Hook cover more than 3 concerns?
- Do props exceed 8?
- Is a page-level large state passed directly to children?
- Are there more than 3 pattern branches?
- Is JSX nesting too deep?

## 12. Exception Rules

- A pure presentation component may be a little long if its responsibility is stable.
- There may be a few helper components in the same file if they only serve the main component.
- A page entry file may be a little long if the business logic has already been split into Hooks.

## 13. Implementation Suggestions

- Before adding new features, decide whether they belong in a page component, business Hook, presentation component, or utility function.
- When a component or Hook has multiple change drivers, split the boundaries before adding more features.

## 14. One-Sentence Summary

- Pages assemble, Hooks manage state, components render, and utility functions handle pure logic.
