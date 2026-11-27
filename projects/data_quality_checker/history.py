import json
import os
import sqlite3
import uuid
from contextlib import closing

DEFAULT_DB_PATH = "data/quality_history.db"


def _get_connection(db_path: str) -> sqlite3.Connection:
    """Open a SQLite connection with dict-like row access and FK enforcement."""
    conn = sqlite3.connect(db_path)
    # Return sqlite3.Row objects so columns can be accessed by name and converted via dict(row)
    conn.row_factory = sqlite3.Row
    # SQLite disables foreign keys by default for legacy compatibility; enable per connection
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Idempotently create the 1-to-many validation_runs and check_results tables."""
    parent_dir = os.path.dirname(db_path)
    # Guard against empty dirname (e.g., when passing 'test.db' in unit tests)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    # closing() ensures the OS file handle is closed; `with conn:` commits or rolls back
    with closing(_get_connection(db_path)) as conn:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS validation_runs (
                    run_id TEXT PRIMARY KEY,
                    ingested_at TEXT NOT NULL,
                    dataset_name TEXT NOT NULL,
                    source_url TEXT,
                    row_count INTEGER NOT NULL,
                    total_checks INTEGER NOT NULL,
                    passed_checks INTEGER NOT NULL,
                    failed_checks INTEGER NOT NULL,
                    pass_rate REAL NOT NULL,
                    overall_status TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS check_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    check_name TEXT NOT NULL,
                    column_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    expected TEXT,
                    actual TEXT,
                    details TEXT,
                    FOREIGN KEY (run_id) REFERENCES validation_runs(run_id)
                )
                """
            )


def save_run(report: dict, metadata: dict, db_path: str = DEFAULT_DB_PATH) -> str:
    """Persist a validation run and all its check results in a single atomic transaction."""
    init_db(db_path)
    # Surrogate UUID primary key avoids timestamp collisions in fast/concurrent runs
    run_id = str(uuid.uuid4())

    check_rows = [
        (
            run_id,
            check["check_name"],
            check["column"],
            check["status"],
            # SQLite only stores scalars; serialize the expectation parameter dict to JSON
            json.dumps(check["expected"]),
            str(check["actual"]),
            check.get("details", ""),
        )
        for check in report["checks"]
    ]

    # Single atomic transaction: if executemany fails, the parent run insert rolls back too
    with closing(_get_connection(db_path)) as conn:
        with conn:
            conn.execute(
                """
                INSERT INTO validation_runs (
                    run_id, ingested_at, dataset_name, source_url,
                    row_count, total_checks, passed_checks, failed_checks,
                    pass_rate, overall_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    metadata["ingested_at"],
                    report["dataset"],
                    metadata.get("source_url", ""),
                    metadata["row_count"],
                    report["total_checks"],
                    report["passed_checks"],
                    report["failed_checks"],
                    report["pass_rate"],
                    report["overall_status"],
                ),
            )
            conn.executemany(
                """
                INSERT INTO check_results (
                    run_id, check_name, column_name, status,
                    expected, actual, details
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                check_rows,
            )

    return run_id


def get_recent_runs(limit: int = 10, db_path: str = DEFAULT_DB_PATH) -> list[dict]:
    """Return the latest N runs ordered newest-first without needing a child JOIN."""
    if not os.path.exists(db_path):
        return []

    with closing(_get_connection(db_path)) as conn:
        rows = conn.execute(
            """
            SELECT run_id, ingested_at, dataset_name, source_url,
                   row_count, total_checks, passed_checks, failed_checks,
                   pass_rate, overall_status
            FROM validation_runs
            ORDER BY ingested_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def _to_float(value: str | None) -> float | None:
    """Safely parse stored TEXT metrics to float, skipping empty/non-numeric values."""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def analyze_trends(
    current_run_id: str, lookback: int = 5, db_path: str = DEFAULT_DB_PATH
) -> dict:
    """Compare the current run against prior runs to detect pass-rate, volume, and check drift."""
    with closing(_get_connection(db_path)) as conn:
        current_row = conn.execute(
            "SELECT * FROM validation_runs WHERE run_id = ?",
            (current_run_id,),
        ).fetchone()
        if current_row is None:
            raise ValueError(f"Run ID not found: {current_run_id}")

        # [Concept 2: Baseline Comparisons] Exclude current_run_id so a broken batch
        # (e.g., 200 rows today) doesn't pull down the rolling average and hide the anomaly.
        prior_rows = conn.execute(
            """
            SELECT * FROM validation_runs
            WHERE run_id != ?
            ORDER BY ingested_at DESC
            LIMIT ?
            """,
            (current_run_id, lookback),
        ).fetchall()

        total_runs = conn.execute(
            "SELECT COUNT(*) FROM validation_runs"
        ).fetchone()[0]

        # [Concept 3: Check-Level Degradation] Even if a check still PASSes (e.g.,
        # closed_date <= 90%), flag if unexpected_percent rose (e.g., 68.5 -> 73.2).
        worsening_checks = []
        if prior_rows:
            prev_run_id = prior_rows[0]["run_id"]
            # Fetch both runs' checks in 1 query (avoiding N+1 per-check SELECTs)
            check_rows = conn.execute(
                """
                SELECT run_id, check_name, column_name, actual
                FROM check_results
                WHERE run_id IN (?, ?)
                """,
                (current_run_id, prev_run_id),
            ).fetchall()

            prev_map = {
                (r["check_name"], r["column_name"]): _to_float(r["actual"])
                for r in check_rows
                if r["run_id"] == prev_run_id
            }
            for r in check_rows:
                if r["run_id"] != current_run_id:
                    continue
                # actual is stored as TEXT; _to_float() skips non-numeric values like ""
                curr_val = _to_float(r["actual"])
                prev_val = prev_map.get((r["check_name"], r["column_name"]))
                if (
                    curr_val is not None
                    and prev_val is not None
                    and curr_val > prev_val
                ):
                    worsening_checks.append({
                        "column": r["column_name"],
                        "check_name": r["check_name"],
                        "previous": prev_val,
                        "current": curr_val,
                    })

    current_pass_rate = current_row["pass_rate"]
    # [Concept 1: Cold-Start Guard] If only 1 run exists in the DB, there is no
    # previous run—return None instead of crashing with an IndexError.
    if not prior_rows:
        return {
            "current_run_id": current_run_id,
            "total_runs_recorded": total_runs,
            "current_pass_rate": current_pass_rate,
            "previous_pass_rate": None,
            "pass_rate_delta": None,
            "avg_baseline_pass_rate": None,
            "avg_baseline_row_count": None,
            "row_count_pct_change": None,
            "worsening_checks": [],
        }

    previous_pass_rate = prior_rows[0]["pass_rate"]
    # [Concept 2: Rolling Baselines] Average of prior runs only (e.g., (95+100+100)/3 = 98.33)
    avg_pass_rate = round(
        sum(r["pass_rate"] for r in prior_rows) / len(prior_rows), 2
    )
    avg_row_count = round(
        sum(r["row_count"] for r in prior_rows) / len(prior_rows), 2
    )
    # Row-count % change: e.g., ((800 - 1000) / 1000) * 100 = -20.0% volume drop
    row_pct_change = (
        round(((current_row["row_count"] - avg_row_count) / avg_row_count) * 100, 2)
        if avg_row_count > 0
        else None
    )

    return {
        "current_run_id": current_run_id,
        "total_runs_recorded": total_runs,
        "current_pass_rate": current_pass_rate,
        "previous_pass_rate": previous_pass_rate,
        # [Concept 1: Pass-Rate Delta] e.g., 90.0 - 95.0 = -5.0 (5pp drop since last run)
        "pass_rate_delta": round(current_pass_rate - previous_pass_rate, 2),
        "avg_baseline_pass_rate": avg_pass_rate,
        "avg_baseline_row_count": avg_row_count,
        "row_count_pct_change": row_pct_change,
        "worsening_checks": worsening_checks,
    }
