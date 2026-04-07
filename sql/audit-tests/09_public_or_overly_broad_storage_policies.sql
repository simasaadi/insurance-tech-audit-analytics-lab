-- Public storage or overly broad access policies
-- Objective: identify high-risk cloud posture findings involving public exposure

SELECT
    finding_id,
    cloud_platform,
    resource_id,
    resource_type,
    control_area,
    severity,
    status,
    public_exposure,
    policy_name
FROM cloud_posture_findings
WHERE status = 'Open'
  AND public_exposure = 'Yes'
  AND resource_type IN ('Storage Account', 'S3 Bucket', 'EC2 Instance')
ORDER BY severity, resource_id;
