# Testing Strategy

## Objective
Define how control testing will be executed across identity, cloud, infrastructure, vulnerability, and resilience domains using synthetic enterprise datasets and SQL-based audit procedures.

## Testing Method
This repository uses analytics-based control testing. The approach is:
1. Build realistic synthetic datasets for the NorthStar Life Insurance environment
2. Define control objectives and risk statements
3. Execute SQL procedures against full-population datasets where feasible
4. Record exceptions in structured workpapers
5. Convert material exceptions into sample audit issues and management actions
6. Summarize outputs for dashboard reporting and framework mapping

## Data Sources Used
- user_access.csv
- privileged_accounts.csv
- asset_inventory.csv
- vulnerability_findings.csv
- patching_status.csv
- firewall_rules.csv
- cloud_posture_findings.csv
- backup_dr_test_logs.csv
- change_tickets.csv
- application_inventory.csv

## Testing Principles
- Prefer full-population testing over small samples when data is structured
- Prioritize critical, internet-facing, and privileged assets/accounts
- Align exceptions to a risk statement and control objective
- Distinguish between observation, root cause, risk, and action
- Preserve an audit-ready trail from dataset to SQL test to issue writeup

## Current Test Coverage

### IAM
- T001 Dormant Privileged Accounts
- T002 Users Without MFA
- T003 Service Accounts Without Owner
- T005 Stale Access After Termination

### Vulnerability and Patch Management
- T004 High-Risk Vulnerabilities Past SLA

### Infrastructure and Network Security
- T006 Unsupported OS in Production
- T009 Public or Overly Broad Storage Policies
- T010 Overly Permissive Firewall Rules

### Resilience
- T007 Backup Failures on Critical Assets
- T008 Failed DR Tests Without Retest

## Exception Handling Logic
Exceptions identified through SQL tests are:
- recorded in the exception register
- evaluated using the issue rating methodology
- escalated into issue writeups when risk is material
- tracked through the management action plan where appropriate

## Reporting Outputs
Testing results are intended to support:
- audit planning documentation
- issue summaries
- framework crosswalks
- dashboard-ready summary tables
- executive-style reporting views

## Future Expansion
Future repo phases can expand testing into:
- admin rights outside approved groups
- toxic access combinations
- patching exceptions by maintenance window
- change-management exceptions tied to high-risk assets
- cloud posture trend analysis
