from history import analyze_trends, get_recent_runs, save_run


def _make_report(pass_rate: float, zip_null_pct: float, status: str = "PASS") -> dict:
    return {
        "dataset": "test_311",
        "total_checks": 2,
        "passed_checks": 2 if status == "PASS" else 1,
        "failed_checks": 0 if status == "PASS" else 1,
        "pass_rate": pass_rate,
        "overall_status": status,
        "checks": [
            {
                "check_name": "expect_column_values_to_not_be_null",
                "column": "incident_zip",
                "status": status,
                "expected": {"mostly": 0.85},
                "actual": zip_null_pct,
                "details": "unexpected_count=0",
            }
        ],
    }


def test_history_cold_start_and_drift(tmp_path):
    # [Isolated Temp Storage] Use pytest's tmp_path so tests never pollute data/quality_history.db
    db_file = str(tmp_path / "test_history.db")

    # Run 1: Healthy baseline (100% pass, 1000 rows, 1.0% null)
    r1 = save_run(
        _make_report(100.0, 1.0, "PASS"),
        {"ingested_at": "2026-11-25T10:00:00+00:00", "row_count": 1000},
        db_path=db_file,
    )
    cold = analyze_trends(r1, db_path=db_file)
    assert cold["pass_rate_delta"] is None
    assert cold["worsening_checks"] == []

    # Run 2: Degraded batch (50% pass, 800 rows -> -20.0% volume drop, 25.0% null)
    r2 = save_run(
        _make_report(50.0, 25.0, "FAIL"),
        {"ingested_at": "2026-11-26T10:00:00+00:00", "row_count": 800},
        db_path=db_file,
    )
    recent = get_recent_runs(limit=10, db_path=db_file)
    assert len(recent) == 2
    # Newest-first ordering: Run 2 must appear before Run 1
    assert recent[0]["run_id"] == r2

    trends = analyze_trends(r2, db_path=db_file)
    assert trends["pass_rate_delta"] == -50.0
    assert trends["row_count_pct_change"] == -20.0
    assert len(trends["worsening_checks"]) == 1
    assert trends["worsening_checks"][0]["column"] == "incident_zip"
