-- Service accounts without named owner
-- Objective: identify privileged service accounts with no accountable owner

SELECT
    account_id,
    account_name,
    privilege_type,
    approved_group_member,
    named_owner,
    last_used_date
FROM privileged_accounts
WHERE account_name LIKE 'svc-%'
  AND (named_owner IS NULL OR TRIM(named_owner) = '')
ORDER BY account_name;
