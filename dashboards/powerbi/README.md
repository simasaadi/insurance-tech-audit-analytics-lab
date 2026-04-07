# Power BI Dashboard Pack

## Pages
1. Audit Overview
2. IAM Review
3. Vulnerability Management
4. Cloud and Infrastructure Posture

## Source Tables
- data/curated/audit_overview_summary.csv
- data/curated/iam_review_summary.csv
- data/curated/vulnerability_summary.csv
- data/curated/cloud_infra_posture_summary.csv

## Suggested visuals

### Audit Overview
- Open findings by domain
- Findings by severity
- Issues by control area

### IAM Review
- Users without MFA
- Dormant privileged accounts
- Service accounts without named owner
- Privileged accounts outside approved group model

### Vulnerability Management
- Overdue findings
- Critical and KEV-listed exposure
- Backup / DR exceptions
- SLA breach indicators

### Cloud and Infrastructure Posture
- Public exposure findings
- Unsupported OS in production
- Broad firewall rules
- Patch and change-control exceptions
