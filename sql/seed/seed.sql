-- DuckDB / PostgreSQL-style seed loader reference

-- user_access
SELECT * FROM read_csv_auto('data/seeds/user_access.csv', header=True);

-- privileged_accounts
SELECT * FROM read_csv_auto('data/seeds/privileged_accounts.csv', header=True);

-- asset_inventory
SELECT * FROM read_csv_auto('data/seeds/asset_inventory.csv', header=True);

-- vulnerability_findings
SELECT * FROM read_csv_auto('data/seeds/vulnerability_findings.csv', header=True);
