function Methodology() {
  return (
    <div>
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Methodology & Data</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Variable definitions, coding rules, index formulas, and data sources for the Global Digital Infrastructure Political Economy Observatory.
        </p>
      </div>

      {/* Overview */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-4">Project Overview</h2>
          <p className="text-sm leading-relaxed text-[#616161] mb-4">
            This observatory tracks the political economy of global submarine cable infrastructure — who builds it, who owns it, and what that means for national sovereignty and geopolitical risk. Phase 1 covers submarine cables. Future phases will add 5G, cloud, and AI infrastructure datasets using the same analytical framework.
          </p>
          <p className="text-sm leading-relaxed text-[#616161]">
            The dataset covers <strong className="text-[#212121]">694 cables</strong>(as of May 5, 2026, updates weekly) with ready-for-service (RFS) years from 1989 to 2030, drawn from TeleGeography, FCC filings, and primary source verification. Each cable is coded for supplier bloc, owner bloc, geographic reach, and regulatory status.
          </p>
        </div>
      </section>

      {/* Bloc Classification */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Bloc Classification</h2>
          <p className="text-sm text-[#616161] mb-6">Each cable is assigned a <code className="bg-[#F5F5F5] px-1.5 py-0.5 rounded text-xs">supplier_bloc</code> and <code className="bg-[#F5F5F5] px-1.5 py-0.5 rounded text-xs">owner_bloc</code> based on the following rules.</p>

          <table className="w-full text-sm border-collapse mb-6">
            <thead>
              <tr className="border-b-2 border-[#E0E0E0]">
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider">Bloc</th>
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider">Supplier Rule</th>
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider">Owner Rule</th>
              </tr>
            </thead>
            <tbody>
              {[
                {
                  bloc: 'Western',
                  supplier: 'Primary supplier is headquartered in the US, EU, Japan, or Australia (e.g. SubCom, ASN, NEC, Alcatel)',
                  owner: 'Majority ownership by entities based in the US, EU, Japan, or Australia'
                },
                {
                  bloc: 'Chinese',
                  supplier: 'Primary supplier is a Chinese state-affiliated or Chinese-owned manufacturer (e.g. HMN Technologies, HTFG)',
                  owner: 'Majority ownership by Chinese state or private entities (e.g. China Mobile, China Telecom, Huawei Marine)'
                },
                {
                  bloc: 'Other',
                  supplier: 'Primary supplier headquartered outside Western or Chinese blocs (e.g. regional telecoms, Global South manufacturers)',
                  owner: 'Majority ownership by entities in the Global South, regional telecoms, or non-aligned countries'
                },
                {
                  bloc: 'Unknown',
                  supplier: 'Supplier not publicly disclosed or unverifiable from available sources',
                  owner: 'Ownership not publicly disclosed or unverifiable'
                },
              ].map((row, i) => (
                <tr key={row.bloc} className={i < 3 ? 'border-b border-[#F0F0F0]' : ''}>
                  <td className="py-3 px-4 font-semibold text-[#212121]">{row.bloc}</td>
                  <td className="py-3 px-4 text-[#616161]">{row.supplier}</td>
                  <td className="py-3 px-4 text-[#616161]">{row.owner}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="p-4 bg-[#F0F4FA] rounded border border-[#E8EDF5] text-sm text-[#616161]">
            <strong className="text-[#212121]">Note on divergence:</strong> Supplier bloc and owner bloc often differ. A cable may be built by a Western supplier but owned by a Chinese-affiliated consortium, or vice versa. The dashboard distinguishes these perspectives throughout.
          </div>
        </div>
      </section>

      {/* Sovereignty Index */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Cable Sovereignty Index</h2>
          <p className="text-sm text-[#616161] mb-6">
            A composite score (0–1) measuring the degree to which a country's cable infrastructure is diversified, domestically controlled, and resilient. Higher scores indicate greater sovereignty. Calculated separately for supplier and owner perspectives.
          </p>

          {/* Formula */}
          <div className="p-6 bg-[#F5F7F8] rounded-lg border border-[#E0E6EA] mb-6">
            <p className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-3">Formula</p>
            <p className="font-mono text-sm text-[#212121] leading-relaxed">
              Sovereignty Index = 0.40 × Diversification<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ 0.30 × Independence<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ 0.20 × No Single-Bloc Dominance<br/>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ 0.10 × Redundancy
            </p>
          </div>

          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b-2 border-[#E0E0E0]">
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider w-1/5">Component</th>
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider w-1/6">Weight</th>
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider">Definition</th>
              </tr>
            </thead>
            <tbody>
              {[
                { component: 'Diversification', weight: '40%', def: 'Shannon entropy of supplier/owner distribution across blocs. Higher entropy = more diversified.' },
                { component: 'Independence', weight: '30%', def: 'Percentage of cables with domestic suppliers or owners. Bloc-neutral — all countries including China score high when infrastructure is domestically controlled.' },
                { component: 'No Single-Bloc Dominance', weight: '20%', def: '1 minus the share of the dominant bloc. A country where one bloc controls >50% of cables scores lower.' },
                { component: 'Redundancy', weight: '10%', def: 'Normalized cable count relative to country size. More cables = more resilient against single-cable failures.' },
              ].map((row, i) => (
                <tr key={row.component} className={i < 3 ? 'border-b border-[#F0F0F0]' : ''}>
                  <td className="py-3 px-4 font-semibold text-[#212121]">{row.component}</td>
                  <td className="py-3 px-4 text-[#212121] font-mono">{row.weight}</td>
                  <td className="py-3 px-4 text-[#616161]">{row.def}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="mt-6 p-4 bg-[#F0F4FA] rounded border border-[#E8EDF5] text-sm text-[#616161]">
            <strong className="text-[#212121]">Bloc-neutrality revision (March 2026):</strong> The Independence component was revised from measuring "independence from Chinese suppliers/owners" to measuring percentage of domestic control. This change allows all countries — including China — to score high sovereignty when their infrastructure is domestically controlled, and prevents the index from being structurally biased against any single country.
          </div>
        </div>
      </section>

      {/* HHI */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Market Concentration (HHI)</h2>
          <p className="text-sm text-[#616161] mb-6">
            The Herfindahl-Hirschman Index measures market concentration among individual suppliers and owners (not blocs). Calculated as the sum of squared market share percentages.
          </p>
          <div className="p-6 bg-[#F5F7F8] rounded-lg border border-[#E0E6EA] mb-4">
            <p className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-3">Formula</p>
            <p className="font-mono text-sm text-[#212121]">HHI = Σ (market_shareᵢ)²</p>
            <p className="text-xs text-[#9E9E9E] mt-2">where market_shareᵢ is the percentage of total cables supplied/owned by entity i</p>
          </div>
          <div className="grid grid-cols-3 divide-x divide-[#E0E0E0]">
            <div className="px-4 first:pl-0">
              <div className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-1">Low Concentration</div>
              <div className="font-serif text-xl font-bold text-[#212121]">HHI &lt; 1,500</div>
              <div className="text-xs text-[#9E9E9E] mt-1">Competitive market</div>
            </div>
            <div className="px-4">
              <div className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-1">Moderate</div>
              <div className="font-serif text-xl font-bold text-[#212121]">1,500 – 2,500</div>
              <div className="text-xs text-[#9E9E9E] mt-1">Moderately concentrated</div>
            </div>
            <div className="px-4">
              <div className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-1">High Concentration</div>
              <div className="font-serif text-xl font-bold text-[#C62828]">HHI &gt; 2,500</div>
              <div className="text-xs text-[#9E9E9E] mt-1">Highly concentrated</div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Variables */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Key Variable Definitions</h2>
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b-2 border-[#E0E0E0]">
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider w-1/4">Variable</th>
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider w-1/4">Type</th>
                <th className="text-left py-3 px-4 text-xs uppercase font-semibold text-[#616161] tracking-wider">Definition</th>
              </tr>
            </thead>
            <tbody>
              {[
                { var: 'rfs_year', type: 'Integer', def: 'Ready-for-service year — the year the cable became or is expected to become operational. Future years (2026–2030) reflect planned or under-construction cables.' },
                { var: 'supplier_bloc', type: 'Categorical', def: 'Geopolitical bloc of the primary cable manufacturer. Values: Western, Chinese, Other, Unknown.' },
                { var: 'owner_bloc', type: 'Categorical', def: 'Geopolitical bloc of the majority cable owner(s). Values: Western, Chinese, Other, Unknown.' },
                { var: 'chinese_supplier', type: 'Binary (0/1)', def: 'Flag indicating any Chinese-affiliated involvement in cable supply, regardless of primary supplier bloc.' },
                { var: 'chinese_owner', type: 'Binary (0/1)', def: 'Flag indicating any Chinese-affiliated involvement in cable ownership.' },
                { var: 'status', type: 'Categorical', def: 'Operational status. Values: In service, Planned, Under construction, Partially retired, In service (partial).' },
                { var: 'length_km', type: 'Integer', def: 'Total cable length in kilometres including all branches.' },
                { var: 'landing_countries', type: 'String (semicolon-delimited)', def: 'All countries where the cable has confirmed landing stations.' },
                { var: 'total_cables', type: 'Integer (per country)', def: 'Number of submarine cables with a landing point in that country. Used in sovereignty and geographic distribution analysis.' },
              ].map((row, i) => (
                <tr key={row.var} className={i < 8 ? 'border-b border-[#F0F0F0]' : ''}>
                  <td className="py-3 px-4 font-mono text-xs text-[#0D47A1] font-semibold">{row.var}</td>
                  <td className="py-3 px-4 text-[#616161] text-xs">{row.type}</td>
                  <td className="py-3 px-4 text-[#616161]">{row.def}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Data Sources */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Data Sources</h2>
          <div className="space-y-4">
            {[
              {
                name: 'TeleGeography Submarine Cable Map',
                url: 'https://www.submarinecablemap.com',
                desc: 'Primary source for cable names, RFS years, landing stations, and route data. Updated continuously.',
                type: 'Primary'
              },
              {
                name: 'FCC International Bureau Filing System (IBFS)',
                url: 'https://www.fcc.gov/submarine-cable-applications',
                desc: 'Cable landing license applications, approvals, and denials for US-connected cables. Used for policy event tracking and regulatory analysis.',
                type: 'Primary'
              },
              {
                name: 'SubTel Forum',
                url: 'https://subtelforum.com',
                desc: 'Industry news, RFS date verification, and supplier confirmation for recent cable deployments.',
                type: 'Secondary'
              },
              {
                name: 'Company press releases & official cable websites',
                url: null,
                desc: 'Used for ownership verification, RFS date disambiguation, and landing station confirmation. Individual sources cited in dataset notes field.',
                type: 'Primary'
              },
              {
                name: 'MERICS BRI Tracker & Green Finance & Development Center',
                url: 'https://merics.org',
                desc: 'Belt and Road Initiative designation data and Chinese overseas investment tracking used for Chinese supplier/owner classification.',
                type: 'Secondary'
              },
            ].map((source, i) => (
              <div key={i} className={`py-4 ${i < 4 ? 'border-b border-[#F0F0F0]' : ''}`}>
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold text-[#212121] text-sm">{source.name}</span>
                      <span className={`text-xs px-2 py-0.5 rounded font-medium ${source.type === 'Primary' ? 'bg-[#E3F2FD] text-[#0D47A1]' : 'bg-[#F5F5F5] text-[#616161]'}`}>
                        {source.type}
                      </span>
                    </div>
                    <p className="text-sm text-[#616161]">{source.desc}</p>
                  </div>
                  {source.url && (
                    <a href={source.url} target="_blank" rel="noopener noreferrer" className="text-xs text-[#0D47A1] underline whitespace-nowrap mt-1">
                      Visit →
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Limitations */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-4">Known Limitations</h2>
          <div className="space-y-3 text-sm text-[#616161]">
            {[
              'Ownership data is more fragmented than supplier data — consortiums of 10–20 entities are common, and individual owner nationality is sometimes ambiguous. Owner bloc reflects majority or dominant owner where determinable.',
              '20 cables (2.9%) have unknown suppliers. These are typically older cables or cables built by undisclosed manufacturers. They are excluded from HHI and bloc share calculations.',
              'RFS years for planned cables (2026–2030) are based on announced schedules and subject to change. Delays of 1–3 years are common in the industry.',
              'The sovereignty index is country-level and does not capture sub-national variation or the specific strategic significance of individual cable routes.',
              'Chinese supplier classification uses a broad definition that includes state-affiliated entities. The line between state and private in Chinese telecoms is contested and the dataset reflects best-available public information.',
            ].map((item, i) => (
              <div key={i} className="flex gap-3">
                <span className="text-[#9E9E9E] mt-0.5 shrink-0">—</span>
                <p className="m-0">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Citation */}
      <section className="mb-10">
        <div className="bg-[#F0F4FA] rounded-lg border border-[#E8EDF5] p-6">
          <h2 className="font-serif text-base font-semibold text-[#212121] mb-2">Citation</h2>
          <p className="text-sm text-[#616161] font-mono leading-relaxed">
            Global Digital Infrastructure Political Economy Observatory, Phase 1: Submarine Cables.<br/>
          </p>
        </div>
      </section>
    </div>
  )
}

export default Methodology