# Insurance Tech Audit Analytics Lab

Technology audit engagement simulator for a synthetic Canadian insurance environment covering IAM, cloud security, vulnerability management, control testing, and executive reporting.

[![Launch Streamlit Dashboard](https://img.shields.io/badge/Launch-Streamlit%20Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://insurance-tech-audit-analytics-lab.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-Project-3776AB?logo=python&logoColor=white)](./)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

## Live dashboard

The interactive public demo for this project is here:

**[Open the Streamlit dashboard](https://insurance-tech-audit-analytics-lab.streamlit.app/)**

## Project overview

This repo simulates a technology audit engagement for a synthetic Canadian insurer. It is designed to demonstrate how audit analytics, control testing, synthetic enterprise data, and executive reporting can be combined in one portfolio project.

Instead of presenting a generic cyber lab, this repo is framed as a structured risk-and-controls analytics engagement.

## Simulated company

**NorthStar Life Insurance**

A synthetic cloud-first insurer operating claims, policy administration, finance reporting, and customer-facing services across Azure, AWS, and supporting infrastructure platforms.

## What this repo demonstrates

- internal audit analytics
- IAM control testing
- cloud and infrastructure security review
- vulnerability management and resilience analysis
- framework mapping to recognized control standards
- curated reporting outputs for dashboard development
- Streamlit-based executive dashboarding for public demo
- Power BI-ready curated outputs and build guidance

## Repository components

### Audit planning and governance
- audit charter
- risk assessment summary
- control universe
- risk-control matrix
- evidence request list
- testing strategy
- issue rating methodology
- management action plan

### Synthetic datasets
- user access
- privileged accounts
- asset inventory
- vulnerabilities
- patching
- firewall rules
- cloud posture findings
- backup and DR tests
- change tickets
- application inventory

### SQL audit tests
- dormant privileged accounts
- users without MFA
- service accounts without owner
- stale access after termination
- overdue vulnerabilities
- unsupported OS in production
- failed DR tests without retest
- public cloud exposure
- overly permissive firewall rules

### Reporting and documentation
- workpapers
- framework mapping
- curated summary and detail tables
- Streamlit dashboard
- Power BI-ready curated outputs and build guidance

## Dashboard pages

The Streamlit app currently includes:

- Audit Overview
- IAM Review
- Vulnerability Management
- Cloud & Infrastructure
- Resilience

## Data flow

See `docs/repo-architecture.md` for the repo structure and reporting flow.

## Run locally

### 1. Install requirements
```bash
pip install -r requirements.txt
2. Generate curated outputs
python scripts/data-generation/generate_data.py
3. Run QA checks
python scripts/qa-checks/qa_checks.py
4. Launch the dashboard
streamlit run app.py
Why this project matters

This repo is designed to look like a real technology audit analytics engagement rather than a generic cyber lab. It combines:

structured audit planning
synthetic enterprise data
SQL control testing
formal workpapers
framework mapping
interactive dashboard delivery
License

MIT