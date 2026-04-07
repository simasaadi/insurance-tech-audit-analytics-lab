# Insurance Tech Audit Analytics Lab

Technology audit engagement simulator for a synthetic Canadian insurance environment.

## Simulated Company
NorthStar Life Insurance

## What this repo demonstrates
- internal audit analytics
- IAM control testing
- cloud and infrastructure security review
- vulnerability and resilience testing
- framework mapping
- dashboard-ready reporting outputs

## Main repo components
### Audit planning and governance
- audit charter
- risk assessment summary
- control universe
- risk-control matrix
- evidence request list
- testing strategy
- issue rating methodology
- management action plan

### Synthetic datasets
- user access
- privileged accounts
- asset inventory
- vulnerabilities
- patching
- firewall rules
- cloud posture findings
- backup and DR tests
- change tickets
- application inventory

### SQL audit tests
- dormant privileged accounts
- users without MFA
- service accounts without owner
- stale access after termination
- overdue vulnerabilities
- unsupported OS in production
- failed DR tests without retest
- public cloud exposure
- overly permissive firewall rules

### Reporting and documentation
- workpapers
- framework mapping
- curated summary tables
- Power BI dashboard pack guidance

## Data flow
See docs/repo-architecture.md for the repo flow and structure.

## Run locally
python scripts/data-generation/generate_data.py
python scripts/qa-checks/qa_checks.py
