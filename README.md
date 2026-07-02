<img width="845" height="484" alt="Screenshot 2026-07-02 at 1 30 15 PM" src="https://github.com/user-attachments/assets/2eea30d7-b448-4d61-9ded-c580ef43d164" />

---

**An open source research platform mapping the political economy of global digital infrastructure — starting with the world's submarine cable network.**

🔗 **Live dashboard:** https://research-platform-sand.vercel.app/

---

## Overview

The Digital Infrastructure Observatory is a public research platform that tracks the physical and regulatory backbone of the global internet. It pairs a continuously updated dataset with an interactive dashboard so that researchers, policymakers, journalists, and the public can explore who owns, builds, and governs critical digital infrastructure.

Phase 1 focuses on **submarine communications cables** — the network of undersea cables that carries the overwhelming majority of international internet traffic — together with the **policies and regulations** that shape it. The same analytical framework is designed to extend to 5G networks and data centers in later phases.

The project is developed at Northeastern University as part of ongoing research on technology, security, and society. It is built to be transparent and reproducible: the data pipeline, the review process, and the dashboard are all open.

## What it tracks

- **Submarine cables** — nearly 700 cables with ownership, suppliers, landing countries and stations, length, operational status, and supplier/owner "bloc" classifications.
- **Policy & regulation** — a timeline of regulatory events from 1884 to the present, spanning the US, EU, and other jurisdictions, each linked to how it affects cable infrastructure.
- **Geopolitical structure** — sovereignty and dependency measures derived from ownership and landing-point data.

## How it works

The dataset stays current through an AI-assisted pipeline with a human review gate. In outline:

**Web sources → AI extraction → enrichment & validation → deduplication → human review → database → dashboard**

1. **Discovery** — Perplexity searches public sources for recent cable announcements and policy developments.
2. **Extraction** — Claude reads the raw source material and pulls out structured records (cable name, owners, suppliers, landing points, dates, and so on).
3. **Enrichment & validation** — a second Claude step standardizes fields, classifies ownership and supplier blocs, and checks records for internal consistency.
4. **Deduplication** — each new record is checked against existing data so the same cable or event is never added twice.
5. **Human review** — proposed records land in a staging sheet where a researcher approves, edits, or rejects them before anything reaches the live dataset.
6. **Database** — approved records are written to the project database.
7. **Dashboard** — the public dashboard reads directly from the database, so approved updates appear without a redeploy.

This keeps the dataset fresh while ensuring a human signs off on every record that goes live. A multi-model cross-check (having two independent models extract the same record and flagging disagreements for review) is being added as a further data-quality safeguard.

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite, Tailwind CSS (deployed on Vercel) |
| Database | Supabase (PostgreSQL) |
| Automation | Make.com |
| AI / extraction | Claude (Anthropic), Perplexity |
| Human review | Google Sheets |

## Getting started

The dashboard is a standard Vite + React application.

```bash
# clone the repo
git clone [repo URL]
cd submarine-cable-observatory

# install dependencies
npm install

# start the dev server
npm run dev
```

Other scripts: `npm run build` (production build), `npm run preview` (preview a build), and `npm run lint`.

**Configuration.** The app connects to a Supabase project using a project URL and a public anon key, currently set in `src/lib/supabase.js`. For public/open-source use, move these into a `.env` file (Vite reads `VITE_`-prefixed variables) and commit a `.env.example` so contributors know what to set. Only the public anon key belongs in the frontend, and only when the database has row-level security enabled — never commit the Supabase service role key or any other secret.

## Roadmap

A short summary is below; see [`roadmap.md`](roadmap.md) for the full version.

- **Now** — keep the submarine cable and policy datasets live and current; add multi-model extraction cross-checks for data-quality confidence.
- **Next** — public website, contributor documentation, and data-coverage reporting.
- **Later (Phase 2+)** — extend the framework to 5G and data center infrastructure.

## Contributing

Contributions are welcome, including data corrections. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to get involved, report an issue, or suggest a change.

## Team

Developed at Northeastern University.

- **[Prof. Xiaoxiao Shen]** — Principal Investigator
- **[Prof. Tsai]** 
- **[Anthony Chan]** — Research Assistant

## Contact / beta access

Interested in using the platform or joining as a beta user? _[Add a sign-up form link or a project contact address.]_

## License

This project is intended as open-source infrastructure.
