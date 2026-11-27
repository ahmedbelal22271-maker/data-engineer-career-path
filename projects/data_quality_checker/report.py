import os
from datetime import datetime, timezone
from jinja2 import Environment, FileSystemLoader, select_autoescape


def generate_html_report(
    report: dict,
    metadata: dict,
    trend_summary: dict,
    recent_runs: list[dict],
    output_dir: str = "reports",
    template_dir: str = "templates",
) -> str:
    """Render a self-contained HTML quality report and return the output file path."""
    # [Idempotent Directory Creation] Ensure reports/ exists before writing
    # (e.g., if reports/ is gitignored and missing on a fresh clone).
    os.makedirs(output_dir, exist_ok=True)

    # [XSS Protection via Autoescape] Untrusted API values (e.g., "<script>"
    # in a sample failing value) are escaped to "&lt;script&gt;" instead of executing.
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("report.html")

    html_content = template.render(
        report=report,
        metadata=metadata,
        trend_summary=trend_summary,
        recent_runs=recent_runs,
    )

    # [Timestamped Artifact Naming] e.g., quality_report_20261126_094500.html
    # prevents overwriting earlier reports on the same day.
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"quality_report_{timestamp}.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path
