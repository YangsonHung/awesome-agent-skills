# Browser Verification Workflow

Use this reference after visible frontend changes or when debugging overflow, responsive behavior, visual regressions, or interaction states.

## Contents

- When To Verify In Browser
- Setup
- Viewports
- Adversarial Content
- Screenshot Pass
- DOM And Console Checks
- Interaction Checks
- Automated Assertions When Useful
- Verification Report

## When To Verify In Browser

Verify with a browser when any change affects:

- Layout, spacing, typography, colors, borders, shadows, or responsive behavior.
- Text rendering, truncation, wrapping, tables, cards, forms, navigation, or modals.
- Dropdowns, tooltips, popovers, drawers, dialogs, sticky elements, or portals.
- Loading, error, empty, disabled, hover, focus, selected, expanded, or collapsed states.
- Canvas, SVG, charts, images, video, maps, or animation.

## Setup

1. Start the project using the existing package manager and dev script.
2. Prefer the repo's documented local URL. If the port is busy, use the next available port only if the framework supports it.
3. Open the page in the in-app browser or available browser automation tool.
4. Watch terminal output, browser console, and network errors.
5. Keep the dev server running only while needed for verification.

## Viewports

Check the changed surface at practical sizes:

- `320x700`: smallest common mobile stress case.
- `375x812`: common mobile.
- `768x1024`: tablet.
- `1024x768`: small desktop or tablet landscape.
- `1280x800`: common laptop.
- `1440x900` or wider: desktop spacing.

Use fewer viewports only for very small changes, but always include at least one narrow and one desktop viewport for layout work.

## Adversarial Content

Inject or create test data when possible:

- Long unbroken token.
- Long normal sentence.
- URL with query string.
- Mixed Chinese and English.
- Long translated button/label.
- Many tags/badges.
- Empty value.
- Missing image/avatar.
- Long validation error.
- Large table row count or many list items.

If live data cannot be changed safely, use devtools DOM editing, local mock data, storybook stories, fixtures, or temporary test-only data. Remove temporary data before finishing.

## Screenshot Pass

For each important viewport:

1. Capture a screenshot of the whole changed surface.
2. Inspect for horizontal overflow, clipped text, overlap, accidental scrollbars, layout shifts, and poor alignment.
3. Compare key states if the change affects interaction.
4. Zoom mentally: titles, labels, values, buttons, and errors should remain readable without guessing.

Look specifically at:

- Page edges for content extending beyond viewport.
- Flex rows containing title + metadata + actions.
- Table wrappers and sticky columns.
- Modal headers/footers and body scroll.
- Dropdown/popover position against viewport edges.
- Text baselines next to icons.
- Loading skeleton dimensions versus final content.

## DOM And Console Checks

Use DOM inspection when screenshots are ambiguous:

- Check computed width, `min-width`, `overflow`, `white-space`, `text-overflow`, `word-break`, and `overflow-wrap`.
- Check whether the overflowing node or its parent needs `min-width: 0`.
- Check portal root and z-index when overlays render incorrectly.
- Check accessible names for icon-only controls.
- Check console errors and warnings.
- Check network failures that cause broken loading/error states.

## Interaction Checks

Exercise real workflows:

- Type long input values.
- Trigger validation errors.
- Open and close dropdowns, popovers, drawers, and modals.
- Hover and keyboard-focus controls.
- Select tabs and filters.
- Sort and scroll tables.
- Resize the viewport while the component is open.
- Submit forms in loading and error cases.

## Automated Assertions When Useful

For Playwright or similar tools, prefer simple checks:

- Assert no document-level horizontal overflow:
  `document.documentElement.scrollWidth <= document.documentElement.clientWidth`
- Assert target text container dimensions are within parent bounds.
- Assert key controls are visible and enabled/disabled as expected.
- Assert screenshots for critical responsive surfaces when the project already supports visual testing.

Avoid brittle pixel-perfect tests unless the project already has visual regression infrastructure.

## Verification Report

In the final response, mention:

- Viewports checked.
- Main states checked.
- Browser/console errors found or absence of relevant errors.
- Any state or viewport not verified and why.

Do not claim visual verification if only code inspection was performed.
