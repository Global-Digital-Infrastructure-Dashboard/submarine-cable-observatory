# Governance Framework

**Version:** v1
**Purpose:** How the Global Digital Infrastructure Political Economy Observatory is maintained, how the data is kept reliable, and how decisions about the dataset are made as the project grows.

## Principles

The project is built on three commitments.

**Transparency.** The data pipeline, the review process, the variable definitions, and the source code are all publicly documented. Any published value can be traced to the source it came from.

**Human accountability.** Automated extraction proposes; a researcher decides. No record reaches the public dataset without a person approving it.

**Openness with stewardship.** Anyone may use the data and propose corrections. A defined maintainer group is responsible for accepting changes, so that openness does not come at the cost of reliability.

## Roles and responsibilities

**Principal Investigators.** Set research direction and scope, approve changes to the data model and to indicator definitions, and hold final authority on what the project publishes.

**Research assistants.** Operate the pipeline, review and approve records in the queue, respond to reported issues, and maintain the documentation.

**Contributors.** Anyone outside the project team who reports an error, submits a source, suggests an indicator, or contributes code or documentation. Contributors do not have direct write access to the dataset.

## Maintaining the core dataset

The dataset is maintained by the project team at Northeastern University. Records enter the dataset only through the reviewed pipeline described in the Workflow Documentation. Direct edits to the production database are reserved for corrections that cannot be routed through the pipeline, and any such edit is recorded in the affected record's notes field.

Write access to the database is limited to the project team. The public dashboard reads the data through a public key with row-level security enabled, granting read-only access.

## Suggesting a correction

Corrections can be raised in two ways.

**GitHub issues** are the preferred route for anyone comfortable with the platform, because the discussion stays attached to the record of the change.

**The user feedback form** is available for users who would rather not use GitHub, and is linked from the project website.

A useful correction identifies the specific record, states what is wrong, gives the correct value where known, and cites a source. Corrections without a source can still be reported, and the team will attempt to verify them.

## How corrections are reviewed

1. **Acknowledgement.** Reports are triaged by a research assistant.
2. **Verification.** The claim is checked against the cited source and, where possible, at least one independent source. Cable ownership and supplier information in particular is often reported inconsistently across outlets.
3. **Decision.** The correction is accepted, rejected with an explanation, or held pending better evidence.
4. **Application.** Accepted corrections are applied to the database, and the record's notes field is updated with the change, the date, and the reason.
5. **Closure.** The reporter is told the outcome.

Where sources genuinely conflict, the project records the discrepancy in the notes field rather than silently choosing one value.

## Changing definitions and taxonomy

Changes to what a variable means, how a category is assigned, or how an indicator is calculated carry more weight than individual record corrections, because they alter every value derived from them and can break comparability with earlier analysis.

Such changes require approval from the Principal Investigators. When one is made, the Data Dictionary is updated and its version number incremented, the change and its rationale are recorded, and any affected indicator is recomputed across the dataset so that old and new definitions are not mixed.

The bloc classification scheme is a particularly consequential example. It determines the market share, concentration, and sovereignty figures, and any change to it would alter the headline findings of the platform.

## Maintaining data quality over time

Several mechanisms operate continuously.

**Scheduled updates.** The discovery pipeline runs weekly, so the dataset reflects current developments rather than a fixed snapshot.

**Review queue monitoring.** Records awaiting review are monitored so that the queue does not stall and coverage does not silently fall behind.

**Provenance retention.** Every record keeps its source URL, making verification possible at any point in the future.

**Correction history.** The notes field preserves what was changed and why, so the dataset's history is legible rather than lost.

**Multi-model cross-checking.** As this is introduced, disagreement between independent models will act as an automated signal that a record deserves human attention.

## Sustainability and continuity

The project is designed to outlast any individual contributor. Documentation is maintained in the public repository rather than held informally, so that an incoming team member can understand the system from the repository alone. As standard practice, project infrastructure is held under institutional rather than personal accounts, so that access and continuity do not depend on any one person.

## Licensing

The software is released under the MIT License, and contributions are accepted under the same license. The dataset is released separately under a Creative Commons Attribution 4.0 International (CC BY 4.0) license. Documentation is published alongside the code and dataset so that researchers, journalists, and policymakers can use and build on them, with attribution to the project requested.
