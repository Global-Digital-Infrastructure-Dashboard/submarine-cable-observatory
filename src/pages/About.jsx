import { Link } from 'react-router-dom'

// TODO: paste your Google Form link here once the beta sign-up form is live.
const BETA_FORM_URL = 'REPLACE_WITH_GOOGLE_FORM_URL'

function About() {
  return (
    <div className="max-w-4xl mx-auto">
      {/* About */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-4">
          About the Observatory
        </h2>
        <p className="text-[#424242] text-lg leading-relaxed mb-4">
          The Digital Infrastructure Observatory is a public research platform for studying the
          physical and political structure of the global internet. It pairs a continuously
          maintained dataset with an interactive dashboard, so that researchers, policymakers,
          journalists, and the public can see who owns, builds, and governs critical digital
          infrastructure.
        </p>
        <p className="text-[#616161] leading-relaxed">
          Phase 1 focuses on submarine communications cables, the undersea network that carries the
          overwhelming majority of international internet traffic, together with the policies that
          shape them. The same framework is designed to extend to 5G networks and data centers in
          later phases.
        </p>
      </section>

      {/* Why it matters */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-6">Why it matters</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
            <div className="text-[#0D47A1] font-semibold text-sm mb-2">Ownership</div>
            <p className="text-[#616161] text-sm leading-relaxed">
              Ownership and supply concentrate among a handful of firms and states. Making that
              structure visible is the first step to understanding it.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
            <div className="text-[#0D47A1] font-semibold text-sm mb-2">Geography</div>
            <p className="text-[#616161] text-sm leading-relaxed">
              Landing points and cable routes shape which countries depend on whom, turning cables
              into questions of sovereignty and resilience.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
            <div className="text-[#0D47A1] font-semibold text-sm mb-2">Policy</div>
            <p className="text-[#616161] text-sm leading-relaxed">
              A fast-moving body of regulation is reshaping who can build and operate cables. The
              platform tracks these changes as they happen.
            </p>
          </div>
        </div>
      </section>

      {/* Data coverage */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-6">What we track</h2>
        <div className="space-y-4">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
            <h3 className="font-serif text-lg font-semibold text-[#212121] mb-1">Submarine cables</h3>
            <p className="text-[#616161] leading-relaxed">
              Nearly 700 cables with ownership, suppliers, landing countries and stations, length,
              operational status, and supplier and owner bloc classifications.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
            <h3 className="font-serif text-lg font-semibold text-[#212121] mb-1">
              Policy and regulation
            </h3>
            <p className="text-[#616161] leading-relaxed">
              A timeline of regulatory events from 1884 to the present, spanning the US, EU, and
              other jurisdictions, each linked to how it affects cable infrastructure.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
            <h3 className="font-serif text-lg font-semibold text-[#212121] mb-1">
              Sovereignty and dependency
            </h3>
            <p className="text-[#616161] leading-relaxed">
              Country-level views of dependence and control, derived from ownership and
              landing-point data.
            </p>
          </div>
        </div>
        <p className="text-[#616161] text-sm mt-4">
          The dataset is kept current through an AI-assisted pipeline with a human review step, so
          coverage stays fresh without sacrificing accuracy.
        </p>
        <Link
          to="/"
          className="inline-block mt-6 px-6 py-3 bg-[#0D47A1] text-white text-sm font-semibold rounded-md hover:bg-[#0B3D8C] transition-colors"
        >
          Explore the dashboard →
        </Link>
      </section>

      {/* Team */}
      <section className="mb-14">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-6">Team</h2>
        <p className="text-[#616161] mb-6">
          Developed at Northeastern University as part of ongoing research on technology, security,
          and society.
        </p>
        <div className="space-y-5">
          <div className="border-l-4 border-[#0D47A1] pl-4">
            <div className="font-serif text-lg font-semibold text-[#212121]">Prof. Xiaoxiao Shen</div>
            <div className="text-[#616161] text-sm">
              Co-Principal Investigator · Assistant Research Professor of Political Science,
              Northeastern University
            </div>
          </div>
          <div className="border-l-4 border-[#0D47A1] pl-4">
            <div className="font-serif text-lg font-semibold text-[#212121]">Prof. Kellee Tsai</div>
            <div className="text-[#616161] text-sm">
              Co-Principal Investigator · Dean of the College of Social Sciences and Humanities and
              Distinguished Professor of Political Science, Northeastern University
            </div>
          </div>
          <div className="border-l-4 border-[#E0E0E0] pl-4">
            <div className="font-serif text-lg font-semibold text-[#212121]">Anthony Chan</div>
            <div className="text-[#616161] text-sm">Research Assistant (current)</div>
          </div>
          <div className="border-l-4 border-[#E0E0E0] pl-4">
            <div className="font-serif text-lg font-semibold text-[#212121]">
              Sowrathi Somasundaram
            </div>
            <div className="text-[#616161] text-sm">Research Assistant (former)</div>
          </div>
        </div>
      </section>

      {/* Contact / beta access */}
      <section className="mb-8 bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
        <h2 className="font-serif text-3xl font-semibold text-[#212121] mb-3">Get involved</h2>
        <p className="text-[#616161] leading-relaxed mb-6 max-w-2xl">
          The platform is open and actively developed. If you would like to use it in your work,
          contribute data corrections, or follow along as it grows, request access below.
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
