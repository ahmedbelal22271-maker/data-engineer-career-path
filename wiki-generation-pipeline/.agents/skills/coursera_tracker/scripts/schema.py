"""Data models for Coursera course tracking.

Pydantic-free schemas using dataclasses for minimal dependency footprint.
All models are JSON-serializable for local state persistence.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional


class ModuleStatus(str, Enum):
    """Completion status for a course module."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


@dataclass
class ModuleRecord:
    """Tracks the state of a single module within a course."""

    status: ModuleStatus = ModuleStatus.PENDING
    notes: str = ""
    score: Optional[float] = None
    registered_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: Optional[str] = None
    time_spent_minutes: float = 0.0

    def mark_completed(self, notes: str = "", score: Optional[float] = None) -> None:
        """Mark this module as completed."""
        self.status = ModuleStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc).isoformat()
        if notes:
            self.notes = notes
        if score is not None:
            self.score = score

    def mark_in_progress(self) -> None:
        """Mark this module as in progress."""
        self.status = ModuleStatus.IN_PROGRESS

    def mark_skipped(self, reason: str = "") -> None:
        """Mark this module as skipped."""
        self.status = ModuleStatus.SKIPPED
        if reason:
            self.notes = reason


@dataclass
class CourseMetadata:
    """Public metadata fetched from a Coursera course page.

    Only contains data from publicly accessible ``/learn/{slug}`` pages.
    No authentication required. No restricted endpoints accessed.
    """

    slug: str
    title: str
    description: str = ""
    provider: str = ""
    modules: list[str] = field(default_factory=list)
    url: str = ""
    fetched_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        """Convert to a plain dict for JSON serialization."""
        return asdict(self)


@dataclass
class CourseRecord:
    """Full tracking record for a single course.

    Contains the course metadata and per-module progress state.
    Stored locally in ``data/progress.json``.
    """

    slug: str
    title: str
    description: str = ""
    provider: str = ""
    url: str = ""
    registered_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    modules: dict[str, ModuleRecord] = field(default_factory=dict)

    @property
    def total_modules(self) -> int:
        """Total number of modules in this course."""
        return len(self.modules)

    @property
    def completed_count(self) -> int:
        """Number of completed modules."""
        return sum(
            1 for m in self.modules.values() if m.status == ModuleStatus.COMPLETED
        )

    @property
    def in_progress_count(self) -> int:
        """Number of modules currently in progress."""
        return sum(
            1 for m in self.modules.values() if m.status == ModuleStatus.IN_PROGRESS
        )

    @property
    def pending_count(self) -> int:
        """Number of modules not yet started."""
        return sum(
            1 for m in self.modules.values() if m.status == ModuleStatus.PENDING
        )

    @property
    def completion_pct(self) -> float:
        """Completion percentage (0.0 to 100.0)."""
        if self.total_modules == 0:
            return 0.0
        return round((self.completed_count / self.total_modules) * 100, 1)

    def next_modules(self, limit: int = 3) -> list[str]:
        """Return the next modules to work on.

        Prioritizes in-progress modules, then pending modules in order.
        """
        in_progress = [
            name for name, m in self.modules.items()
            if m.status == ModuleStatus.IN_PROGRESS
        ]
        pending = [
            name for name, m in self.modules.items()
            if m.status == ModuleStatus.PENDING
        ]
        return (in_progress + pending)[:limit]

    def to_dict(self) -> dict:
        """Convert to a plain dict for JSON serialization."""
        return {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "provider": self.provider,
            "url": self.url,
            "registered_at": self.registered_at,
            "modules": {
                name: {
                    "status": m.status.value,
                    "notes": m.notes,
                    "score": m.score,
                    "registered_at": m.registered_at,
                    "completed_at": m.completed_at,
                    "time_spent_minutes": m.time_spent_minutes,
                }
                for name, m in self.modules.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> CourseRecord:
        """Reconstruct a CourseRecord from a serialized dict."""
        modules = {}
        for name, m_data in data.get("modules", {}).items():
            modules[name] = ModuleRecord(
                status=ModuleStatus(m_data.get("status", "pending")),
                notes=m_data.get("notes", ""),
                score=m_data.get("score"),
                registered_at=m_data.get("registered_at", ""),
                completed_at=m_data.get("completed_at"),
                time_spent_minutes=m_data.get("time_spent_minutes", 0.0),
            )
        return cls(
            slug=data["slug"],
            title=data.get("title", ""),
            description=data.get("description", ""),
            provider=data.get("provider", ""),
            url=data.get("url", ""),
            registered_at=data.get("registered_at", ""),
            modules=modules,
        )


@dataclass
class ProgressReport:
    """Summary of progress across one or all courses."""

    course_slug: str
    title: str
    total_modules: int
    completed: int
    in_progress: int
    pending: int
    skipped: int
    completion_pct: float
    next_modules: list[str]
    courses: Optional[list[dict]] = None

    def to_markdown(self) -> str:
        """Render as a human-readable Markdown report."""
        lines = [f"## {self.title} ({self.course_slug})"]
        lines.append(f"**Progress:** {self.completion_pct}% "
                      f"({self.completed}/{self.total_modules} modules)")
        lines.append("")
        lines.append(f"- Completed: {self.completed}")
        lines.append(f"- In Progress: {self.in_progress}")
        lines.append(f"- Pending: {self.pending}")
        if self.skipped > 0:
            lines.append(f"- Skipped: {self.skipped}")
        lines.append("")
        if self.next_modules:
            lines.append("**Next up:**")
            for mod in self.next_modules:
                lines.append(f"1. {mod}")
        return "\n".join(lines)


@dataclass
class AccessLogEntry:
    """A single access validation log entry."""

    timestamp: str
    url: str
    path: str
    allowed: bool
    reason: str
    user_agent: str = "ClaudeBot"
