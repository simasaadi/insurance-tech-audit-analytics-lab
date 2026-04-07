-- Unsupported OS versions in production
-- Objective: identify production assets using legacy operating systems

SELECT
    asset_id,
    hostname,
    environment,
    cloud_platform,
    business_service,
    business_criticality,
    internet_facing,
    os_version,
    backup_status
FROM asset_inventory
WHERE environment = 'Production'
  AND os_version IN ('Windows Server 2012', 'Windows Server 2016', 'Ubuntu 18.04')
ORDER BY business_criticality, hostname;
