# Frontend Code Review Checklist

Use this reference before modifying or reviewing project UI code. Keep the review surgical: flag concrete defects, fix only the changed surface, and preserve existing patterns.

## Contents

- Review Order
- React And Next.js
- Vue And Nuxt
- Svelte
- HTML And CSS
- Data And Content
- Forms
- Tables And Dense Data
- Component Libraries
- State And Interaction
- Performance Risks
- Review Findings Format

## Review Order

1. Identify the changed user-facing surface.
2. Find the component boundaries, wrappers, design-system primitives, data shape, and CSS source.
3. Trace every dynamic text value into the DOM.
4. Check layout constraints from parent to child, especially flex/grid containers.
5. Check all meaningful states: loading, empty, error, disabled, readonly, focus, hover, selected, expanded, collapsed, and permission-limited.
6. Verify with adversarial text and at least one narrow viewport when feasible.

## React And Next.js

- Check whether text-bearing children inside `flex` or `grid` have `min-w-0`, `flex-1`, `shrink-0`, or equivalent classes in the right places.
- Keep truncation on the text node, not on a high-level row that also contains buttons or badges.
- Avoid unstable layout caused by conditional rendering that inserts/removes wrappers; prefer stable slots where loading/error states share dimensions.
- Do not use array index keys for reorderable, filterable, or dynamic lists.
- Ensure client/server component boundaries in Next.js do not force unnecessary client rendering just for styling.
- Avoid hydration mismatches from browser-only values, dates, random IDs, and viewport-dependent rendering.
- Keep `aria-label`, `title`, tooltip content, and visible labels consistent when truncating.
- Ensure `useEffect` is not used for simple derived display values.
- Keep memoization local and justified; do not add `useMemo`/`useCallback` to hide inefficient structure unless measurable.
- Check that Suspense, skeletons, and loading states preserve final layout dimensions.

## Vue And Nuxt

- Check `v-if`/`v-show` choices: `v-if` can remove layout and focus targets; `v-show` preserves DOM and dimensions.
- Verify `:key` stability in `v-for`.
- Keep computed display strings in `computed`, not repeated inline template expressions when they affect multiple UI locations.
- Ensure scoped CSS does not rely on brittle deep selectors unless component-library APIs are unavailable.
- Check slots with long content; parent components must constrain slot layout.
- Avoid fixed-height containers around translated labels and validation text.
- Ensure SSR/client-only logic does not cause layout shifts in Nuxt.

## Svelte

- Check `{#each}` blocks use stable keys for dynamic lists.
- Ensure reactive declarations do not recompute expensive layout data unnecessarily.
- Keep conditional blocks from replacing focusable elements in ways that lose focus.
- Check slotted content constraints, especially card headers, table cells, and toolbar actions.

## HTML And CSS

- Confirm semantic elements match behavior: `button` for actions, `a` for navigation, `label` for form fields, `table` for tabular data.
- Check that `position: absolute` is not used to patch normal document flow unless the UI is intentionally overlaid.
- Check stacking contexts before adding `z-index`; many overlay bugs come from transformed parents, opacity, filters, or positioned ancestors.
- Verify `overflow: hidden` does not clip focus rings, dropdowns, sticky children, or validation messages.
- Avoid fixed `height` for text-heavy containers; prefer `min-height`, content flow, or internal scroll.
- Ensure global CSS changes are scoped and do not alter unrelated components.
- Check print styles only when the surface is printable.

## Data And Content

- Treat backend content as untrusted for length and formatting.
- Test empty/null/undefined values without rendering `undefined`, `null`, `NaN`, or broken punctuation.
- Avoid concatenating optional fields into awkward strings with dangling separators.
- Format numbers, dates, currency, and percentages consistently with existing utilities.
- Keep raw IDs, URLs, hashes, and file paths copyable when they are operationally important.
- Preserve whitespace only for logs/code/preformatted content, not ordinary labels.

## Forms

- Confirm every input has a visible or accessible label.
- Keep validation messages close to the field and allow them to wrap.
- Check long labels in checkboxes, radios, switches, select options, and segmented controls.
- Preserve browser affordances: autocomplete, input type, required, disabled, readonly, invalid.
- Avoid disabled submit buttons without explaining what blocks submission.
- Ensure async submit states prevent duplicate submission without shifting layout.
- Check that errors returned from APIs do not overflow toast/dialog/form containers.

## Tables And Dense Data

- Decide per column: wrap, truncate, fixed, flexible, sticky, or hidden on small screens.
- Use horizontal scroll at the table wrapper, not the whole page.
- Ensure row actions remain reachable at narrow widths.
- Keep headers aligned with cells after scroll, sticky, or virtualization changes.
- Check virtualization with variable row height if cells can wrap.
- Ensure empty/filter/no-permission states keep table frame coherent.
- Avoid hiding columns that contain required decisions unless there is a detail row or drill-in path.

## Component Libraries

- Prefer project wrapper components before importing raw library primitives.
- Read existing usage nearby; match size, density, variant, tone, and placement.
- Use documented props for ellipsis, tooltip, placement, popup container, scroll, virtualized lists, and status.
- Avoid overriding generated class names or internals unless there is no supported API.
- Check portal containers for dropdowns, popovers, modals, selects, and date pickers.
- Verify overlays inside drawers/modals do not render behind their parent or outside expected clipping.

## State And Interaction

- Check keyboard interaction for every click target.
- Ensure hover-only actions are also discoverable by keyboard and touch users.
- Keep optimistic UI reversible or clearly pending.
- Preserve focus after dialogs close, filters apply, tabs switch, rows expand, or async actions complete.
- Avoid layout shifts when toggling details, sorting, filtering, or validation messages.
- Confirm destructive actions use the project's confirmation pattern.

## Performance Risks

- Avoid rendering huge lists without pagination, virtualization, or lazy loading.
- Avoid measuring layout repeatedly in render loops.
- Debounce expensive search/filter operations when input is large.
- Check image dimensions, lazy loading, and object fit.
- Avoid importing large icon packs or chart libraries for one small visual.
- Ensure CSS animations do not animate `width`, `height`, `top`, `left`, or expensive filters in repeated elements.

## Review Findings Format

When reviewing, lead with defects:

- Severity and short title.
- File and line reference.
- Why it breaks under realistic content or viewport.
- Minimal fix direction.
- Mention missing verification or test gaps after findings.
