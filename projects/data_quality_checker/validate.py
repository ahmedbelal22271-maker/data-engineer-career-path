import yaml
import pandas as pd
import great_expectations as gx
import great_expectations.expectations as gxe


def load_expectations(path: str = "config/expectations.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def validate_dataframe(df: pd.DataFrame, config: dict) -> dict:
    # Coerce numeric/datetime columns configured in expectations so GX can evaluate ranges cleanly
    df = df.copy()
    for col, rules in config.get("columns", {}).items():
        if col in df.columns:
            if rules.get("type") == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce")
            elif rules.get("type") == "datetime":
                df[col] = pd.to_datetime(df[col], errors="coerce")

    context = gx.get_context(mode="ephemeral")
    data_source = context.data_sources.add_pandas("pandas_source")
    data_asset = data_source.add_dataframe_asset("dataframe_asset")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("whole_df")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    suite = gx.ExpectationSuite(name=config.get("dataset", "dq_suite"))

    if "min_rows" in config:
        suite.add_expectation(
            gxe.ExpectTableRowCountToBeBetween(min_value=config["min_rows"])
        )

    for col, rules in config.get("columns", {}).items():
        if "max_null_pct" in rules:
            suite.add_expectation(
                gxe.ExpectColumnValuesToNotBeNull(
                    column=col, mostly=1.0 - rules["max_null_pct"]
                )
            )
        if rules.get("unique"):
            suite.add_expectation(gxe.ExpectColumnValuesToBeUnique(column=col))
        if "min" in rules or "max" in rules:
            suite.add_expectation(
                gxe.ExpectColumnValuesToBeBetween(
                    column=col,
                    min_value=rules.get("min"),
                    max_value=rules.get("max"),
                )
            )
        if "allowed_values" in rules:
            suite.add_expectation(
                gxe.ExpectColumnValuesToBeInSet(
                    column=col, value_set=rules["allowed_values"]
                )
            )

    gx_result = batch.validate(suite)

    checks = []
    for res in gx_result.results:
        cfg = res.expectation_config
        checks.append({
            "check_name": cfg.type,
            "column": cfg.kwargs.get("column", "__dataset__"),
            "status": "PASS" if res.success else "FAIL",
            "expected": {k: v for k, v in cfg.kwargs.items() if k != "column"},
            "actual": res.result.get("unexpected_percent", res.result.get("observed_value", "")),
            "details": f"unexpected_count={res.result.get('unexpected_count', 0)}",
        })

    passed = sum(1 for c in checks if c["status"] == "PASS")
    total = len(checks)
    return {
        "dataset": config.get("dataset", "unknown"),
        "total_checks": total,
        "passed_checks": passed,
        "failed_checks": total - passed,
        "pass_rate": round((passed / total) * 100, 2) if total else 0.0,
        "overall_status": "PASS" if gx_result.success else "FAIL",
        "checks": checks,
    }
