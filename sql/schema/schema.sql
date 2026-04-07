CREATE TABLE user_access (
    user_id VARCHAR,
    employee_name VARCHAR,
    department VARCHAR,
    job_title VARCHAR,
    employment_status VARCHAR,
    termination_date DATE,
    mfa_enabled VARCHAR,
    last_login_date DATE,
    access_group VARCHAR,
    account_type VARCHAR
);

CREATE TABLE privileged_accounts (
    account_id VARCHAR,
    user_id VARCHAR,
    account_name VARCHAR,
    privilege_type VARCHAR,
    approved_group_member VARCHAR,
    named_owner VARCHAR,
    last_used_date DATE
);

CREATE TABLE asset_inventory (
    asset_id VARCHAR,
    hostname VARCHAR,
    environment VARCHAR,
    cloud_platform VARCHAR,
    business_service VARCHAR,
    business_criticality VARCHAR,
    internet_facing VARCHAR,
    os_version VARCHAR,
    backup_status VARCHAR
);

CREATE TABLE vulnerability_findings (
    finding_id VARCHAR,
    asset_id VARCHAR,
    severity VARCHAR,
    cve_id VARCHAR,
    kev_listed VARCHAR,
    status VARCHAR,
    date_identified DATE,
    sla_due_date DATE,
    date_closed DATE
);
