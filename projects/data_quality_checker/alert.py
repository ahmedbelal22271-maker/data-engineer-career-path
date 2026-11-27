import logging
import os
import requests

logger = logging.getLogger(__name__)


def send_alert(
    report: dict,
    trend_summary: dict,
    report_path: str,
    min_pass_rate: float = 100.0,
) -> bool:
    """Dispatch a webhook alert on quality failure/threshold breach, or log a dry-run."""
    # [Threshold & Status Gate] Stay silent on healthy runs (e.g., PASS and 100.0% >= 100.0%);
    # only alert when overall_status == "FAIL" or pass_rate drops below min_pass_rate (e.g., 95.0 < 100.0).
    should_alert = (
        report["overall_status"] == "FAIL" or report["pass_rate"] < min_pass_rate
    )
    if not should_alert:
        logger.info("Quality check passed (%.2f%%); no alert triggered.", report["pass_rate"])
        return False

    failing = [
        f"- {c['column']} ({c['check_name']}): {c['details']}"
        for c in report["checks"]
        if c["status"] == "FAIL"
    ]
    delta = trend_summary.get("pass_rate_delta")
    delta_str = f"{delta:+.2f}%" if delta is not None else "N/A (first run)"

    message = (
        f"[DATA QUALITY ALERT] {report['dataset']} — {report['overall_status']}\n"
        f"Run ID: {trend_summary['current_run_id']}\n"
        f"Pass Rate: {report['pass_rate']}% (Delta: {delta_str})\n"
        f"Report: {report_path}\n"
        f"Failing Checks:\n" + ("\n".join(failing) if failing else "None")
    )

    # [Secrets via Environment Variables] Never hardcode Slack/Discord webhook URLs in Git;
    # read WEBHOOK_URL from the environment so local/CI runs without secrets still work.
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        logger.warning("WEBHOOK_URL not set; dry-run alert:\n%s", message)
        return True

    # [Non-Blocking Alerting] If Slack/Discord returns 503 or times out after 10s,
    # log the error without crashing—preserving the already-saved DB history and HTML report.
    try:
        response = requests.post(webhook_url, json={"text": message}, timeout=10)
        response.raise_for_status()
        logger.info("Alert dispatched successfully to webhook.")
    except requests.exceptions.RequestException as e:
        logger.error("Failed to dispatch webhook alert: %s", e)

    return True
