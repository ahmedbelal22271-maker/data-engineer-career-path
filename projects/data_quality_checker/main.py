import argparse
import logging
import sys

from alert import send_alert
from history import DEFAULT_DB_PATH, analyze_trends, get_recent_runs, save_run
from ingest import ingest_data
from report import generate_html_report
from validate import load_expectations, validate_dataframe

DEFAULT_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
logger = logging.getLogger(__name__)


def run_pipeline(
    url: str = DEFAULT_URL,
    limit: int = 1000,
    config_path: str = "config/expectations.yaml",
    db_path: str = DEFAULT_DB_PATH,
    output_dir: str = "reports",
    template_dir: str = "templates",
    min_pass_rate: float = 100.0,
) -> dict:
    """Execute the full DQ pipeline: Ingest -> Validate -> History -> Report -> Alert."""
    # [Dependency Injection for Testability] Accepting paths as arguments (with defaults)
    # lets Milestone 5 tests pass tmp_path without touching data/quality_history.db or reports/.
    config = load_expectations(config_path)
    df, metadata = ingest_data(url, limit=limit)
    report = validate_dataframe(df, config)

    # [Fault-Isolated Ordering] Persist history and render the HTML report BEFORE alerting
    # so a webhook outage never prevents audit records from being saved.
    run_id = save_run(report, metadata, db_path=db_path)
    recent_runs = get_recent_runs(limit=10, db_path=db_path)
    trend_summary = analyze_trends(run_id, lookback=5, db_path=db_path)

    report_path = generate_html_report(
        report,
        metadata,
        trend_summary,
        recent_runs,
        output_dir=output_dir,
        template_dir=template_dir,
    )
    alert_sent = send_alert(
        report, trend_summary, report_path, min_pass_rate=min_pass_rate
    )

    logger.info(
        "Pipeline complete | status=%s | pass_rate=%.2f%% | report=%s",
        report["overall_status"],
        report["pass_rate"],
        report_path,
    )
    return {
        "run_id": run_id,
        "report": report,
        "trend_summary": trend_summary,
        "report_path": report_path,
        "alert_sent": alert_sent,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Data Quality Checker pipeline.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Socrata JSON API endpoint")
    parser.add_argument("--limit", type=int, default=1000, help="Max rows to ingest")
    parser.add_argument("--config", default="config/expectations.yaml", help="Expectations YAML path")
    args = parser.parse_args()

    result = run_pipeline(url=args.url, limit=args.limit, config_path=args.config)
    # [CI/Orchestrator Gate] Exit non-zero (1) on FAIL so schedulers/CI halt downstream jobs.
    if result["report"]["overall_status"] == "FAIL":
        sys.exit(1)
