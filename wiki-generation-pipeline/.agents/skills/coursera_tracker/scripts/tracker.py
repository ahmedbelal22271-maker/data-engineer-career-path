"""Core CourseraTracker class for local-first course progress management.

All operations respect robots.txt constraints. No restricted endpoints
are accessed. Progress is stored locally in JSON files.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

from .safety import RobotsTxtGuard
from .schema import (
    CourseMetadata,
    CourseRecord,
    ModuleRecord,
    ModuleStatus,
    ProgressReport,
)

logger = logging.getLogger(__name__)

_BASE_URL = "https://www.coursera.org"
_DATA_DIR = Path(__file__).parent.parent / "data"
_PROGRESS_FILE = "progress.json"


class CourseraTracker:
    """Local-first Coursera course progress tracker.

    Tracks completion across multiple courses using only publicly
    accessible course pages. All web access is validated against
    Coursera's robots.txt before execution.

    Usage::

        tracker = CourseraTracker()
        tracker.register_course("machine-learning", ["Linear Regression", "NN"])
        tracker.update_status("machine-learning", "Linear Regression", "completed")
        report = tracker.fetch_progress("machine-learning")
    """

    def __init__(self, data_dir: Optional[str | Path] = None) -> None:
        """Initialize the tracker.

        Args:
            data_dir: Directory for persisting progress data.
                      Defaults to ``<skill>/data/``.
        """
        self._data_dir = Path(data_dir) if data_dir else _DATA_DIR
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._progress_path = self._data_dir / _PROGRESS_FILE
        self._guard = RobotsTxtGuard()
        self._courses: dict[str, CourseRecord] = {}
        self._load_state()

    # ── State persistence ────────────────────────────────────────────

    def _load_state(self) -> None:
        """Load progress state from disk."""
        if not self._progress_path.exists():
            self._courses = {}
            return

        try:
            raw = json.loads(self._progress_path.read_text(encoding="utf-8"))
            self._courses = {
                slug: CourseRecord.from_dict(data)
                for slug, data in raw.get("courses", {}).items()
            }
        except (json.JSONDecodeError, KeyError, OSError) as exc:
            logger.warning("Failed to load progress state: %s — starting fresh", exc)
            self._courses = {}

    def _save_state(self) -> None:
        """Persist progress state to disk."""
        payload = {
            "version": 1,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "courses": {slug: record.to_dict() for slug, record in self._courses.items()},
        }
        self._progress_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # ── Safety ───────────────────────────────────────────────────────

    def validate_access(self, url: str) -> bool:
        """Validate a URL against Coursera's robots.txt for ClaudeBot.

        Args:
            url: Full URL to check.

        Returns:
            True if allowed, False if blocked.

        Raises:
            ValueError: If URL is not a Coursera URL.
        """
        return self._guard.validate(url)

    # ── Public metadata (allowed by robots.txt) ──────────────────────

    def get_fetch_url(self, course_slug: str) -> str:
        """Return the public URL for a course page (safe to fetch with webfetch).

        Args:
            course_slug: The course slug (e.g., ``"machine-learning"``).

        Returns:
            The full URL to fetch.

        Raises:
            PermissionError: If the URL is blocked by robots.txt.
        """
        url = f"{_BASE_URL}/learn/{course_slug}"
        if not self.validate_access(url):
            raise PermissionError(
                f"ACCESS DENIED: {url} is blocked by Coursera's robots.txt. "
                "Cannot fetch course metadata from restricted paths."
            )
        return url

    def fetch_public_metadata(
        self, course_slug: str, html: Optional[str] = None
    ) -> CourseMetadata:
        """Fetch course metadata from the public ``/learn/{slug}`` page.

        Only accesses publicly allowed paths. No authentication required.

        Args:
            course_slug: The course slug (e.g., ``"machine-learning"``).
            html: Optional raw HTML from the page. If provided, modules are
                  parsed from this HTML. If None, returns a stub with the
                  URL for the agent to fetch.

        Returns:
            CourseMetadata with title, description, and module list.

        Raises:
            PermissionError: If the URL is blocked by robots.txt.
        """
        url = f"{_BASE_URL}/learn/{course_slug}"
        if not self.validate_access(url):
            raise PermissionError(
                f"ACCESS DENIED: {url} is blocked by Coursera's robots.txt. "
                "Cannot fetch course metadata from restricted paths."
            )

        logger.info("Fetching public metadata for %s", course_slug)

        if html is not None:
            modules = self.extract_modules_from_html(html)
            # Try to extract title from HTML
            title_match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else course_slug.replace("-", " ").title()
            # Clean title (remove " | Coursera" suffix)
            title = re.sub(r"\s*\|\s*Coursera\s*$", "", title, flags=re.IGNORECASE)
            # Try to extract description
            desc_match = re.search(
                r'<meta\s+name="description"\s+content="([^"]+)"', html, re.IGNORECASE
            )
            description = desc_match.group(1).strip() if desc_match else ""
            return CourseMetadata(
                slug=course_slug,
                title=title,
                url=url,
                description=description,
                modules=modules,
            )

        # No HTML provided — return stub for agent to fetch
        return CourseMetadata(
            slug=course_slug,
            title=course_slug.replace("-", " ").title(),
            url=url,
            description="(fetch from /learn/{slug} page)",
            modules=[],
        )

    def extract_modules_from_html(self, html: str) -> list[str]:
        """Extract module names from a Coursera course page HTML.

        Looks for common patterns in the course syllabus section.

        Args:
            html: Raw HTML from a ``/learn/{slug}`` page.

        Returns:
            List of module/week names found.
        """
        modules: list[str] = []

        # Pattern 1: Week/module headings
        week_pattern = re.compile(
            r'<(?:h[23]|span)[^>]*>\s*(?:Week\s+\d+|Module\s+\d+)[^<]*</(?:h[23]|span)>',
            re.IGNORECASE,
        )
        for match in week_pattern.finditer(html):
            text = re.sub(r"<[^>]+>", "", match.group()).strip()
            if text and text not in modules:
                modules.append(text)

        # Pattern 2: Syllabus list items
        syllabus_pattern = re.compile(
            r'<(?:li|div)[^>]*class="[^"]*syllabus[^"]*"[^>]*>([^<]+)</(?:li|div)>',
            re.IGNORECASE,
        )
        for match in syllabus_pattern.finditer(html):
            text = match.group(1).strip()
            if text and text not in modules:
                modules.append(text)

        return modules

    # ── Course management ────────────────────────────────────────────

    def register_course(
        self,
        course_slug: str,
        title: str = "",
        modules: Optional[list[str]] = None,
        description: str = "",
        provider: str = "",
    ) -> CourseRecord:
        """Register a course for tracking.

        If the course is already registered, updates its metadata
        and adds any new modules.

        Args:
            course_slug: Unique course identifier (URL slug).
            title: Course display name. Defaults to slug-derived title.
            modules: List of module names. If None, attempts to fetch.
            description: Course description.
            provider: Course provider/university name.

        Returns:
            The CourseRecord for this course.
        """
        if course_slug in self._courses:
            record = self._courses[course_slug]
            if modules:
                for mod in modules:
                    if mod not in record.modules:
                        record.modules[mod] = ModuleRecord()
            self._save_state()
            return record

        if not title:
            title = course_slug.replace("-", " ").title()

        record = CourseRecord(
            slug=course_slug,
            title=title,
            description=description,
            provider=provider,
            url=f"{_BASE_URL}/learn/{course_slug}",
        )

        if modules:
            for mod in modules:
                record.modules[mod] = ModuleRecord()

        self._courses[course_slug] = record
        self._save_state()
        logger.info("Registered course: %s (%d modules)", title, len(modules or []))
        return record

    def unregister_course(self, course_slug: str) -> bool:
        """Remove a course from tracking.

        Args:
            course_slug: The course to remove.

        Returns:
            True if the course was removed, False if not found.
        """
        if course_slug in self._courses:
            del self._courses[course_slug]
            self._save_state()
            logger.info("Unregistered course: %s", course_slug)
            return True
        return False

    def list_courses(self) -> list[str]:
        """List all registered course slugs."""
        return list(self._courses.keys())

    # ── Progress tracking ────────────────────────────────────────────

    def update_status(
        self,
        course_slug: str,
        module: str,
        status: str,
        notes: str = "",
        score: Optional[float] = None,
    ) -> None:
        """Update the status of a specific module.

        Args:
            course_slug: Course identifier.
            module: Module name (must match exactly).
            status: New status — one of: pending, in_progress, completed, skipped.
            notes: Optional notes about this module.
            score: Optional numeric score (0-100).

        Raises:
            KeyError: If course or module not found.
            ValueError: If status is invalid.
        """
        if course_slug not in self._courses:
            raise KeyError(f"Course not registered: {course_slug}")

        record = self._courses[course_slug]
        if module not in record.modules:
            raise KeyError(
                f"Module '{module}' not found in course '{course_slug}'. "
                f"Available modules: {list(record.modules.keys())}"
            )

        try:
            new_status = ModuleStatus(status)
        except ValueError:
            raise ValueError(
                f"Invalid status '{status}'. Must be one of: "
                f"{[s.value for s in ModuleStatus]}"
            )

        mod = record.modules[module]
        mod.status = new_status

        if new_status == ModuleStatus.COMPLETED:
            mod.completed_at = datetime.now(timezone.utc).isoformat()
            if notes:
                mod.notes = notes
            if score is not None:
                mod.score = score
        elif notes:
            mod.notes = notes

        self._save_state()
        logger.info(
            "Updated %s/%s → %s", course_slug, module, new_status.value
        )

    def fetch_progress(
        self, course_slug: Optional[str] = None
    ) -> ProgressReport | list[ProgressReport]:
        """Get current progress for a course or all courses.

        Args:
            course_slug: Specific course, or None for all courses.

        Returns:
            A single ProgressReport if course_slug given,
            or a list of ProgressReports for all courses.
        """
        if course_slug:
            if course_slug not in self._courses:
                raise KeyError(f"Course not registered: {course_slug}")
            return self._build_report(course_slug)

        return [self._build_report(slug) for slug in self._courses]

    def _build_report(self, course_slug: str) -> ProgressReport:
        """Build a ProgressReport for a single course."""
        record = self._courses[course_slug]
        return ProgressReport(
            course_slug=record.slug,
            title=record.title,
            total_modules=record.total_modules,
            completed=record.completed_count,
            in_progress=record.in_progress_count,
            pending=record.pending_count,
            skipped=sum(
                1 for m in record.modules.values()
                if m.status == ModuleStatus.SKIPPED
            ),
            completion_pct=record.completion_pct,
            next_modules=record.next_modules(),
        )

    def suggest_next(self, course_slug: str, limit: int = 3) -> list[str]:
        """Suggest the next modules to work on.

        Args:
            course_slug: Course to get suggestions for.
            limit: Maximum number of suggestions.

        Returns:
            List of module names to work on next.

        Raises:
            KeyError: If course not found.
        """
        if course_slug not in self._courses:
            raise KeyError(f"Course not registered: {course_slug}")
        return self._courses[course_slug].next_modules(limit)

    def add_notes(
        self, course_slug: str, module: str, notes: str
    ) -> None:
        """Add notes to a module without changing its status.

        Args:
            course_slug: Course identifier.
            module: Module name.
            notes: Notes to append.
        """
        if course_slug not in self._courses:
            raise KeyError(f"Course not registered: {course_slug}")
        record = self._courses[course_slug]
        if module not in record.modules:
            raise KeyError(f"Module '{module}' not found in '{course_slug}'")
        existing = record.modules[module].notes
        if existing:
            record.modules[module].notes = f"{existing}\n{notes}"
        else:
            record.modules[module].notes = notes
        self._save_state()

    # ── Reporting ────────────────────────────────────────────────────

    def export_report(self) -> str:
        """Generate a Markdown progress report for all tracked courses.

        Returns:
            Markdown string with progress summary for every course.
        """
        if not self._courses:
            return "# Coursera Progress Report\n\nNo courses registered yet.\n"

        sections = ["# Coursera Progress Report\n"]
        sections.append(
            f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*\n"
        )

        total_completed = 0
        total_modules = 0

        for slug, record in self._courses.items():
            report = self._build_report(slug)
            sections.append(report.to_markdown())
            sections.append("")
            total_completed += report.completed
            total_modules += report.total_modules

        if total_modules > 0:
            overall_pct = round((total_completed / total_modules) * 100, 1)
            sections.append("---")
            sections.append(
                f"**Overall:** {total_completed}/{total_modules} modules "
                f"({overall_pct}%) across {len(self._courses)} courses"
            )

        return "\n".join(sections)

    def export_json(self) -> str:
        """Export all progress data as a formatted JSON string."""
        payload = {
            "version": 1,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "courses": {
                slug: record.to_dict()
                for slug, record in self._courses.items()
            },
        }
        return json.dumps(payload, indent=2, ensure_ascii=False)
