-- Users without MFA
-- Objective: identify active users missing MFA coverage

SELECT
    user_id,
    employee_name,
    department,
    job_title,
    employment_status,
    mfa_enabled,
    access_group,
    account_type
FROM user_access
WHERE employment_status = 'Active'
  AND mfa_enabled = 'No'
ORDER BY department, employee_name;
