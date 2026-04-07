-- Segmentation exceptions or overly permissive firewall rules
-- Objective: identify production rules with broad or any-any access

SELECT
    rule_id,
    environment,
    source_zone,
    destination_zone,
    port_protocol,
    access_scope,
    any_any_rule,
    business_justification,
    review_status
FROM firewall_rules
WHERE environment = 'Production'
  AND (any_any_rule = 'Yes' OR access_scope = 'Broad' OR port_protocol = 'Any/Any')
ORDER BY any_any_rule DESC, review_status, rule_id;
