#!/usr/bin/env python3
"""
Web Scraper CLI — Part of the Large File Protocol Skill

Fetches full page content from URLs using Playwright (headless Chromium),
extracts main article content via readability-lxml, converts to clean
markdown via html2text, and stores results with YAML frontmatter for
downstream LFP processing.

Usage:
    python web_scraper.py --urls URL1 URL2 URL3 --output scraped_content/
    python web_scraper.py --urls-file urls.txt --output scraped_content/
    python web_scraper.py --urls URL1 --output scraped_content/ --delay 5

Deduplication: reads existing manifest.json in output dir, skips already-scraped URLs.
"""

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from html2text import HTML2Text
from playwright.sync_api import sync_playwright
from readability import Document


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_DELAY = 2
DEFAULT_TIMEOUT = 30000
MANIFEST_FILENAME = "manifest.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str, max_len: int = 60) -> str:
    """Convert arbitrary text into a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:max_len]


def content_hash(text: str) -> str:
    """SHA-256 hash of extracted content for deduplication."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_manifest(output_dir: Path) -> dict:
    """Load existing manifest or return empty structure."""
    manifest_path = output_dir / MANIFEST_FILENAME
    if manifest_path.exists():
        try:
            return json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"scraped_urls": {}}
    return {"scraped_urls": {}}


def save_manifest(output_dir: Path, manifest: dict) -> None:
    """Persist manifest to disk."""
    manifest_path = output_dir / MANIFEST_FILENAME
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def make_filename(url: str, title: str) -> str:
    """Generate a deterministic filename from domain + title slug."""
    parsed = urlparse(url)
    domain = slugify(parsed.netloc.replace("www.", ""))
    title_slug = slugify(title) if title else slugify(parsed.path.strip("/"))
    return f"{domain}-{title_slug}.md"


def format_frontmatter(url: str, title: str, domain: str, word_count: int) -> str:
    """Produce YAML frontmatter block."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        f"---\n"
        f"url: {url}\n"
        f"title: \"{title}\"\n"
        f"domain: {domain}\n"
        f"scraped_at: {now}\n"
        f"word_count: {word_count}\n"
        f"---\n\n"
    )


# ---------------------------------------------------------------------------
# Core scraping
# ---------------------------------------------------------------------------

def scrape_url(page, url: str, user_agent: str) -> dict | None:
    """
    Navigate to *url*, extract main content, return metadata + markdown.
    Returns None on failure.
    """
    try:
        page.set_extra_http_headers({"User-Agent": user_agent})
        response = page.goto(url, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)

        if response and response.status >= 400:
            print(f"  [HTTP {response.status}] {url}", file=sys.stderr)
            return None

        html = page.content()
        if not html or len(html) < 200:
            print(f"  [EMPTY PAGE] {url}", file=sys.stderr)
            return None

        # readability extraction
        doc = Document(html)
        title = doc.title() or page.title() or ""
        article_html = doc.summary()

        # Check for empty extraction
        soup = BeautifulSoup(article_html, "lxml")
        text_preview = soup.get_text(strip=True)
        if len(text_preview) < 50:
            print(f"  [CONTENT TOO SHORT] {url} ({len(text_preview)} chars)", file=sys.stderr)
            return None

        # Convert to markdown
        h = HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.body_width = 0  # no line wrapping
        markdown = h.handle(article_html)

        # Clean up excessive blank lines
        markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

        word_count = len(markdown.split())
        domain = urlparse(url).netloc.replace("www.", "")

        return {
            "url": url,
            "title": title.strip(),
            "domain": domain,
            "markdown": markdown,
            "word_count": word_count,
        }

    except Exception as e:
        print(f"  [ERROR] {url}: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Web Scraper CLI — fetches full page content for LFP wiki processing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--urls",
        nargs="+",
        help="Space-separated list of URLs to scrape.",
    )
    parser.add_argument(
        "--urls-file",
        type=str,
        help="Path to a text file with one URL per line.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory for scraped markdown files.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help=f"Seconds between requests (default: {DEFAULT_DELAY}).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-scrape even if URL already exists in manifest.",
    )

    args = parser.parse_args()

    # Collect URLs
    urls = []
    if args.urls:
        urls.extend(args.urls)
    if args.urls_file:
        urls_file = Path(args.urls_file)
        if not urls_file.exists():
            print(f"ERROR: URLs file not found: {args.urls_file}", file=sys.stderr)
            sys.exit(1)
        urls.extend(
            line.strip()
            for line in urls_file.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        )

    if not urls:
        print("ERROR: No URLs provided. Use --urls or --urls-file.", file=sys.stderr)
        sys.exit(1)

    # Prepare output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load manifest for deduplication
    manifest = load_manifest(output_dir)
    scraped_urls = manifest.get("scraped_urls", {})

    # Filter already-scraped URLs
    urls_to_scrape = []
    for url in urls:
        if url in scraped_urls and not args.force:
            print(f"  [SKIP] Already scraped: {url}")
        else:
            urls_to_scrape.append(url)

    if not urls_to_scrape:
        print("All URLs already scraped. Use --force to re-scrape.")
        sys.exit(0)

    print(f"Scraping {len(urls_to_scrape)} URL(s) to {output_dir}/")

    # Initialize browser
    ua = UserAgent()
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for i, url in enumerate(urls_to_scrape):
            print(f"  [{i + 1}/{len(urls_to_scrape)}] {url}")
            user_agent = ua.random

            result = scrape_url(page, url, user_agent)

            if result is None:
                print(f"    FAILED — skipping", file=sys.stderr)
                continue

            # Generate filename and write
            filename = make_filename(url, result["title"])
            filepath = output_dir / filename

            content = format_frontmatter(
                url=result["url"],
                title=result["title"],
                domain=result["domain"],
                word_count=result["word_count"],
            ) + result["markdown"]

            filepath.write_text(content, encoding="utf-8")

            # Update manifest
            scraped_urls[url] = {
                "file_path": filename,
                "scraped_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "content_hash": content_hash(result["markdown"]),
                "page_title": result["title"],
                "word_count": result["word_count"],
            }

            results.append({
                "url": url,
                "filename": filename,
                "word_count": result["word_count"],
                "title": result["title"],
            })

            print(f"    OK — {result['word_count']} words -> {filename}")

            # Rate limiting
            if i < len(urls_to_scrape) - 1:
                time.sleep(args.delay)

        browser.close()

    # Save updated manifest
    manifest["scraped_urls"] = scraped_urls
    save_manifest(output_dir, manifest)

    # Summary
    print(f"\nDone. {len(results)}/{len(urls_to_scrape)} scraped successfully.")
    print(f"Output: {output_dir}/")
    for r in results:
        print(f"  {r['filename']} ({r['word_count']} words)")


if __name__ == "__main__":
    main()
