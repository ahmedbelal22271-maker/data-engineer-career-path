# Frontend Generation Architecture: Robust HTML/CSS for Automated Workers

## Core Principle: Decide Layout Strategy Before Writing Any CSS

The single most common source of layout bugs in automated generation is picking a layout primitive (Grid, Flexbox, or block/float) reactively, line by line, rather than deciding the overall structure upfront. Before writing markup, classify the component:

- **One-dimensional arrangement** (a row of nav items, a vertical stack of cards, a toolbar) → **Flexbox**.
- **Two-dimensional arrangement** (a dashboard with rows AND columns that need to align against each other, a photo gallery, a page-level layout with header/sidebar/content/footer) → **Grid**.
- **Document-flow content** (article text, prose with inline images) → normal block flow; don't force Flexbox/Grid onto content that's fundamentally just flowing text.

### The Decision Test
Ask: "Do I need items in this container to align with items in a *different* container along the same axis?" If yes (e.g., card headers across a row of cards should align even though card bodies have different heights), Grid's explicit track system handles this natively. Flexbox can approximate it but requires fighting `flex-basis` math; Grid's `grid-template-columns`/`subgrid` is the correct tool. If no — if it's purely "arrange these children in a single row or column, distribute space" — Flexbox is simpler and sufficient.

### Never mix layout systems on the same axis without a reason
Nesting Flexbox inside Grid inside Flexbox is fine *when each layer has a clear, distinct job* (e.g., Grid for the page skeleton, Flexbox for the toolbar inside one grid cell). It becomes a bug magnet when the same alignment problem is solved redundantly at multiple nesting levels (e.g., centering content with both a flex `justify-content: center` on the parent AND `margin: auto` on the child) — pick exactly one mechanism per alignment decision.

## Step 1: Establish the Box-Sizing Baseline First

Before any component-specific CSS, set a global reset that prevents the single most common source of "my widths don't add up" bugs:

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

Without this, `width: 100%` plus any `padding`/`border` overflows the intended size — a bug that looks like a layout engine problem but is actually a box-model default problem. Set this once, globally, before writing any other rule.

## Step 2: Prevent Collapse Bugs at the Container Level

### Flex/Grid containers collapsing to zero height
A container with `display: flex` or `display: grid` whose children have no intrinsic height (e.g., empty divs awaiting dynamic content, or images that haven't loaded yet) will collapse. Always give containers an explicit `min-height` when their content is dynamic/loaded asynchronously, rather than relying on content to define height:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  min-height: 200px; /* prevents collapse before content loads */
  gap: 1rem;
}
```

### `auto-fit` vs `auto-fill` — pick deliberately, not by habit
`auto-fit` collapses empty tracks to take up no space (good for galleries where you want remaining items to stretch to fill the row). `auto-fill` keeps empty track slots reserved (good when you want consistent column width regardless of item count, e.g., a calendar grid). Using the wrong one is a frequent source of "why is my last row stretched weirdly" bugs.

### Flex children overflowing their container despite `flex-shrink`
By default, flex items have `min-width: auto`, which means they refuse to shrink below their *content's* intrinsic size (e.g., a long unbroken string or a fixed-width image) even with `flex-shrink: 1` set. This is the single most common cause of flex children overflowing their container on narrow viewports. Fix explicitly:

```css
.flex-item {
  min-width: 0; /* allows shrinking below content's intrinsic size */
  overflow-wrap: break-word; /* or overflow: hidden, depending on intent */
}
```

The equivalent rule for Grid items is `min-width: 0` on the grid item, or `minmax(0, 1fr)` instead of bare `1fr` in the track definition — bare `1fr` tracks have the same intrinsic-content-size floor problem.

## Step 3: Responsive Strategy — Build Fluid First, Add Breakpoints Second

### Default to intrinsically responsive patterns before reaching for media queries
Many "responsive" bugs come from over-relying on fixed breakpoints when a fluid technique would adapt automatically with zero breakpoints needed:

- `grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))` reflows column count automatically as width changes — no media query required for the common "N columns that wrap based on available space" pattern.
- `clamp(1rem, 2vw + 0.5rem, 1.5rem)` for font sizes scales fluidly between a minimum and maximum instead of jumping at fixed breakpoints.
- `aspect-ratio: 16 / 9` (rather than a fixed height) keeps media elements proportional across all widths without separate rules per breakpoint.

### When breakpoints are genuinely needed, choose them from content, not devices
Don't hardcode breakpoints to "iPhone width" / "iPad width" — device sizes change constantly and this couples your CSS to a moving target. Instead, identify the actual width at which *this specific layout* starts to look broken (e.g., "at narrower than 600px, this 3-column grid's columns become too narrow to read") and set the breakpoint there, verified programmatically (see Step 5).

### Mobile-first ordering prevents override fights
Write base styles for the narrowest viewport, then use `min-width` media queries to progressively enhance for wider viewports — not the reverse. `max-width`-based "mobile overrides" on top of desktop-first base styles tend to accumulate specificity conflicts and `!important` patches as the component evolves; mobile-first additive scaling avoids that by construction.

```css
.toolbar { display: flex; flex-direction: column; } /* mobile default */

@media (min-width: 768px) {
  .toolbar { flex-direction: row; }
}
```

## Step 4: Z-Index and Stacking Context Discipline

Z-index collisions are rarely "wrong number chosen" — they're usually a **stacking context** misunderstanding. A `z-index` value only competes with other z-indexes within the *same* stacking context; a child with `z-index: 9999` inside a parent that itself has a low z-index (or any property that creates a new stacking context, like `transform`, `opacity < 1`, or `filter`) will still render behind a sibling subtree with a higher-positioned stacking context, regardless of the child's own z-index value.

- Maintain a single, deliberate z-index scale for the whole project (e.g., a fixed set: `--z-dropdown: 100; --z-modal: 200; --z-toast: 300;`) rather than ad hoc numbers chosen per component — ad hoc escalating z-index values ("let's make this 9999 to be safe") are the direct cause of most z-index bugs, since the next component author does the same thing and now nothing has a stable order.
- Before debugging "why won't this appear on top," check the entire ancestor chain for properties that create new stacking contexts — the fix is very often in an ancestor, not in the element with the z-index rule itself.

## Step 5: Programmatic Verification Before Shipping

Since the worker can't visually inspect rendered output by eye, verify computed layout programmatically (via a headless browser controlling a real layout engine) rather than just reviewing the CSS source text:

- Check computed `width`/`height` of key containers at multiple viewport widths — assert non-zero, assert within expected bounds.
- Check for unintended overlap between elements that should be visually distinct (bounding-box intersection tests).
- Check computed `overflow` behavior — does content actually fit, or is it being silently clipped/hidden?
- Sweep at least 3-4 representative breakpoints (e.g., 375px, 768px, 1024px, 1440px), not just the viewport the component happened to be written against.

CSS source code reading alone cannot catch these classes of bugs — `flex: 1` and `grid-template-columns: 1fr 1fr` are only meaningful once resolved against actual content, which requires running an actual layout engine.

## Common Failure Patterns Checklist

| Symptom | Likely Cause |
|---|---|
| Content overflows its flex/grid container on narrow screens | Missing `min-width: 0` on flex/grid items |
| Last row of a grid stretches unexpectedly | `auto-fill` used where `auto-fit` was intended (or vice versa) |
| Element with high z-index still renders behind another | A `transform`/`opacity`/`filter` on an ancestor created a new stacking context |
| Container collapses to zero height before content loads | No explicit `min-height` on a container relying on dynamic content for sizing |
| Widths don't add up to 100% as expected | Missing global `box-sizing: border-box` reset |
| Layout looks fine at common breakpoints but breaks at unusual widths | Breakpoints chosen by device guess rather than verified by sweeping a continuous range of widths |
