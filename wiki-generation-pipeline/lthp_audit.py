"""
LTHP Audit Script — Layer 2 (Detection)

Verifies that lthp-highlight is applied to the correct set of elements in the HTML file.
Usage: python lthp_audit.py <html_file> [--initial-gen]

For initial generation (--initial-gen): expects EVERY .card to carry lthp-highlight.
For subsequent edits (default): expects exactly ONE .lthp-highlight element.

Exits 0 on pass, 1 on fail with descriptive message.
"""

import re
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python lthp_audit.py <html_file> [--initial-gen]")
        sys.exit(1)

    html_file = sys.argv[1]
    initial_gen = "--initial-gen" in sys.argv

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Find content-bearing card elements (exclude .future-card placeholders)
    cards = re.findall(r'<div\s+class="([^"]*card[^"]*)"', html)
    cards = [c for c in cards if 'future-card' not in c]
    card_count = len(cards)

    # Find all elements with lthp-highlight in their class attribute (not in CSS)
    highlighted = re.findall(r'class="[^"]*\blthp-highlight\b[^"]*"', html)
    highlight_count = len(highlighted)

    issues = []

    if initial_gen:
        # Expect ALL cards to be highlighted
        non_highlighted = 0
        for c in cards:
            if 'lthp-highlight' not in c:
                non_highlighted += 1

        if non_highlighted > 0:
            issues.append(
                f"{non_highlighted} of {card_count} .card elements lack lthp-highlight "
                f"(initial gen requires all cards highlighted)"
            )
        if highlight_count == 0:
            issues.append("No lthp-highlight elements found anywhere in the file")
    else:
        # Expect exactly ONE highlighted element
        if highlight_count == 0:
            issues.append("No lthp-highlight elements found — expected exactly 1")
        elif highlight_count > 1:
            issues.append(
                f"Found {highlight_count} lthp-highlight elements — expected exactly 1 "
                f"(only the most recently touched block should be highlighted)"
            )

    # Check that no structural containers carry the highlight
    structural_patterns = [
        r'<section[^>]*lthp-highlight',
        r'<main[^>]*lthp-highlight',
        r'<header[^>]*lthp-highlight',
        r'<footer[^>]*lthp-highlight',
        r'<nav[^>]*lthp-highlight',
        r'<article[^>]*lthp-highlight',
        r'<aside[^>]*lthp-highlight',
    ]
    for pattern in structural_patterns:
        if re.search(pattern, html):
            tag = pattern.split("[^>]*")[0][1:]
            issues.append(f"LTHP BREACH: structural tag <{tag}> carries lthp-highlight")

    if issues:
        print("LTHP AUDIT FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        mode = "initial gen" if initial_gen else "subsequent edit"
        print(f"LTHP AUDIT PASSED ({mode}): {highlight_count} highlight(s) on {card_count} cards, no breaches")
        sys.exit(0)


if __name__ == "__main__":
    main()
