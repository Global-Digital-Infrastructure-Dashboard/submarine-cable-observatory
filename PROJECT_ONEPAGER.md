# Digital Infrastructure Observatory

**A public research platform mapping who owns, builds, and supplies the physical infrastructure that AI and the global internet run on.**

Northeastern University · [research-platform-sand.vercel.app](https://research-platform-sand.vercel.app/)

## The problem

Almost all international internet traffic travels through submarine cables. Those cables, and the data centers that AI depends on, are owned and built by a small number of firms and states. That concentration has become a question of national security and economic competitiveness, not simply connectivity.

Existing public sources show where cables are and who operates them. Very few show the ownership and supply structure behind them, and fewer still track how quickly the regulatory environment around them is changing. That gap is what this project addresses.

## What we built

An openly available dataset and an interactive dashboard covering:

- **Nearly 700 submarine cables**, with owners, suppliers, landing countries and stations, length, operational status, and geopolitical bloc classification for both supply and ownership.
- **A regulatory timeline from 1884 to the present**, spanning the United States, the European Union, and other jurisdictions, with each event linked to its effect on cable infrastructure.
- **Derived measures of sovereignty and dependency**, including market concentration and a composite sovereignty index calculated for each country.

## How it stays current

The dataset is maintained by an AI-assisted pipeline with a human review step:

**Web sources → AI extraction → validation → researcher review → database → dashboard**

Automated discovery and extraction run weekly. Every record is reviewed and approved by a researcher before it is published, and each one retains the source it came from. A multi-model cross-check, in which two independent models extract the same record and disagreements are flagged for human attention, is being added as a further safeguard.

## Who it is for

Researchers studying infrastructure, political economy, and security. Policymakers assessing dependency and resilience. Journalists reporting on ownership and control of digital infrastructure. Developers and analysts who want a structured, current dataset to build on.

## Open by design

The project is open source under the MIT License. The code, the variable definitions, the workflow, and the governance process are all publicly documented, so that the platform can be understood, verified, and extended by people outside the research group. Contributions are welcome, including data corrections from people with direct knowledge of particular systems.

## What is next

The same framework is being extended to the data centers that power AI and to 5G networks. Near-term work focuses on deeper interactivity in the dashboard, broader non-Western source coverage, and expanded contributor tooling.

## Get involved

Explore the dashboard, request beta access for the underlying dataset, or contribute on GitHub. Contact the project team through the website.

**Team**
Prof. Kellee Tsai, Co-PI · Dean, College of Social Sciences and Humanities; Distinguished Professor of Political Science, Northeastern University
Prof. Xiaoxiao Shen, Co-PI · Assistant Research Professor of Political Science, Northeastern University
Anthony Chan, Research Assistant
Sowrathi Somasundaram, Research Assistant (former)
