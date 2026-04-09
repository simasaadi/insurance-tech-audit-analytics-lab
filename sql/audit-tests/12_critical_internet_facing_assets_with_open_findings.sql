-- Critical internet-facing assets with open findings
-- Objective: identify critical internet-facing assets that still have open high-risk vulnerability findings

SELECT
    ai.asset_id,
    ai.hostname,
    ai.business_service,
    ai.business_criticality,
    ai.internet_facing,
    vf.finding_id,
    vf.severity,
    vf.cve_id,
    vf.kev_listed,
    vf.status,
    vf.sla_due_date
FROM asset_inventory ai
INNER JOIN vulnerability_findings vf
    ON ai.asset_id = vf.asset_id
WHERE ai.business_criticality = 'Critical'
  AND ai.internet_facing = 'Yes'
  AND vf.status = 'Open'
  AND vf.severity IN ('Critical', 'High')
ORDER BY ai.hostname, vf.severity;
