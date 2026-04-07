# Control Universe

## Purpose
This document defines the core technology control areas covered by the audit engagement and aligns them to a practical control-testing structure.

## Organizing Framework
The control universe is organized using NIST CSF 2.0 style logic:
- Govern
- Identify
- Protect
- Detect
- Respond
- Recover

## Control Domains

### Govern
- Security policy and standards alignment
- Exception governance
- Issue ownership and remediation tracking
- Change approval and review discipline

### Identify
- Asset inventory completeness
- Application criticality classification
- Vulnerability identification processes
- Cloud posture visibility
- Account and entitlement inventory

### Protect
- MFA enforcement
- Privileged-access governance
- Service-account ownership
- Firewall rule governance
- Secure configuration / supported OS baseline
- Public exposure restrictions for cloud resources

### Detect
- Vulnerability aging monitoring
- Detection of stale privileged accounts
- Detection of access after termination
- Monitoring of backup failures
- Review of broad or unreviewed firewall rules

### Respond
- Escalation of overdue vulnerabilities
- Follow-up on access control exceptions
- Management action planning
- Exception register maintenance

### Recover
- Backup success monitoring
- Disaster recovery testing
- Retest validation after failed restore or DR exercises

## Control Objectives Mapped to Current Tests

| Test ID | Test Name | Primary Control Objective |
|---|---|---|
| T001 | Dormant Privileged Accounts | Elevated accounts should be actively governed and periodically reviewed |
| T002 | Users Without MFA | Active users should be protected by strong authentication |
| T003 | Service Accounts Without Owner | Privileged service accounts must have accountable ownership |
| T004 | High-Risk Vulnerabilities Past SLA | Severe vulnerabilities should be remediated within required timeframes |
| T005 | Stale Access After Termination | Logical access should be removed promptly after termination |
| T006 | Unsupported OS in Production | Production systems should remain on supported platforms |
| T007 | Backup Failures on Critical Assets | Critical services should have reliable backup protection |
| T008 | Failed DR Tests Without Retest | Recovery failures should be retested and evidentially closed |
| T009 | Public or Overly Broad Storage Policies | Public cloud exposure should be restricted and controlled |
| T010 | Overly Permissive Firewall Rules | Network access rules should be justified and periodically reviewed |

## Notes
This control universe is intentionally written in plain operational language so that it reads like a technology audit planning document rather than a pure cybersecurity reference sheet.
