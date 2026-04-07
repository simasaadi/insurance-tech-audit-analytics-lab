-- Stale access not removed after termination date
-- Objective: identify terminated users with login activity after termination

SELECT
    user_id,
    employee_name,
    department,
    job_title,
    employment_status,
    termination_date,
    last_login_date,
    access_group,
    account_type
FROM user_access
WHERE employment_status = 'Terminated'
  AND termination_date IS NOT NULL
  AND last_login_date > termination_date
ORDER BY termination_date;
