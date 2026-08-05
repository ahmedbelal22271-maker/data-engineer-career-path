"""Test suite for Coursera Tracker — validates safety layer, schema, and tracker logic."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.safety import RobotsTxtGuard
from scripts.schema import (
    CourseMetadata,
    CourseRecord,
    ModuleRecord,
    ModuleStatus,
    ProgressReport,
)
from scripts.tracker import CourseraTracker


def test_robots_txt_guard():
    """Validate robots.txt enforcement for ClaudeBot."""
    guard = RobotsTxtGuard()
    print("\n=== robots.txt Guard Tests ===")

    # Should ALLOW — public course pages
    assert guard.validate("https://www.coursera.org/learn/machine-learning"), \
        "FAIL: /learn/ should be allowed"
    print("  PASS: /learn/ -> allowed")

    assert guard.validate("https://www.coursera.org/specializations/data-science"), \
        "FAIL: /specializations/ should be allowed"
    print("  PASS: /specializations/ -> allowed")

    assert guard.validate("https://www.coursera.org/professional-certificates/google-it"), \
        "FAIL: /professional-certificates/ should be allowed"
    print("  PASS: /professional-certificates/ -> allowed")

    # Should BLOCK — API endpoints
    assert not guard.validate("https://www.coursera.org/api/v1/enrollments"), \
        "FAIL: /api/ should be blocked"
    print("  PASS: /api/ -> blocked")

    # Should BLOCK — lecture content
    assert not guard.validate("https://www.coursera.org/lecture/ml/week-1"), \
        "FAIL: /lecture/ should be blocked"
    print("  PASS: /lecture/ -> blocked")

    # Should BLOCK — account pages
    assert not guard.validate("https://www.coursera.org/account/settings"), \
        "FAIL: /account/ should be blocked"
    print("  PASS: /account/ -> blocked")

    # Should BLOCK — search
    assert not guard.validate("https://www.coursera.org/search?query=machine+learning"), \
        "FAIL: /search should be blocked"
    print("  PASS: /search -> blocked")

    # Should BLOCK — maestro
    assert not guard.validate("https://www.coursera.org/maestro/api/something"), \
        "FAIL: /maestro/ should be blocked"
    print("  PASS: /maestro/ -> blocked")

    # Should ALLOW — image proxy
    assert guard.validate("https://www.coursera.org/api/utilities/v1/imageproxy/some-image"), \
        "FAIL: /api/utilities/v1/imageproxy should be allowed"
    print("  PASS: /api/utilities/v1/imageproxy -> allowed")

    # Should reject non-Coursera URLs
    try:
        guard.validate("https://evil.com/steal")
        assert False, "FAIL: non-Coursera URL should raise ValueError"
    except ValueError:
        print("  PASS: non-Coursera URL -> ValueError")

    print("  ALL GUARD TESTS PASSED")


def test_schema():
    """Validate data models."""
    print("\n=== Schema Tests ===")

    # ModuleStatus enum
    assert ModuleStatus.PENDING.value == "pending"
    assert ModuleStatus.COMPLETED.value == "completed"
    print("  PASS: ModuleStatus enum values correct")

    # ModuleRecord
    mod = ModuleRecord()
    assert mod.status == ModuleStatus.PENDING
    assert mod.score is None
    mod.mark_completed(notes="Passed quiz", score=95.0)
    assert mod.status == ModuleStatus.COMPLETED
    assert mod.completed_at is not None
    assert mod.score == 95.0
    print("  PASS: ModuleRecord lifecycle")

    # CourseMetadata
    meta = CourseMetadata(slug="test-course", title="Test Course")
    d = meta.to_dict()
    assert d["slug"] == "test-course"
    assert "fetched_at" in d
    print("  PASS: CourseMetadata serialization")

    # CourseRecord
    record = CourseRecord(slug="test", title="Test")
    record.modules["Mod A"] = ModuleRecord(status=ModuleStatus.COMPLETED)
    record.modules["Mod B"] = ModuleRecord(status=ModuleStatus.IN_PROGRESS)
    record.modules["Mod C"] = ModuleRecord()
    assert record.total_modules == 3
    assert record.completed_count == 1
    assert record.in_progress_count == 1
    assert record.pending_count == 1
    assert record.completion_pct == 33.3
    print("  PASS: CourseRecord counters")

    # Round-trip serialization
    d = record.to_dict()
    restored = CourseRecord.from_dict(d)
    assert restored.slug == record.slug
    assert restored.total_modules == record.total_modules
    assert restored.completion_pct == record.completion_pct
    print("  PASS: CourseRecord round-trip serialization")

    print("  ALL SCHEMA TESTS PASSED")


def test_tracker():
    """Validate core tracker operations."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tracker = CourseraTracker(data_dir=tmpdir)
        print("\n=== Tracker Tests ===")

        # Register course
        rec = tracker.register_course(
            "machine-learning",
            title="Machine Learning",
            modules=["Linear Regression", "Neural Networks", "Recommender Systems"],
        )
        assert rec.total_modules == 3
        print("  PASS: register_course")

        # List courses
        courses = tracker.list_courses()
        assert "machine-learning" in courses
        print("  PASS: list_courses")

        # Update status
        tracker.update_status("machine-learning", "Linear Regression", "completed",
                              notes="Scored 92%", score=92.0)
        mod = tracker._courses["machine-learning"].modules["Linear Regression"]
        assert mod.status == ModuleStatus.COMPLETED
        assert mod.score == 92.0
        print("  PASS: update_status (completed)")

        # Update to in_progress
        tracker.update_status("machine-learning", "Neural Networks", "in_progress")
        mod = tracker._courses["machine-learning"].modules["Neural Networks"]
        assert mod.status == ModuleStatus.IN_PROGRESS
        print("  PASS: update_status (in_progress)")

        # Fetch progress
        report = tracker.fetch_progress("machine-learning")
        assert isinstance(report, ProgressReport)
        assert report.completed == 1
        assert report.in_progress == 1
        assert report.pending == 1
        assert report.completion_pct == 33.3
        print("  PASS: fetch_progress (single course)")

        # Fetch all progress
        all_reports = tracker.fetch_progress()
        assert isinstance(all_reports, list)
        assert len(all_reports) == 1
        print("  PASS: fetch_progress (all courses)")

        # Suggest next
        next_mods = tracker.suggest_next("machine-learning")
        assert "Neural Networks" in next_mods
        print("  PASS: suggest_next")

        # Export report
        md = tracker.export_report()
        assert "Machine Learning" in md
        assert "33.3%" in md
        print("  PASS: export_report (markdown)")

        # Export JSON
        js = tracker.export_json()
        data = json.loads(js)
        assert "machine-learning" in data["courses"]
        print("  PASS: export_report (json)")

        # Validate access
        assert tracker.validate_access("https://www.coursera.org/learn/ml")
        assert not tracker.validate_access("https://www.coursera.org/api/v1/x")
        print("  PASS: validate_access")

        # Error handling
        try:
            tracker.update_status("nonexistent", "mod", "completed")
            assert False, "Should have raised KeyError"
        except KeyError:
            print("  PASS: update_status (KeyError on unknown course)")

        try:
            tracker.update_status("machine-learning", "Fake Module", "completed")
            assert False, "Should have raised KeyError"
        except KeyError:
            print("  PASS: update_status (KeyError on unknown module)")

        try:
            tracker.update_status("machine-learning", "Neural Networks", "bogus")
            assert False, "Should have raised ValueError"
        except ValueError:
            print("  PASS: update_status (ValueError on bad status)")

        # Persistence: new tracker from same dir should load state
        tracker2 = CourseraTracker(data_dir=tmpdir)
        report2 = tracker2.fetch_progress("machine-learning")
        assert report2.completed == 1
        print("  PASS: state persistence across instances")

        # Unregister
        assert tracker.unregister_course("machine-learning")
        assert not tracker.unregister_course("nonexistent")
        print("  PASS: unregister_course")

        print("  ALL TRACKER TESTS PASSED")


if __name__ == "__main__":
    test_robots_txt_guard()
    test_schema()
    test_tracker()
    print("\n" + "=" * 40)
    print("ALL TESTS PASSED")
