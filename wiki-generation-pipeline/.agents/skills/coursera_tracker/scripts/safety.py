"""robots.txt enforcement layer for Coursera access validation.

Parses Coursera's robots.txt and provides URL validation against
the ClaudeBot user-agent rules. Every web fetch must pass through
validate_access() before execution.
"""

from __future__ import annotations

import json
import re
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

_ROBOTS_PATH = Path(__file__).parent / "robots.txt"
_ACCESS_LOG_PATH = Path(__file__).parent.parent / "data" / "access_log.json"

# Paths explicitly blocked for ClaudeBot per Coursera robots.txt
_BLOCKED_PREFIXES: list[str] = [
    "/api/",
    "/lecture/",
    "/account/",
    "/search",
    "/maestro/",
    "/ui/",
    "/signature/voucher/",
    "/acclaimbadge/",
    "/voucher/",
    "/ent-website/",
    "/learn-perf/",
    "/specializations-perf/",
    "/professional-certificates-perf/",
    "/learn-noperf/",
    "/specializations-noperf/",
    "/professional-certificates-noperf/",
    "/business/xmlrpc.php",
    "/business/wp-content/uploads/",
    "/business/search",
    "/business/teams/search",
    "/organizations/",
]

# Paths explicitly allowed for ClaudeBot
_ALLOWED_PREFIXES: list[str] = [
    "/learn/",
    "/specializations/",
    "/professional-certificates/",
    "/api/utilities/v1/imageproxy",
]


class RobotsTxtGuard:
    """Validates URLs against Coursera's robots.txt rules for ClaudeBot.

    Uses a cached copy of robots.txt. If the cache is stale or missing,
    falls back to the hardcoded block/allow lists extracted from the
    actual robots.txt (fetched 2026-07-13).

    Usage::

        guard = RobotsTxtGuard()
        guard.validate("https://www.coursera.org/learn/machine-learning")  # True
        guard.validate("https://www.coursera.org/api/v1/enrollments")     # False
    """

    _USER_AGENT = "ClaudeBot"

    def __init__(self, robots_path: Optional[Path] = None) -> None:
        self._robots_path = robots_path or _ROBOTS_PATH
        self._blocked_prefixes = _BLOCKED_PREFIXES
        self._allowed_prefixes = _ALLOWED_PREFIXES
        self._parsed = self._load_robots_txt()

    def _load_robots_txt(self) -> dict[str, dict[str, list[str]]]:
        """Parse robots.txt into a structured dict.

        Returns a dict mapping user-agent strings to their
        ``{"Allow": [...], "Disallow": [...]}`` rules.
        Falls back to hardcoded rules if file is missing or unparseable.
        """
        if not self._robots_path.exists():
            logger.warning(
                "robots.txt not found at %s — using hardcoded rules",
                self._robots_path,
            )
            return {}

        try:
            content = self._robots_path.read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("Failed to read robots.txt: %s", exc)
            return {}

        rules: dict[str, dict[str, list[str]]] = {}
        current_agent: Optional[str] = None

        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.lower().startswith("user-agent:"):
                current_agent = line.split(":", 1)[1].strip()
                if current_agent not in rules:
                    rules[current_agent] = {"Allow": [], "Disallow": []}
            elif line.lower().startswith("disallow:") and current_agent:
                path = line.split(":", 1)[1].strip()
                if path:
                    rules[current_agent]["Disallow"].append(path)
            elif line.lower().startswith("allow:") and current_agent:
                path = line.split(":", 1)[1].strip()
                if path:
                    rules[current_agent]["Allow"].append(path)

        return rules

    def _get_rules_for_agent(self, user_agent: str) -> dict[str, list[str]]:
        """Get rules for a specific user agent, merging with '*' baseline.

        Per robots.txt standard, the ``*`` user-agent provides baseline
        rules, and agent-specific rules supplement/override them.
        """
        base = dict(self._parsed.get("*", {"Allow": [], "Disallow": []}))
        agent_rules = self._parsed.get(user_agent)

        if agent_rules:
            # Merge: agent-specific rules replace/extend the baseline
            merged_allow = list(base.get("Allow", [])) + list(agent_rules.get("Allow", []))
            merged_disallow = list(base.get("Disallow", [])) + list(agent_rules.get("Disallow", []))
            return {"Allow": merged_allow, "Disallow": merged_disallow}

        return base

    def validate(self, url: str) -> bool:
        """Check if a URL is allowed for the ClaudeBot user-agent.

        Args:
            url: Full URL to validate (e.g., "https://www.coursera.org/learn/ml")

        Returns:
            True if the path is allowed, False if blocked.

        Raises:
            ValueError: If the URL is not a Coursera URL.
        """
        parsed = urlparse(url)

        if parsed.hostname and "coursera.org" not in parsed.hostname:
            raise ValueError(
                f"Non-Coursera URL rejected: {url}. "
                "Only coursera.org URLs are within scope."
            )

        path = parsed.path.rstrip("/") or "/"

        # Check against ClaudeBot-specific rules from robots.txt
        rules = self._get_rules_for_agent(self._USER_AGENT)

        # Allow rules first — specific Allow overrides broader Disallow
        # (robots.txt standard: most specific rule wins)
        for allow_pattern in rules["Allow"]:
            if self._path_matches(path, allow_pattern):
                self._log_access(url, path, True, f"matches Allow: {allow_pattern}")
                return True

        # Then check Disallow rules
        for disallow_pattern in rules["Disallow"]:
            if self._path_matches(path, disallow_pattern):
                self._log_access(url, path, False, f"matches Disallow: {disallow_pattern}")
                return False

        # Fallback: no rule matches -> allowed (robots.txt default)
        # Cross-check against hardcoded lists, but skip if Allow overrides
        allow_paths = set(rules.get("Allow", []))
        for blocked in self._blocked_prefixes:
            if path.startswith(blocked):
                overridden = any(path.startswith(a) for a in allow_paths)
                if overridden:
                    self._log_access(url, path, True, f"Allow overrides hardcoded block: {blocked}")
                    return True
                self._log_access(url, path, False, f"hardcoded block: {blocked}")
                return False

        self._log_access(url, path, True, "no blocking rule found")
        return True

    @staticmethod
    def _path_matches(path: str, pattern: str) -> bool:
        """Check if a URL path matches a robots.txt pattern.

        Supports prefix matching (standard robots.txt behavior):
        ``/api/`` matches ``/api/v1/enrollments``.
        """
        if not pattern:
            return False
        # robots.txt patterns are prefix matches
        return path == pattern or path.startswith(pattern)

    def _log_access(self, url: str, path: str, allowed: bool, reason: str) -> None:
        """Append an access attempt to the log file."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "url": url,
            "path": path,
            "allowed": allowed,
            "reason": reason,
            "user_agent": self._USER_AGENT,
        }

        _ACCESS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        log_entries: list[dict] = []
        if _ACCESS_LOG_PATH.exists():
            try:
                log_entries = json.loads(_ACCESS_LOG_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                log_entries = []

        log_entries.append(entry)
        # Keep only last 500 entries
        log_entries = log_entries[-500:]

        _ACCESS_LOG_PATH.write_text(
            json.dumps(log_entries, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        if not allowed:
            logger.warning("ACCESS DENIED: %s — %s", path, reason)

    def get_blocked_paths(self) -> list[str]:
        """Return all paths blocked for ClaudeBot."""
        rules = self._get_rules_for_agent(self._USER_AGENT)
        return rules["Disallow"]

    def get_allowed_paths(self) -> list[str]:
        """Return all paths explicitly allowed for ClaudeBot."""
        rules = self._get_rules_for_agent(self._USER_AGENT)
        return rules["Allow"]
