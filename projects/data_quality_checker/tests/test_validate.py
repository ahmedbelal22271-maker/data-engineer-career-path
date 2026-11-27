import pandas as pd
from validate import validate_dataframe


def _sample_config() -> dict:
    return {
        "dataset": "test_311",
        "min_rows": 3,
        "columns": {
            "unique_key": {"type": "string", "max_null_pct": 0.0, "unique": True},
            "latitude": {"type": "float", "min": 40.4, "max": 41.0, "max_null_pct": 0.0},
            "borough": {"type": "string", "allowed_values": ["MANHATTAN", "BROOKLYN"]},
        },
    }


def _valid_df() -> pd.DataFrame:
    # [String-Encoded JSON Numbers] Socrata returns floats as strings (e.g., "40.71");
    # validate_dataframe() must coerce them cleanly before range checks.
    return pd.DataFrame([
        {"unique_key": "1", "latitude": "40.4", "borough": "MANHATTAN"},
        {"unique_key": "2", "latitude": "40.75", "borough": "BROOKLYN"},
        {"unique_key": "3", "latitude": "41.0", "borough": "MANHATTAN"},
    ])


def test_validate_happy_path():
    result = validate_dataframe(_valid_df(), _sample_config())
    assert result["overall_status"] == "PASS"
    assert result["pass_rate"] == 100.0
    assert result["failed_checks"] == 0


def test_validate_null_and_duplicate_failures():
    df = _valid_df()
    # Inject a duplicate key ("1") and a null latitude
    df.loc[1, "unique_key"] = "1"
    df.loc[2, "latitude"] = None

    result = validate_dataframe(df, _sample_config())
    assert result["overall_status"] == "FAIL"
    failed_cols = {c["column"] for c in result["checks"] if c["status"] == "FAIL"}
    assert "unique_key" in failed_cols
    assert "latitude" in failed_cols


def test_validate_out_of_range_and_truncated_rows():
    # [Truncated Batch Guard] Only 2 rows (< min_rows=3) and latitude=99.0 (> 41.0)
    df = pd.DataFrame([
        {"unique_key": "1", "latitude": "99.0", "borough": "MANHATTAN"},
        {"unique_key": "2", "latitude": "40.7", "borough": "QUEENS"},
    ])
    result = validate_dataframe(df, _sample_config())
    assert result["overall_status"] == "FAIL"
    failed_checks = {c["check_name"] for c in result["checks"] if c["status"] == "FAIL"}
    assert "expect_table_row_count_to_be_between" in failed_checks
    assert "expect_column_values_to_be_between" in failed_checks
    assert "expect_column_values_to_be_in_set" in failed_checks
