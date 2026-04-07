-- Backup failures on critical systems
-- Objective: identify critical assets with failed backup status

SELECT
    asset_id,
    hostname,
    business_service,
    business_criticality,
    cloud_platform,
    backup_status
FROM asset_inventory
WHERE business_criticality = 'Critical'
  AND backup_status = 'Failed'
ORDER BY hostname;
