# Risk Assessment Summary

## Engagement
Technology Audit Analytics Review - Identity, Cloud, and Infrastructure Controls

## Entity
NorthStar Life Insurance

## Purpose
This risk assessment summarizes the highest-priority technology and cyber risks addressed by the audit analytics procedures in this repository. The assessment is designed for a synthetic Canadian insurance environment operating across Azure, AWS, and supporting infrastructure platforms.

## Risk Assessment Approach
Risks were prioritized using the following factors:
- Privileged access exposure
- Customer or regulated data exposure
- Business criticality of affected applications and assets
- Internet exposure
- Weakness in preventive or detective controls
- Aging / duration of unresolved issues
- Recovery and resilience implications
- Financial-services regulatory relevance

## High-Priority Risk Areas

### 1. Identity and Access Management
Improperly governed privileged access, missing MFA, stale access after termination, and weak service-account ownership can lead to unauthorized access or control failure across critical systems.

### 2. Vulnerability Management
Critical and high-severity vulnerabilities that remain open past SLA increase exploitation risk, especially on business-critical or internet-facing assets.

### 3. Cloud Security Posture
Publicly exposed storage or compute resources, weak policy enforcement, and misconfigured cloud services can expose sensitive insurer systems and data.

### 4. Infrastructure and Network Security
Legacy operating systems, broad firewall rules, and inconsistent asset hardening increase operational and cyber risk across production services.

### 5. Backup and Disaster Recovery Resilience
Failed backups or DR tests without retest evidence reduce confidence that critical services can be restored when needed.

## Residual Risk Themes Identified in This Repo
- Access governance gaps
- Weak lifecycle management for accounts and assets
- Aging remediation items
- Limited evidence of retesting or closure validation
- Exposure concentration in critical and customer-facing services

## Overall Risk Conclusion
The simulated environment reflects a moderate-to-high technology control risk profile, with the most significant exposure concentrated in IAM, vulnerability remediation, cloud exposure, and resilience validation. These areas therefore drive the testing strategy and issue prioritization used across the repo.
