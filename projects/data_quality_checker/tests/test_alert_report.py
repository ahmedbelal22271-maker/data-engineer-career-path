import requests
from alert import send_alert
from report import generate_html_report


def test_generate_html_report_escapes_html(tmp_path):
    report = {
        "dataset": "test_311",
        "total_checks": 1,
        "passed_checks": 0,
        "failed_checks": 1,
        "pass_rate": 0.0,
        "overall_status": "FAIL",
        "checks": [
            {
                "check_name": "expect_column_values_to_be_in_set",
                "column": "borough",
                "status": "FAIL",
                "expected": {"value_set": ["MANHATTAN"]},
                "actual": 100.0,
                # [XSS Autoescape Verification] Raw <script> must be escaped in HTML output
                "details": "<script>alert(1)</script>",
            }
        ],
    }
    metadata = {"ingested_at": "2026-11-26T10:00:00+00:00", "row_count": 10}
    trends = {"current_run_id": "run-1", "pass_rate_delta": None, "worsening_checks": []}

    path = generate_html_report(report, metadata, trends, [], output_dir=str(tmp_path))
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    assert "test_311" in html
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html


def test_send_alert_silent_on_pass(monkeypatch):
    monkeypatch.delenv("WEBHOOK_URL", raising=False)
    report = {"dataset": "test_311", "overall_status": "PASS", "pass_rate": 100.0, "checks": []}
    assert send_alert(report, {"current_run_id": "1"}, "reports/r.html") is False


def test_send_alert_webhook_and_non_blocking_error(monkeypatch):
    monkeypatch.setenv("WEBHOOK_URL", "https://example.com/webhook")

    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Simulated Slack outage")

    # [Non-Blocking Alerting] Even if requests.post raises ConnectionError, send_alert must not crash
    monkeypatch.setattr(requests, "post", fake_post)
    report = {"dataset": "test_311", "overall_status": "FAIL", "pass_rate": 50.0, "checks": []}
    assert send_alert(report, {"current_run_id": "1"}, "reports/r.html") is True
