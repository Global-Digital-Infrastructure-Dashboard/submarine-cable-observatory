# Final Review and Open Items

**Version:** v1
**Purpose:** A single place to see what is complete, what still needs a decision from the Principal Investigators, and what remains to be done before and after the proposal is submitted.

## 1. Status at a glance

All of the deliverables on the July task list have a first version in place. The documentation is drafted and in the repository, the public website is live, and the dashboard has been made substantially more interactive.

| # | Deliverable | Status |
|---|-------------|--------|
| 1 | GitHub documentation (README, CONTRIBUTING, roadmap) | Complete |
| 2 | Project website | Live |
| 3 | Architecture diagram and FAQ | Complete |
| 4 | Data Dictionary | Complete, pending indicator confirmation (see 3.6) |
| 5 | Workflow Documentation | Complete |
| 6 | Governance Framework | Complete |
| 7 | Contributor Guide | Complete |
| 8 | Beta tracking template, feedback form, one-pager | Templates complete; feedback form to be built as a Google Form |
| 9 | Final review and open items | This document |

A full index of every deliverable and where to find it is in `DELIVERABLES_INDEX.md`.

## 2. What was added to the dashboard

The dashboard previously presented summary charts with no way to reach the records behind them. The following interactivity was added so that a visitor can move from a headline figure down to the underlying data.

- **Cable explorer** on the System Overview page: search, filter by status and by supplier or owner bloc, sortable columns, and an expandable detail view for each cable showing owners, suppliers, landing points, and source. This works on the full dataset the page already loads.
- **Clickable market share bars**: selecting a bloc filters the explorer to exactly those cables, so the specific cables behind a percentage are one click away.
- **Policy and regulation filters**: the jurisdiction filter previously used a fixed list that left several jurisdictions in the data unreachable. It is now built from the data itself and includes a search box.

This directly addresses the concern that the dashboard was described as interactive without fully being so.

## 3. Decisions needed from you

These are the points where a decision from the Principal Investigators would let the work move forward or be finalized.

**3.1 Beta sign-up recipients.** The beta sign-up form is live and collecting responses in a linked spreadsheet. Please confirm who should receive or monitor new sign-ups so that they can be followed up promptly.

**3.2 License copyright holder.** The repository uses the MIT License, with the copyright line currently reading "Digital Infrastructure Observatory, Northeastern University." Please confirm whether the university's intellectual property policy requires a specific holder, so the notice can be set correctly before wider release.

**3.3 Landing page.** The website currently opens on the About page, with the dashboard one click away. If you would prefer visitors to land directly on the dashboard, that is a small change. Please confirm the preference.

**3.4 Team representation.** The team is listed with both Principal Investigators as Co-PIs and both research assistants by name. Please confirm this is how you would like the team presented on a public, proposal-facing page, including whether to note current versus former status.

**3.5 Scope of the "interactive dashboard" claim.** With the explorer and filters now in place, the site's description of an interactive dashboard is now accurate. Please confirm you are comfortable with the wording as it stands, or let me know if you would like it softened further.

**3.6 Indicator definitions.** The Data Dictionary documents the Sovereignty Index, the concentration measure, and the bloc classifications. These definitions were reconstructed by reading the analysis scripts, since the indicators were originally built by Sowrathi. Her confirmation of the exact weights and intent would make these authoritative. This is the single most important item to close before the Data Dictionary is treated as final.

**3.7 Bloc grouping consistency.** There are currently two bloc groupings in the system. The stored data uses Western, Chinese, Mixed, Other, and Unknown, assigned during ingestion. The sovereignty analysis recomputes a finer grouping (US, Europe, Japan, China, India) from the country fields. Because the bloc scheme determines the market share, concentration, and sovereignty figures, please confirm whether the two groupings are intended to differ or should be aligned.

**3.8 Multi-model comparison.** The design for the two-model cross-check is ready. The proposed pairing is Claude with a model from a different provider, so that agreement between them is a meaningful signal. Please confirm the pairing and whether to proceed with building it into the pipeline.

## 4. Known issues and technical notes

These do not require a decision, but they should be on the record.

**4.1 Account ownership.** Key services have been tied to personal accounts rather than institutional ones. Hosting has been moved to a personal account through a claim transfer, and the database and one API account remain on a departed researcher's personal accounts. Moving these onto institutional or project-owned accounts would remove a continuity risk and is recommended regardless of the proposal.

**4.2 Reimbursement.** The former research assistant paid $53.13 for API credits on a personal card in April 2026. If this has not been reimbursed, it should be.

**4.3 Database access hardening.** Before the platform is promoted for wide public use, row-level security should be enabled on the database with read-only access for the public key, so that the public dashboard can read the data but not modify it.

**4.4 Policy pipeline schedule.** The policy scraping scenario carries a leftover high-frequency schedule from testing. This should be set to the weekly cadence before it is activated, to avoid unnecessary operations and API cost.

**4.5 Feedback form.** The content of the user feedback form is written and documented. It still needs to be built as a Google Form and linked from the site and the repository, in the same way as the beta sign-up form.

## 5. Suggested next steps

In rough priority order, after the proposal groundwork is set:

1. Confirm the indicator definitions with Sowrathi and finalize the Data Dictionary.
2. Build the user feedback form as a Google Form.
3. Enable row-level security on the database ahead of any wider launch.
4. Migrate hosting, database, and API billing onto institutional accounts.
5. Build the multi-model cross-check into the pipeline, once the model pairing is confirmed.
6. Continue adding interactivity to the remaining dashboard pages, in particular a time range control on Temporal Dynamics.
7. Begin scoping the next phase, extending the framework to data centers and 5G networks.

## 6. Cost summary

A full one-year cost estimate has been provided separately. In short, the platform costs roughly $1,100 per year to operate, dominated by platform subscriptions rather than AI usage, and requesting approximately $2,000 is recommended to leave headroom for deeper data collection and growth.
