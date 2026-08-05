"""Coursera Course Tracker — local-first progress tracking with robots.txt enforcement."""

from .safety import RobotsTxtGuard
from .schema import CourseMetadata, CourseRecord, ModuleStatus, ProgressReport
from .tracker import CourseraTracker

__all__ = [
    "CourseraTracker",
    "RobotsTxtGuard",
    "CourseMetadata",
    "CourseRecord",
    "ModuleStatus",
    "ProgressReport",
]
