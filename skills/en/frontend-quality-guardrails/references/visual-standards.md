# Visual Standards

Use this reference when creating, redesigning, or polishing UI. The goal is not decoration; it is clear hierarchy, stable layout, readable content, and a product surface that feels intentional.

## Contents

- Visual Hierarchy
- Density
- Color
- Typography
- Spacing
- Borders, Radius, And Shadows
- Icons
- Layout Composition
- Interaction States
- Motion
- Common Style Failures
- Finish Criteria

## Visual Hierarchy

- Make the primary task visually obvious within the first viewport.
- Use one dominant heading level per surface; avoid multiple elements competing as the page title.
- Use spacing and grouping before adding borders, shadows, or background fills.
- Keep secondary metadata visually quieter than titles and actions.
- Do not use hero-scale type inside dashboards, tables, sidebars, cards, modals, or toolbars.
- Keep action hierarchy clear: primary, secondary, tertiary, destructive, disabled.

## Density

- Match density to product type. SaaS/admin tools should be compact, scannable, and calm; marketing pages can breathe more.
- Avoid oversized cards for small amounts of operational data.
- Avoid large decorative whitespace that pushes key workflows below the fold.
- Keep repeated rows/cards consistent so users can scan quickly.
- Use progressive disclosure for advanced controls rather than crowding the first screen.

## Color

- Use existing tokens first.
- Limit accent colors; one primary accent plus semantic colors is usually enough.
- Do not communicate status by color alone; pair with text/icon/shape.
- Check muted text contrast on real backgrounds, not only white.
- Avoid one-note palettes where every surface is a tint of the same hue.
- Keep destructive colors reserved for destructive or dangerous actions.
- Avoid gradients unless the product style already uses them or the surface is explicitly editorial/marketing.

## Typography

- Keep a clear scale: page title, section title, body, metadata, caption.
- Do not use negative letter spacing.
- Do not use viewport-width-driven font sizes.
- Keep line length readable: long prose should not span the full desktop width.
- Use tabular numerals for dashboards, financial values, timers, and comparable numeric columns.
- Prefer sentence case unless the existing product style uses title case.
- Avoid all-caps labels for long strings; they become harder to scan and localize.

## Spacing

- Use the project's spacing scale.
- Keep related elements close and unrelated groups farther apart.
- Align vertical edges across sections, forms, cards, and tables.
- Keep toolbar control gaps consistent.
- Avoid stacking multiple containers each with large padding; nested padding makes cramped content look accidental.
- Do not solve alignment by hand-tuned one-off margins when layout primitives can express it.

## Borders, Radius, And Shadows

- Use radius consistently by component type.
- Avoid nested cards with competing borders/shadows.
- Use shadows for elevation, not decoration.
- Keep borders subtle but visible enough to define dense data regions.
- Avoid hover borders that change size; use existing border width with transparent idle color.
- Do not mix many radius values in the same control group.

## Icons

- Use the project's icon library.
- Keep icon size and stroke weight consistent within a toolbar or list.
- Use `aria-hidden` for decorative icons and accessible labels for icon-only buttons.
- Do not replace clear text with unfamiliar icons unless tooltip/label support exists.
- Align icons optically with text, not just mathematically.

## Layout Composition

- Keep page sections full-width or naturally grouped; do not put whole pages inside floating cards unless the product pattern requires it.
- Avoid cards inside cards.
- Use grids when comparing similar items; use lists/tables when scanning many records.
- Keep sidebars and filters from stealing space from primary content at small widths.
- Let important content, not decoration, occupy the largest visual area.
- Make responsive changes intentional: stack, collapse, scroll, or hide with a substitute path.

## Interaction States

- Design idle, hover, active, focus, disabled, loading, selected, error, warning, success, empty, and skeleton states.
- Keep state changes from resizing the component.
- Ensure focus styles are visible against all state backgrounds.
- Ensure disabled controls still explain unavailable actions when the reason is not obvious.
- Make selected state stronger than hover state.
- Keep loading indicators close to the content/action they affect.

## Motion

- Use motion to clarify cause and effect, not as decoration.
- Prefer transform and opacity.
- Keep durations short for operational UI.
- Respect reduced motion.
- Avoid animating repeated table rows or dense list items unless the product pattern demands it.

## Common Style Failures

- Text too large for compact controls.
- Metadata louder than primary content.
- Too many borders plus shadows.
- Low-contrast gray text on tinted backgrounds.
- Center-aligned dense content.
- Buttons with inconsistent heights.
- Icons that shift text baseline.
- Badges that dominate titles.
- Empty states that look like errors.
- Skeletons that do not match final content.
- Cards with hover transforms that make the grid jitter.
- Dropdowns and popovers visually disconnected from their trigger.

## Finish Criteria

Before finalizing visual work, confirm:

- The eye lands on the right first action/content.
- Related controls align and share dimensions.
- Text hierarchy is clear without reading every word.
- Long text has a planned behavior.
- The page still works in a dense, real-data scenario.
- No decorative choice harms readability, scanning, or accessibility.
