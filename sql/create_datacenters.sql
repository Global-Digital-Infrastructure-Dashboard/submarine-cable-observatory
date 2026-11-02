-- US data-center ownership enrichment (enrich_datacenters.py), loaded by push_datacenters.py.
-- Run once in the Supabase SQL editor.
--
-- PRIVATE: row level security is on and there is deliberately no policy, so the public anon
-- key the dashboard ships can't read this table; only the service role can. The rows carry
-- FracTracker Alliance fields, which aren't cleared for public release. Add a read policy only
-- once a citation-compliant public version exists.
--
-- Text fields use the dataset's "not disclosed" convention. Numeric fields with no value are
-- null. capacity_estimated_mw stays text because sources give ranges ("50-100").

create table if not exists public.datacenters (
    id                      bigint generated always as identity primary key,
    created_at              timestamptz not null default now(),
    facility_id             text not null unique,   -- FT-... (FracTracker) or TDC-... (trackdatacenters.com)
    facility_name           text not null,
    operator                text,
    owner_parent            text,
    owner_parent_inferred   boolean not null,       -- from public corporate knowledge, not facility evidence
    country                 text,
    city                    text,
    lat                     double precision,
    lon                     double precision,
    capacity_mw_coded       double precision,
    capacity_basis          text,
    capacity_estimated_mw   text,
    capacity_raw            text,                   -- FracTracker's original MW field
    operator_nationality    text,
    owner_origin            text,
    owner_origin_inferred   boolean not null,
    legal_domicile          text,
    ownership_structure     text,
    ownership_structure_raw text,
    operator_type           text,
    service_model           text,
    tier_rating             text,
    siting_determinants     text,
    facilities_within_50km  integer,
    cable_landing_km        double precision,       -- to the nearest in-service submarine-cable landing
    nearest_landing         text,
    operator_siting_logic   text,
    bis_listed              text,                   -- "not disclosed" = no source reports a listing
    ofac_listed             text,
    fdi_screening           text,
    data_localization       text,
    status                  text,                   -- FracTracker's status
    source_urls             text,
    attribution_tier        text,                   -- 1 operator, 2 filing, 3 analyst, or "not disclosed"
    notes                   text,
    foreign_linked_entities text                    -- "not extracted" on 57 rows coded before this field existed
);

alter table public.datacenters enable row level security;

comment on table public.datacenters is
    'US data-center ownership enrichment. Private (RLS, no policies): carries FracTracker Alliance fields; '
    'cite "Data provided by FracTracker Alliance (2026). Accessed via https://www.fractracker.org/data-centers/".';
