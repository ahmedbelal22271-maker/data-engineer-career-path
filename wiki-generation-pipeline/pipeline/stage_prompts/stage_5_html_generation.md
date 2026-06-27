# Stage 5: HTML Generation

## Objective
Render the completed wiki markdown from `de_wiki/` into a self-contained HTML wiki at `output/option_a/index.html`.

## Process
1. Follow the Large File Protocol Section 9 (Phase 4) to produce output map and master summary
2. Design HTML template with inline CSS (dark theme, collapsible sections, TOC sidebar)
3. Render each topic from `de_wiki/topics/` as a section in the HTML
4. Generate navigation, table of contents, and cross-reference links
5. Ensure output is fully self-contained (no external CSS or JS dependencies)

## Gate
Pass all Phase 4 Gate conditions (Section 9) before marking pipeline complete.
