-- High-risk vulnerabilities past SLA
-- Objective: identify open critical/high findings past remediation deadline

SELECT
    vf.finding_id,
    vf.asset_id,
    ai.hostname,
    ai.business_service,
    ai.business_criticality,
    ai.internet_facing,
    vf.severity,
    vf.cve_id,
    vf.kev_listed,
    vf.status,
    vf.date_identified,
    vf.sla_due_date
FROM vulnerability_findings vf
LEFT JOIN asset_inventory ai
    ON vf.asset_id = ai.asset_id
WHERE vf.status = 'Open'
  AND vf.severity IN ('Critical', 'High')
  AND vf.sla_due_date < DATE '2026-04-07'
ORDER BY vf.severity, vf.sla_due_date;
