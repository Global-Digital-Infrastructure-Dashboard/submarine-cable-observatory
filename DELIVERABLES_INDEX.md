# Deliverables Index

**Version:** v1
**Purpose:** Every PESOSE deliverable, what it is, and where to find it.

**Repository:** [GITHUB URL, PLACEHOLDER, PENDING TRANSFER TO INSTITUTIONAL ACCOUNT AND PUBLIC RELEASE]
**Live site:** https://research-platform-sand.vercel.app/

Everything below is public. No login is required for any deliverable.

## 1. GitHub documentation

| Deliverable | Where |
|---|---|
| README | `README.md` in the repository root |
| Contributing guide | `CONTRIBUTING.md` (includes all six ways to contribute in full detail) |
| Roadmap | `roadmap.md` |
| License (MIT) | `LICENSE` |

The README covers the project overview, motivation, screenshots, dashboard link, an explanation of the AI workflow, the team, and setup instructions.

## 2. Project website

| Deliverable | Where |
|---|---|
| Public site | https://research-platform-sand.vercel.app/ |

The site opens on an About page covering what the project is, why it matters, data coverage, how it works, the team, an FAQ, and beta sign-up. The dashboard is part of the same site, reachable from the navigation.

## 3. Visual documentation

| Deliverable | Where |
|---|---|
| Architecture diagram | On the About page under "How it works", and in the repository at `public/architecture.svg` |
| FAQ | On the About page |

## 4. Data Dictionary

| Deliverable | Where |
|---|---|
| Data Dictionary v1 | `DATA_DICTIONARY.md` in the repository, plus a Word copy sent by email |

Documents all 19 variables in the cable dataset and every computed dashboard indicator, with definitions, what each measures, sources, coding rules, and possible values.

## 5. Workflow Documentation

| Deliverable | Where |
|---|---|
| Workflow Documentation v1 | `WORKFLOW_DOCUMENTATION.md` in the repository, plus a Word copy sent by email |

Covers all seven pipeline stages from source discovery to dashboard display, with the quality-control points identified. The workflow figure is the architecture diagram referenced above.

## 6. Governance Framework

| Deliverable | Where |
|---|---|
| Governance Framework v1 | `GOVERNANCE_FRAMEWORK.md` in the repository, plus a Word copy sent by email |

## 7. Community engagement materials

| Deliverable | Where |
|---|---|
| Beta user tracking template | Sent by email as an Excel file. Not committed to the repository, because it holds contact details |
| User feedback form | Live [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSe4hQcIMxplSJR44xBjhGSWRCcukj8hlWhWNH8WxJS8C5xj9g/viewform); specification and question set at `USER_FEEDBACK_FORM.md` |
| Project one-pager | `PROJECT_ONEPAGER.md` in the repository, plus a Word copy sent by email |
| Beta sign-up form | Google Form, already shared with the PI and Co-PI's Northeastern and personal email addresses |

## 8. Supporting material

| Item | Where |
|---|---|
| One-year cost estimate | Sent by email. Approximately $1,100 per year to operate; roughly $2,000 recommended for the budget request |

## Accounts behind the platform

These are not deliverables, but they are the services the platform runs on. Each needs an account login rather than a public link, so access is best arranged directly rather than by email.

| Service | Purpose |
|---|---|
| Vercel | Hosts the public website and dashboard |
| Supabase | PostgreSQL database holding the cable and policy records |
| Make.com | Runs the four automation pipelines |
| Google Sheets | Review queues sitting between AI extraction and the database |
| Perplexity and Claude APIs | Source discovery and extraction |
