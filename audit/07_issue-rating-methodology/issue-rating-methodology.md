# Issue Rating Methodology

## Purpose
This methodology assigns a consistent severity rating to audit issues identified through control testing.

## Rating Factors
Each issue is assessed using the following factors:
- Control impact
- Business criticality
- Data sensitivity
- Internet exposure
- Privilege level
- Compensating controls
- Duration / aging
- Regulatory or financial-services relevance

## Rating Definitions

### High
Issue affects a critical control area, involves privileged access or critical assets, has no effective compensating control, or creates material cyber / operational risk.

### Medium
Issue reflects a meaningful control weakness with manageable impact, partial compensating controls, or lower criticality exposure.

### Low
Issue is isolated, low impact, and unlikely to materially affect risk outcomes.

## Escalation Guidance
- High issues require formal management action plan and target remediation date.
- Medium issues require accountable owner and remediation tracking.
- Low issues should be corrected through routine operational follow-up.

## Examples
- Privileged admin account with no approved group and stale usage on a production environment: High
- Active employee without MFA on a non-critical internal function: Medium
- Documentation gap with low operational impact: Low
