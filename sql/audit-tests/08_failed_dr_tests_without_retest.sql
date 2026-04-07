-- Failed DR tests with no retest evidence
-- Objective: identify failed backup or DR tests with no retest completed

SELECT
    b.test_id,
    b.asset_id,
    a.hostname,
    a.business_service,
    a.business_criticality,
    b.test_type,
    b.test_date,
    b.test_result,
    b.retest_completed,
    b.retest_date
FROM backup_dr_test_logs b
LEFT JOIN asset_inventory a
    ON b.asset_id = a.asset_id
WHERE b.test_result = 'Fail'
  AND b.retest_completed = 'No'
ORDER BY b.test_date;
