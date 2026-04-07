# ISS-001: Stale and Weakly Governed Privileged Accounts

## Rating
High

## Observation
Multiple privileged accounts were identified as dormant or outside the approved admin-group model. At least one privileged account was linked to a terminated user, and one cloud/infrastructure admin account showed stale usage with no evidence of timely recertification.

## Risk
Excessive or stale privileged access increases the risk of unauthorized administrative activity, delayed deprovisioning, and misuse of elevated rights in a production environment.

## Root Cause
Periodic privileged-access recertification was not consistently enforced, and deprovisioning controls did not fully align with privileged account inventories.

## Recommendation
Implement monthly privileged-access review, enforce approved-group membership, remove dormant accounts, and reconcile privileged inventories against HR termination and transfer events.

## Management Action
Infrastructure Security management will review all privileged accounts, remove stale access, and document accountable ownership for each elevated account.
