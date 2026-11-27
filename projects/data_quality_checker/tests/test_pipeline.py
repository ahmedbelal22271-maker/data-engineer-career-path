import os
import requests
import yaml
from main import run_pipeline


class _FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return [
            {"unique_key": "1", "latitude": "40.71", "borough": "MANHATTAN"},
            {"unique_key": "2", "latitude": "40.75", "borough": "BROOKLYN"},
            {"unique_key": "3", "latitude": "40.80", "borough": "MANHATTAN"},
        ]


def test_end_to_end_pipeline_offline(tmp_path, monkeypatch):
    # [Hermetic Integration Test] Mock HTTP so tests never hit live NYC Open Data
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: _FakeResponse())
    monkeypatch.delenv("WEBHOOK_URL", raising=False)

    cfg_path = tmp_path / "expectations.yaml"
    cfg_path.write_text(
        yaml.safe_dump({
            "dataset": "integration_311",
            "min_rows": 2,
            "columns": {
                "unique_key": {"type": "string", "max_null_pct": 0.0, "unique": True},
                "latitude": {"type": "float", "min": 40.4, "max": 41.0},
            },
        }),
        encoding="utf-8",
    )

    db_path = str(tmp_path / "history.db")
    reports_dir = str(tmp_path / "reports")

    output = run_pipeline(
        url="https://fake.local/311.json",
        limit=3,
        config_path=str(cfg_path),
        db_path=db_path,
        output_dir=reports_dir,
    )

    assert output["report"]["overall_status"] == "PASS"
    assert output["alert_sent"] is False
    assert os.path.exists(db_path)
    assert os.path.exists(output["report_path"])
