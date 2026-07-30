# Final Review and Open Items

**Version:** v2
**Purpose:** A single place to see what is complete, what has been decided, and what remains to be done before and after the proposal is submitted. This version records the decisions returned by the Principal Investigators.

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
| 7 | Contributor Guide (consolidated into CONTRIBUTING) | Complete |
| 8 | Beta tracking template, feedback form, one-pager | Complete; feedback form is built and linked |
| 9 | Final review and open items | This document |

A full index of every deliverable and where to find it is in `DELIVERABLES_INDEX.md`.

## 2. What was added to the dashboard

The dashboard previously presented summary charts with no way to reach the records behind them. The following interactivity was added so that a visitor can move from a headline figure down to the underlying data.

- **Cable explorer** on the System Overview page: search, filter by status and by supplier or owner bloc, sortable columns, and an expandable detail view for each cable showing owners, suppliers, landing points, and source.
- **Clickable market share bars** on the System Overview and Market Structure pages: selecting a bloc filters the explorer to exactly those cables.
- **Policy and regulation filters**: the jurisdiction filter is now built from the data itself and includes a search box.

## 3. Decisions from the Principal Investigators

These points were raised for decision and have now been resolved. Two items are pending external confirmation, as noted.

**3.1 Beta sign-up recipients.** Resolved. The project team will monitor and follow up on new sign-ups.

**3.2 License copyright holder.** The copyright line has been updated to the full platform name, "Global Digital Infrastructure Political Economy Observatory, Northeastern University," so it is consistent across the repository. The separate question of the correct copyright holder under the university's intellectual property policy is being confirmed with the office that would know, in a separate message.

**3.3 Landing page.** Resolved. The site will continue to open on the About page, with the dashboard one click away.

**3.4 Team representation.** Resolved. The current presentation is confirmed: Prof. Tsai as PI, Prof. Shen as Co-PI, with current team members listed.

**3.5 Interactive dashboard wording.** Resolved. The wording is confirmed as accurate now that the explorer and filters are in place.

**3.6 Indicator definitions.** Confirmation has been requested by email from the former research assistant who designed the indicators, with the Co-PI copied. The Data Dictionary will be treated as final once that confirmation is received.

**3.7 Bloc grouping consistency.** Confirmation of whether the two bloc groupings are intended to differ or should be aligned has been requested from the same person, with the Co-PI copied.

**3.8 Multi-model comparison.** Approved. The two-model cross-check will be built into the pipeline, pairing Claude with a model from a different provider so that agreement between them is a meaningful signal.

## 4. Requirements before the repository is made public

The Principal Investigators have confirmed that the platform must actually match its documentation before the repository is opened. Several documents now describe the following as done, so each must be verified and genuinely in place first.

**4.1 Row-level security.** Row-level security must be enabled on the database, with read-only access for the public key, so that the public dashboard can read the data but not modify it. This is now described as done in the documentation and must be confirmed.

**4.2 Weekly pipeline schedule.** Both the cable and policy pipelines must be confirmed running on the weekly schedule, matching the documentation. The policy scraping scenario in particular should be checked, since it previously carried a leftover high-frequency schedule from testing.

**4.3 Commit history.** The full commit history must be scanned for any keys or credentials before the repository is made public, and anything sensitive removed and rotated.

**4.4 Repository transfer.** The repository should be transferred to an institutional or organization account and then made public, with the placeholder URLs in the documentation updated to match.

## 5. Other known items

**5.1 Account ownership.** Hosting, database, and one API account have been tied to personal accounts. Moving these onto institutional or project-owned accounts removes a continuity risk and is recommended regardless of the proposal.

**5.2 Reimbursement.** The former research assistant paid $53.13 for API credits on a personal card in April 2026. If this has not been reimbursed, it should be.

## 6. Suggested next steps

In rough priority order:

1. Confirm the indicator definitions and bloc grouping with the former research assistant, then finalize the Data Dictionary.
2. Confirm row-level security is enabled and both pipelines are on the weekly schedule.
3. Scan the commit history, transfer the repository to an institutional account, and make it public.
4. Build the multi-model cross-check into the pipeline.
5. Confirm the correct license copyright holder and update the notice if needed.
6. Continue adding interactivity to the remaining dashboard pages, in particular a time range control on Temporal Dynamics.
7. Begin scoping the next phase, extending the framework to data centers and 5G networks.

## 7. Cost summary

A full one-year cost estimate has been provided separately. In short, the platform costs roughly $1,100 per year to operate, dominated by platform subscriptions rather than AI usage, and requesting approximately $2,000 is recommended to leave headroom for deeper data collection and growth.
