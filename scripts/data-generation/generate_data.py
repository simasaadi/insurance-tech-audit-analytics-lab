from pathlib import Path
from datetime import datetime, date
import csv

ROOT = Path(__file__).resolve().parents[2]
SEEDS = ROOT / "data" / "seeds"
CURATED = ROOT / "data" / "curated"

REF_DATE = date(2026, 4, 7)
DORMANT_THRESHOLD = date(2026, 2, 6)
UNSUPPORTED_OS = {"Windows Server 2012", "Windows Server 2016", "Ubuntu 18.04"}
PUBLIC_RESOURCE_TYPES = {"Storage Account", "S3 Bucket", "EC2 Instance"}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_date(value: str):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def main():
    users = read_csv(SEEDS / "user_access.csv")
    privileged = read_csv(SEEDS / "privileged_accounts.csv")
    assets = read_csv(SEEDS / "asset_inventory.csv")
    vulns = read_csv(SEEDS / "vulnerability_findings.csv")
    patches = read_csv(SEEDS / "patching_status.csv")
    firewall = read_csv(SEEDS / "firewall_rules.csv")
    cloud = read_csv(SEEDS / "cloud_posture_findings.csv")
    dr_logs = read_csv(SEEDS / "backup_dr_test_logs.csv")
    changes = read_csv(SEEDS / "change_tickets.csv")

    assets_by_id = {row["asset_id"]: row for row in assets}
    users_by_id = {row["user_id"]: row for row in users}

    active_users_without_mfa = sum(
        1 for row in users
        if row["employment_status"] == "Active" and row["mfa_enabled"] == "No"
    )

    dormant_privileged_accounts = sum(
        1 for row in privileged
        if parse_date(row["last_used_date"]) and parse_date(row["last_used_date"]) < DORMANT_THRESHOLD
    )

    service_accounts_without_owner = sum(
        1 for row in privileged
        if row["account_name"].startswith("svc-") and not row["named_owner"].strip()
    )

    terminated_users_with_post_term_activity = sum(
        1 for row in users
        if row["employment_status"] == "Terminated"
        and parse_date(row["termination_date"])
        and parse_date(row["last_login_date"])
        and parse_date(row["last_login_date"]) > parse_date(row["termination_date"])
    )

    privileged_accounts_outside_group_model = sum(
        1 for row in privileged if row["approved_group_member"] == "No"
    )

    open_critical_vulns = sum(
        1 for row in vulns if row["status"] == "Open" and row["severity"] == "Critical"
    )

    open_high_vulns = sum(
        1 for row in vulns if row["status"] == "Open" and row["severity"] == "High"
    )

    overdue_critical_or_high = sum(
        1 for row in vulns
        if row["status"] == "Open"
        and row["severity"] in {"Critical", "High"}
        and parse_date(row["sla_due_date"]) < REF_DATE
    )

    kev_listed_overdue = sum(
        1 for row in vulns
        if row["status"] == "Open"
        and row["severity"] in {"Critical", "High"}
        and row["kev_listed"] == "Yes"
        and parse_date(row["sla_due_date"]) < REF_DATE
    )

    critical_assets_with_failed_backup = sum(
        1 for row in assets
        if row["business_criticality"] == "Critical" and row["backup_status"] == "Failed"
    )

    failed_dr_without_retest = sum(
        1 for row in dr_logs
        if row["test_result"] == "Fail" and row["retest_completed"] == "No"
    )

    open_public_cloud_exposures = sum(
        1 for row in cloud
        if row["status"] == "Open"
        and row["public_exposure"] == "Yes"
        and row["resource_type"] in PUBLIC_RESOURCE_TYPES
    )

    unsupported_os_in_prod = sum(
        1 for row in assets
        if row["environment"] == "Production" and row["os_version"] in UNSUPPORTED_OS
    )

    permissive_firewall_rules = sum(
        1 for row in firewall
        if row["environment"] == "Production"
        and (
            row["any_any_rule"] == "Yes"
            or row["access_scope"] == "Broad"
            or row["port_protocol"] == "Any/Any"
        )
    )

    assets_with_missing_patches = sum(
        1 for row in patches if row["patch_status"] == "Missing"
    )

    emergency_changes_without_complete_review = sum(
        1 for row in changes
        if row["change_type"] == "Emergency"
        and row["post_implementation_review"] != "Completed"
    )

    write_csv(
        CURATED / "audit_overview_summary.csv",
        ["domain", "open_findings_count"],
        [
            {"domain": "IAM", "open_findings_count": active_users_without_mfa + dormant_privileged_accounts + service_accounts_without_owner + terminated_users_with_post_term_activity},
            {"domain": "Vulnerability Management", "open_findings_count": overdue_critical_or_high},
            {"domain": "Infrastructure Security", "open_findings_count": unsupported_os_in_prod},
            {"domain": "Resilience", "open_findings_count": critical_assets_with_failed_backup + failed_dr_without_retest},
            {"domain": "Cloud Security", "open_findings_count": open_public_cloud_exposures},
            {"domain": "Network Security", "open_findings_count": permissive_firewall_rules},
        ],
    )

    write_csv(
        CURATED / "iam_review_summary.csv",
        ["metric", "value"],
        [
            {"metric": "Active users without MFA", "value": active_users_without_mfa},
            {"metric": "Dormant privileged accounts over 60 days", "value": dormant_privileged_accounts},
            {"metric": "Privileged service accounts without named owner", "value": service_accounts_without_owner},
            {"metric": "Terminated users with post-termination activity", "value": terminated_users_with_post_term_activity},
            {"metric": "Privileged accounts outside approved group model", "value": privileged_accounts_outside_group_model},
        ],
    )

    write_csv(
        CURATED / "vulnerability_summary.csv",
        ["metric", "value"],
        [
            {"metric": "Open critical vulnerabilities", "value": open_critical_vulns},
            {"metric": "Open high vulnerabilities", "value": open_high_vulns},
            {"metric": "Overdue critical or high findings", "value": overdue_critical_or_high},
            {"metric": "KEV-listed overdue findings", "value": kev_listed_overdue},
            {"metric": "Critical assets with failed backup status", "value": critical_assets_with_failed_backup},
            {"metric": "Failed DR or restore tests without retest", "value": failed_dr_without_retest},
        ],
    )

    write_csv(
        CURATED / "cloud_infra_posture_summary.csv",
        ["metric", "value"],
        [
            {"metric": "Open public cloud exposure findings", "value": open_public_cloud_exposures},
            {"metric": "Production assets with unsupported operating systems", "value": unsupported_os_in_prod},
            {"metric": "Production firewall rules with broad or any-any access", "value": permissive_firewall_rules},
            {"metric": "Assets with missing patches", "value": assets_with_missing_patches},
            {"metric": "Emergency changes without complete review", "value": emergency_changes_without_complete_review},
            {"metric": "Critical assets with failed backup status", "value": critical_assets_with_failed_backup},
        ],
    )

    iam_detail = []

    for row in users:
        if row["employment_status"] == "Active" and row["mfa_enabled"] == "No":
            iam_detail.append({
                "issue_type": "Active user without MFA",
                "user_or_account": row["user_id"],
                "display_name": row["employee_name"],
                "department": row["department"],
                "asset_id": "",
                "asset_name": "",
                "severity": "High" if row["account_type"] == "Privileged" else "Medium",
                "status": "Open",
                "source_table": "user_access"
            })

        if (
            row["employment_status"] == "Terminated"
            and parse_date(row["termination_date"])
            and parse_date(row["last_login_date"])
            and parse_date(row["last_login_date"]) > parse_date(row["termination_date"])
        ):
            iam_detail.append({
                "issue_type": "Post-termination access activity",
                "user_or_account": row["user_id"],
                "display_name": row["employee_name"],
                "department": row["department"],
                "asset_id": "",
                "asset_name": "",
                "severity": "High",
                "status": "Open",
                "source_table": "user_access"
            })

    for row in privileged:
        linked_user = users_by_id.get(row["user_id"], {})
        if parse_date(row["last_used_date"]) and parse_date(row["last_used_date"]) < DORMANT_THRESHOLD:
            iam_detail.append({
                "issue_type": "Dormant privileged account",
                "user_or_account": row["account_name"],
                "display_name": linked_user.get("employee_name", ""),
                "department": linked_user.get("department", ""),
                "asset_id": "",
                "asset_name": "",
                "severity": "High",
                "status": "Open",
                "source_table": "privileged_accounts"
            })

        if row["account_name"].startswith("svc-") and not row["named_owner"].strip():
            iam_detail.append({
                "issue_type": "Service account without named owner",
                "user_or_account": row["account_name"],
                "display_name": "",
                "department": "",
                "asset_id": "",
                "asset_name": "",
                "severity": "High",
                "status": "Open",
                "source_table": "privileged_accounts"
            })

        if row["approved_group_member"] == "No":
            iam_detail.append({
                "issue_type": "Privileged account outside approved group model",
                "user_or_account": row["account_name"],
                "display_name": linked_user.get("employee_name", ""),
                "department": linked_user.get("department", ""),
                "asset_id": "",
                "asset_name": "",
                "severity": "High",
                "status": "Open",
                "source_table": "privileged_accounts"
            })

    write_csv(
        CURATED / "iam_detail.csv",
        ["issue_type", "user_or_account", "display_name", "department", "asset_id", "asset_name", "severity", "status", "source_table"],
        iam_detail,
    )

    vulnerability_detail = []
    for row in vulns:
        asset = assets_by_id.get(row["asset_id"], {})
        if (
            row["status"] == "Open"
            and row["severity"] in {"Critical", "High"}
            and parse_date(row["sla_due_date"]) < REF_DATE
        ):
            vulnerability_detail.append({
                "finding_id": row["finding_id"],
                "asset_id": row["asset_id"],
                "asset_name": asset.get("hostname", ""),
                "business_service": asset.get("business_service", ""),
                "business_criticality": asset.get("business_criticality", ""),
                "internet_facing": asset.get("internet_facing", ""),
                "severity": row["severity"],
                "kev_listed": row["kev_listed"],
                "status": row["status"],
                "sla_due_date": row["sla_due_date"]
            })

    write_csv(
        CURATED / "vulnerability_detail.csv",
        ["finding_id", "asset_id", "asset_name", "business_service", "business_criticality", "internet_facing", "severity", "kev_listed", "status", "sla_due_date"],
        vulnerability_detail,
    )

    cloud_infra_detail = []

    for row in cloud:
        if (
            row["status"] == "Open"
            and row["public_exposure"] == "Yes"
            and row["resource_type"] in PUBLIC_RESOURCE_TYPES
        ):
            cloud_infra_detail.append({
                "issue_type": "Public cloud exposure",
                "resource_or_rule_id": row["resource_id"],
                "platform_or_environment": row["cloud_platform"],
                "severity": row["severity"],
                "status": row["status"],
                "detail": row["policy_name"]
            })

    for row in firewall:
        if (
            row["environment"] == "Production"
            and (
                row["any_any_rule"] == "Yes"
                or row["access_scope"] == "Broad"
                or row["port_protocol"] == "Any/Any"
            )
        ):
            cloud_infra_detail.append({
                "issue_type": "Overly permissive firewall rule",
                "resource_or_rule_id": row["rule_id"],
                "platform_or_environment": row["environment"],
                "severity": "High",
                "status": "Open",
                "detail": row["business_justification"]
            })

    for row in assets:
        if row["environment"] == "Production" and row["os_version"] in UNSUPPORTED_OS:
            cloud_infra_detail.append({
                "issue_type": "Unsupported OS in production",
                "resource_or_rule_id": row["asset_id"],
                "platform_or_environment": row["cloud_platform"],
                "severity": "High" if row["business_criticality"] == "Critical" else "Medium",
                "status": "Open",
                "detail": row["hostname"]
            })

    write_csv(
        CURATED / "cloud_infra_detail.csv",
        ["issue_type", "resource_or_rule_id", "platform_or_environment", "severity", "status", "detail"],
        cloud_infra_detail,
    )

    resilience_detail = []
    for row in dr_logs:
        asset = assets_by_id.get(row["asset_id"], {})
        if row["test_result"] == "Fail" and row["retest_completed"] == "No":
            resilience_detail.append({
                "test_id": row["test_id"],
                "asset_id": row["asset_id"],
                "asset_name": asset.get("hostname", ""),
                "business_service": asset.get("business_service", ""),
                "business_criticality": asset.get("business_criticality", ""),
                "test_type": row["test_type"],
                "test_result": row["test_result"],
                "retest_completed": row["retest_completed"],
                "status": "Open"
            })

    write_csv(
        CURATED / "resilience_detail.csv",
        ["test_id", "asset_id", "asset_name", "business_service", "business_criticality", "test_type", "test_result", "retest_completed", "status"],
        resilience_detail,
    )

    print("Generated curated summary and detail tables in data/curated")


if __name__ == "__main__":
    main()
