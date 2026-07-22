import { Link } from 'react-router-dom'

// Google Form for beta sign-up
const BETA_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfKs-Woma7qoMD5hFfk6ZhdWdFokj8UIBOWfYFQwtt0KnRuLw/viewform?usp=dialog'

// Body text stays readable; the page itself spans the full app container.
const PROSE = 'max-w-4xl'
const CARD = 'bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6'

const whyItMatters = [
  {
    title: 'Ownership',
    body: 'Ownership, construction, and supply concentrate among a handful of firms and states. Making that structure visible is the first step to understanding it.',
  },
  {
    title: 'Geography',
    body: 'Landing points and cable routes shape which countries depend on whom, turning cables into questions of sovereignty and resilience.',
  },
  {
    title: 'Policy',
    body: "A fast-moving body of regulation is reshaping who can build and operate cables. The platform's monitoring pipeline tracks these changes as they happen.",
  },
  {
    title: 'AI and national security',
    body: 'The infrastructure AI depends on, the cables and data centers it runs on, is increasingly a matter of national security and economic competitiveness, not just connectivity. Understanding who owns and supplies it is a first step toward assessing that exposure.',
  },
]

const whatWeTrack = [
  {
    title: 'Submarine cables',
    body: 'Nearly 700 cables with ownership, suppliers, landing countries and stations, length, operational status, and supplier and owner bloc classifications.',
  },
  {
    title: 'Policy and regulation',
    body: 'A timeline of regulatory events from 1884 to the present, spanning the US, EU, and other jurisdictions, each linked to how it affects cable infrastructure, and kept current by an AI-driven monitoring pipeline that flags new developments as they happen.',
  },
  {
    title: 'Sovereignty and dependency',
    body: 'Country-level views of dependence and control, derived from ownership and landing-point data.',
  },
  {
    title: 'Coming next: AI data centers and 5G',
    body: 'The same framework will extend to the data centers that power AI and to 5G networks in upcoming phases, tracking ownership, suppliers, and the policy environment around them the same way it does for cables today.',
  },
]

const team = [
  {
    name: 'Prof. Kellee Tsai',
    role: 'Co-PI · Dean, College of Social Sciences and Humanities; Distinguished Professor of Political Science, Northeastern University',
  },
  {
    name: 'Prof. Xiaoxiao Shen',
    role: 'Co-PI · Assistant Research Professor of Political Science, Northeastern University',
  },
  { name: 'Anthony Chan', role: 'Research Assistant (current)' },
  { name: 'Sowrathi Somasundaram', role: 'Research Assistant (former)' },
]

const faqs = [
  {
    q: 'What is the Digital Infrastructure Observatory?',
    a: "It is a public research platform that tracks who owns, builds, and supplies the physical infrastructure that AI and the internet run on, starting with the world's submarine cable network, paired with an interactive dashboard and an openly available dataset.",
  },
  {
    q: 'Where does the data come from?',
    a: 'From public sources such as industry cable maps, regulatory filings, and company announcements, gathered through an AI-assisted pipeline and checked by a researcher before publishing.',
  },
  {
    q: 'How current is the data?',
    a: 'The dataset is updated on a recurring basis. New cables and policy developments are added as they are found and approved, so the record stays live rather than frozen at a point in time.',
  },
  {
    q: 'Does this only cover submarine cables?',
    a: 'Submarine cables are Phase 1. The same framework is being extended to the data centers that power AI and to 5G networks in later phases.',
  },
  {
    q: 'How is data quality ensured?',
    a: 'Every record passes automated checks and human review before it goes live. A multi-model cross-check, in which two independent models extract the same record, flags any disagreements for a person to resolve.',
  },
  {
    q: 'Is the project open source, and can I contribute?',
    a: "Yes. The project is open source under the MIT License. You don't need to be a developer to contribute. Anyone can explore the dashboard, flag missing or outdated information, suggest new indicators to track, request beta access, or contribute code on GitHub.",
  },
]

function About() {
  return (
    <div className="w-full">
      {/* About */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-4">
          About the Observatory
        </h2>
        <div className={PROSE}>
          <p className="text-[#424242] text-lg leading-relaxed mb-4">
            The Digital Infrastructure Observatory is a public research platform for tracking who
            owns, builds, and supplies the physical infrastructure that AI and the global internet
            run on. It pairs a continuously maintained dataset, kept current by an AI-driven
            monitoring pipeline, with an interactive dashboard, so that researchers, policymakers,
            journalists, and the public can see the ownership and supply structure behind critical
            digital infrastructure, not just where it is located or who operates it, which is where
            most existing sources stop.
          </p>
          <p className="text-[#616161] leading-relaxed">
            Phase 1 focuses on submarine communications cables, the undersea network that carries the
            overwhelming majority of international internet traffic, together with the policies that
            shape them. The same framework is designed to extend to the data centers that power AI
            and to 5G networks in later phases.
          </p>
        </div>
      </section>

      {/* Why it matters */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-6">Why it matters</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {whyItMatters.map((c) => (
            <div key={c.title} className={CARD}>
              <div className="text-[#0D47A1] font-semibold text-sm mb-2">{c.title}</div>
              <p className="text-[#616161] text-sm leading-relaxed">{c.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* What we track */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-6">What we track</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {whatWeTrack.map((c) => (
            <div key={c.title} className={CARD}>
              <h3 className="font-serif text-lg font-semibold text-[#212121] mb-1">{c.title}</h3>
              <p className="text-[#616161] leading-relaxed">{c.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-4">How it works</h2>
        <p className={`${PROSE} text-[#616161] leading-relaxed mb-6`}>
          New records move through an AI-assisted pipeline with a researcher review step, so the
          dataset stays current without sacrificing accuracy. Nothing reaches the live dashboard
          until a researcher has approved it.
        </p>
        <div className={CARD}>
          <img
            src="/architecture.svg"
            alt="Data pipeline: web sources, to AI extraction, to validation, to database, to dashboard"
            className="w-full"
          />
        </div>
      </section>

      {/* A look at the dashboard */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-6">
          A look at the dashboard
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <img
            src="/screenshots/map.png"
            alt="World map of global submarine cable landing points"
            className="w-full rounded-lg border border-[#E0E0E0] shadow-sm"
          />
          <img
            src="/screenshots/supplier-bloc.png"
            alt="Market share by supplier bloc"
            className="w-full rounded-lg border border-[#E0E0E0] shadow-sm"
          />
          <img
            src="/screenshots/sovereignty.png"
            alt="Sovereignty versus infrastructure density"
            className="w-full rounded-lg border border-[#E0E0E0] shadow-sm"
          />
          <img
            src="/screenshots/timeline.png"
            alt="Regulatory timeline of submarine cable policy events"
            className="w-full rounded-lg border border-[#E0E0E0] shadow-sm"
          />
        </div>
        <Link
          to="/overview"
          className="inline-block mt-6 px-6 py-3 bg-[#0D47A1] text-white text-sm font-semibold rounded-md hover:bg-[#0B3D8C] transition-colors"
        >
          Explore the dashboard →
        </Link>
      </section>

      {/* Team */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-4">Team</h2>
        <p className={`${PROSE} text-[#616161] mb-5`}>
          Developed at Northeastern University as part of ongoing research on technology, security,
          and society.
        </p>
        <ul className="space-y-2">
          {team.map((m) => (
            <li key={m.name} className="text-[#616161] text-sm leading-relaxed">
              <span className="font-semibold text-[#212121]">{m.name}</span> · {m.role}
            </li>
          ))}
        </ul>
      </section>

      {/* FAQ */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-6">
          Frequently asked questions
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 items-start">
          {faqs.map((f) => (
            <details key={f.q} className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-5 group">
              <summary className="font-serif text-base font-semibold text-[#212121] cursor-pointer list-none flex justify-between items-center">
                {f.q}
                <span className="text-[#0D47A1] text-xl ml-4 group-open:rotate-45 transition-transform">
                  +
                </span>
              </summary>
              <p className="text-[#616161] text-sm leading-relaxed mt-3">{f.a}</p>
            </details>
          ))}
        </div>
      </section>

      {/* Contact / beta access */}
      <section className="mb-8 bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-3">Get involved</h2>
        <p className={`${PROSE} text-[#616161] leading-relaxed mb-6`}>
          The dashboard is free to explore for anyone. Request beta access below if you want to
          download the underlying dataset (CSV) or register as a contributor, to submit data
          corrections, flag missing information, or suggest new indicators to track.
        </p>
        <a
          href={BETA_FORM_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block px-6 py-3 bg-[#0D47A1] text-white text-sm font-semibold rounded-md hover:bg-[#0B3D8C] transition-colors"
        >
          Request beta access
        </a>
      </section>
    </div>
  )
}

export default About