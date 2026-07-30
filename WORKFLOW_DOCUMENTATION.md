# Workflow Documentation

**Version:** v1
**Scope:** How information moves through the Global Digital Infrastructure Political Economy Observatory, from discovering a new infrastructure asset to displaying it on the public dashboard.

## Overview

Every record on the dashboard passes through seven stages. The pipeline is automated end to end except for one deliberate stop: a researcher must approve each record before it reaches the live database. Nothing is published on the strength of an AI extraction alone.

**Web sources → AI extraction → enrichment and classification → deduplication → researcher review → database update → dashboard**

The pipeline runs on a weekly schedule and is orchestrated in Make.com across four scenarios: two that discover and stage new records (one for cables, one for policy), and two that move approved records into the database.

## Stage 1: Source discovery

A scheduled query runs against the Perplexity API to search public sources for recent submarine cable announcements and regulatory developments. Typical sources include industry cable maps and trade press, regulatory filings and government notices, company and consortium announcements, and international body publications.

The query is scoped with a recency filter so that results reflect genuinely new developments rather than re-surfacing established records. The policy query is additionally tuned to counteract a strong bias toward United States and FCC sources, and explicitly names regulators outside the United States so that additional jurisdictions are covered.

**Output:** raw text and source URLs describing candidate records.

## Stage 2: AI extraction

The raw source material is passed to Claude with an extraction prompt that returns structured JSON. For cables this includes the cable name, owners, suppliers, landing countries and stations, ready-for-service year, length, and operational status. For policy events it includes the policy name, event date, jurisdiction, the substance of the change, its effect on cable infrastructure, and the source URL.

Extraction is deliberately separated from interpretation. This step captures what the source says; the following step normalizes and classifies it.

**Output:** structured records in a consistent schema.

## Stage 3: Enrichment and classification

A second Claude step normalizes and enriches the extracted records. It standardizes field formats so that values are consistent with existing records, in particular jurisdiction labels, which must match the short forms already used in the dataset. It assigns geopolitical bloc classifications for suppliers and owners based on their country of origin, following the rules documented in the Data Dictionary. It also performs internal consistency checks, for example confirming that a supplier country is present when a supplier is named.

**Output:** normalized, classified records ready for comparison against existing data.

## Stage 4: Deduplication

Deduplication happens in two passes. First, an AI step merges duplicate records that appear within the same batch, since a single development is often reported by several outlets. Second, at the point of database insertion, the pipeline issues a query against the live database keyed on the record's name. If a matching record already exists, a filter stops the record from being inserted and it is not written again.

This second check is what prevents the dataset from accumulating repeated entries over successive weekly runs.

**Output:** a set of records believed to be genuinely new.

## Stage 5: Researcher review

New records are written to a staging spreadsheet in Google Sheets, which functions as the review queue. Each row carries the extracted fields plus quality metadata, including a confidence rating, a needs-review flag, and an indicator of whether the record is likely to already exist.

A researcher reviews each row and marks an approval column. Only rows explicitly marked as approved advance. Rows may also be edited before approval, or left unapproved indefinitely if the underlying source is weak.

This is the project's primary quality-control gate. It is intentionally manual, and it is the reason no AI-generated record reaches the public dashboard without human judgment applied to it.

**Output:** an approved subset of records.

## Stage 6: Database update

A second Make.com scenario reads the review queue, filters to approved rows, runs the deduplication check described in Stage 4, and inserts the record into the project database (Supabase, PostgreSQL). On a successful insert, the scenario writes a status back to the source row in the spreadsheet, which removes it from the approved set so that it is not imported twice on the next run.

**Output:** the record is live in the database.

## Stage 7: Dashboard visualization

The public dashboard reads directly from the database at page load. There is no separate publication or export step, and no redeployment is required. Once a record is in the database, it appears on the dashboard the next time a visitor loads the page.

Derived indicators, including bloc market share, concentration measures, and the sovereignty index, are computed from the underlying records rather than stored, so they update automatically as the dataset grows.

**Output:** the record is visible to the public.

## Quality control summary

Quality is enforced at four points rather than one.

| Stage | Control |
|-------|---------|
| Extraction | Structured schema constrains what can be captured |
| Enrichment | Normalization and internal consistency checks |
| Deduplication | In-batch merge, plus a live check against the database |
| Researcher review | Explicit human approval required before publication |

Every record also retains its source URL, so any published value can be traced back to the material it came from. A notes field records subsequent corrections, including what was changed and why.

## Planned addition: multi-model cross-check

A further safeguard is in development. Two independent models, from different providers, will extract the same record from the same source. Where they agree, confidence in the extracted values increases. Where they diverge, the record is flagged for researcher attention rather than passing through on a single model's output.

Using models from different providers is deliberate: two models from the same family would tend to share the same blind spots, so their agreement would carry less information.
