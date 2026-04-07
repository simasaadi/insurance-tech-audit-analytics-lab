# Repository Architecture

## End-to-End Flow
data/seeds -> scripts/data-generation -> data/curated
data/seeds -> sql/audit-tests -> workpapers
sql/audit-tests -> framework-mapping
data/curated -> dashboards/powerbi

## Structure
- data/seeds: source datasets
- sql/audit-tests: audit SQL logic
- scripts: generation and QA checks
- audit: planning and governance documents
- workpapers: exceptions, issues, and action plans
- framework-mapping: standards crosswalk
- data/curated: Power BI-ready outputs
- dashboards/powerbi: dashboard build guidance
