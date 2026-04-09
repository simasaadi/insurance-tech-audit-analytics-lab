from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[2]
SEEDS = ROOT / "data" / "seeds"
CURATED = ROOT / "data" / "curated"
AUDIT_TESTS = ROOT / "sql" / "audit-tests"

EXPECTED_COLUMNS = {
    "user_access.csv": ["user_id", "employee_name", "department", "job_title", "employment_status", "termination_date", "mfa_enabled", "last_login_date", "access_group", "account_type"],
    "privileged_accounts.csv": ["account_id", "user_id", "account_name", "privilege_type", "approved_group_member", "named_owner", "last_used_date"],
    "asset_inventory.csv": ["asset_id", "hostname", "environment", "cloud_platform", "business_service", "business_criticality", "internet_facing", "os_version", "backup_status"],
    "vulnerability_findings.csv": ["finding_id", "asset_id", "severity", "cve_id", "kev_listed", "status", "date_identified", "sla_due_date", "date_closed"],
    "patching_status.csv": ["patch_id", "asset_id", "patch_group", "patch_status", "last_patch_date", "maintenance_window", "exception_approved"],
    "firewall_rules.csv": ["rule_id", "environment", "source_zone", "destination_zone", "port_protocol", "access_scope", "any_any_rule", "business_justification", "review_status"],
    "cloud_posture_findings.csv": ["finding_id", "cloud_platform", "resource_id", "resource_type", "control_area", "severity", "status", "public_exposure", "policy_name"],
    "backup_dr_test_logs.csv": ["test_id", "asset_id", "test_type", "test_date", "test_result", "retest_completed", "retest_date"],
    "change_tickets.csv": ["change_id", "asset_id", "change_type", "implementation_date", "approval_status", "post_implementation_review"],
    "application_inventory.csv": ["application_id", "application_name", "business_unit", "business_criticality", "data_classification", "hosting_model", "customer_facing", "dr_tier"],
}

PRIMARY_KEYS = {
    "user_access.csv": "user_id",
    "privileged_accounts.csv": "account_id",
    "asset_inventory.csv": "asset_id",
    "vulnerability_findings.csv": "finding_id",
    "patching_status.csv": "patch_id",
    "firewall_rules.csv": "rule_id",
    "cloud_posture_findings.csv": "finding_id",
    "backup_dr_test_logs.csv": "test_id",
    "change_tickets.csv": "change_id",
    "application_inventory.csv": "application_id",
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def fail(message, errors):
    print(f"FAIL: {message}")
    errors.append(message)


def ok(message):
    print(f"PASS: {message}")


def main():
    errors = []

    for filename, expected in EXPECTED_COLUMNS.items():
        path = SEEDS / filename
        if not path.exists():
            fail(f"Missing seed file: {filename}", errors)
            continue

        rows = read_csv(path)
        if not rows:
            fail(f"Seed file is empty: {filename}", errors)
            continue

        actual = rows[0].keys()
        missing = [col for col in expected if col not in actual]
        if missing:
            fail(f"{filename} missing columns: {missing}", errors)
        else:
            ok(f"{filename} columns validated")

        pk = PRIMARY_KEYS[filename]
        seen = set()
        dupes = set()
        for row in rows:
            key = row[pk]
            if key in seen:
                dupes.add(key)
            seen.add(key)
        if dupes:
            fail(f"{filename} has duplicate keys: {sorted(dupes)}", errors)
        else:
            ok(f"{filename} primary key uniqueness validated")

    if (SEEDS / "asset_inventory.csv").exists():
        asset_ids = {row["asset_id"] for row in read_csv(SEEDS / "asset_inventory.csv")}

        for filename, fk_field in [
            ("vulnerability_findings.csv", "asset_id"),
            ("patching_status.csv", "asset_id"),
            ("backup_dr_test_logs.csv", "asset_id"),
            ("change_tickets.csv", "asset_id"),
        ]:
            path = SEEDS / filename
            if path.exists():
                rows = read_csv(path)
                bad_refs = sorted({row[fk_field] for row in rows if row[fk_field] not in asset_ids})
                if bad_refs:
                    fail(f"{filename} contains invalid asset references: {bad_refs}", errors)
                else:
                    ok(f"{filename} asset references validated")

    matrix_path = ROOT / "audit" / "04_risk-control-matrix" / "risk-control-matrix.csv"
    crosswalk_path = ROOT / "framework-mapping" / "control-framework-crosswalk.csv"

    if matrix_path.exists() and crosswalk_path.exists():
        matrix_ids = {row["test_id"] for row in read_csv(matrix_path)}
        crosswalk_ids = {row["test_id"] for row in read_csv(crosswalk_path)}

        if matrix_ids != crosswalk_ids:
            fail("Risk-control matrix test IDs do not match framework crosswalk test IDs", errors)
        else:
            ok("Risk-control matrix and framework crosswalk IDs are aligned")

    sql_files = sorted(AUDIT_TESTS.glob("*.sql"))
    if len(sql_files) != 12:
        fail(f"Expected 12 SQL audit tests but found {len(sql_files)}", errors)
    else:
        ok("Found 10 SQL audit tests")

    curated_files = [
        CURATED / "audit_overview_summary.csv",
        CURATED / "iam_review_summary.csv",
        CURATED / "vulnerability_summary.csv",
        CURATED / "cloud_infra_posture_summary.csv",
        CURATED / "iam_detail.csv",
        CURATED / "vulnerability_detail.csv",
        CURATED / "cloud_infra_detail.csv",
        CURATED / "resilience_detail.csv",
    ]
    for path in curated_files:
        if not path.exists():
            fail(f"Missing curated output: {path.name}", errors)
        else:
            ok(f"Curated output present: {path.name}")

    if errors:
        print(f"\nQA checks failed: {len(errors)} issue(s)")
        sys.exit(1)

    print("\nAll QA checks passed successfully.")


if __name__ == "__main__":
    main()

