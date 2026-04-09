-- Admin rights assigned outside approved groups
-- Objective: identify elevated accounts not assigned through the approved group-based access model

SELECT
    pa.account_id,
    pa.user_id,
    pa.account_name,
    pa.privilege_type,
    pa.approved_group_member,
    pa.named_owner,
    ua.employee_name,
    ua.department,
    ua.job_title,
    ua.employment_status
FROM privileged_accounts pa
LEFT JOIN user_access ua
    ON pa.user_id = ua.user_id
WHERE pa.approved_group_member = 'No'
ORDER BY pa.privilege_type, pa.account_name;
