-- Dormant privileged accounts
-- Objective: identify privileged accounts unused for more than 60 days

SELECT
    account_id,
    user_id,
    account_name,
    privilege_type,
    approved_group_member,
    named_owner,
    last_used_date
FROM privileged_accounts
WHERE last_used_date < DATE '2026-02-06'
ORDER BY last_used_date;
