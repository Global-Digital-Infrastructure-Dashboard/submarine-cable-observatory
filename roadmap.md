# Roadmap

This roadmap gives a high-level view of where the Global Digital Infrastructure Political Economy Observatory is today and where it is heading. It is a living document and will evolve as the project grows.

## Current phase: Submarine cables

The platform currently tracks the global submarine cable network and the policies that govern it.

**Live today**

- Interactive dashboard covering cable ownership, suppliers, landing points, and supplier/owner blocs.
- A policy and regulation timeline spanning 1884 to the present.
- Sovereignty and dependency views derived from ownership and landing-point data.
- An AI-assisted data pipeline with a human review gate that keeps both the cable and policy datasets current, running on a weekly schedule for both.
- Row-level security enabled on the database, restricting the public dashboard to read-only access.

**In progress**

- **Multi-model extraction cross-checks:** two independent models extract each record, and disagreements are flagged for human review as an added data-quality safeguard.
- **Automated review-queue notifications** so newly discovered records are reviewed promptly rather than sitting in the queue.

## Near term

- A public **website** introducing the project, its goals, data coverage, and a beta-user sign-up.
- **Contributor documentation** and a clear process for community data corrections.
- **Data-coverage and data-quality reporting** so users can see how complete and current the dataset is.
- **Completing the GitHub repository transfer** to a public, institutional account, the remaining step before the codebase itself is opened up.

## Later: additional infrastructure domains (Phase 2+)

The same framework (discovery, AI extraction, validation, human review, and a public dashboard) is designed to extend to other layers of digital infrastructure:

- 5G networks
- Data centers

## How to get involved

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Data corrections, feature suggestions, and issue reports are all welcome.
