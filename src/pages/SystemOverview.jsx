import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

function SystemOverview() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadCables() {
      console.log('Fetching from Supabase...')
      const { data: cables, error } = await supabase
        .from('submarinecables')
        .select('*')
      if (error) {
        console.error('Supabase error:', error)
        setLoading(false)
        return
      }
      console.log('Loaded cables:', cables?.length || 0)
      console.log('First cable:', cables?.[0])
      setData(cables)
      setLoading(false)
    }
    loadCables()
  }, [])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <div className="w-10 h-10 border-4 border-gray-200 border-t-[#0D47A1] rounded-full animate-spin mb-4"></div>
        <p className="text-[#616161]">Loading submarine cable data...</p>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
        <p className="text-red-600">No data found. Check console for details.</p>
        <p className="text-sm text-gray-600 mt-2">Data length: {data?.length || 0}</p>
      </div>
    )
  }

  const blocCounts = data.reduce((acc, cable) => {
    const bloc = cable.supplier_bloc || 'Unknown'
    acc[bloc] = (acc[bloc] || 0) + 1
    return acc
  }, {})

  const ownerBlocCounts = data.reduce((acc, cable) => {
    const bloc = cable.owner_bloc || 'Unknown'
    acc[bloc] = (acc[bloc] || 0) + 1
    return acc
  }, {})

  const activeCables = data.filter(c => c.status === 'In service').length
  const chineseCables = data.filter(c => c.chinese_supplier === 1 || c.chinese_supplier === '1').length
  const westernCount = blocCounts['Western'] || 0

  // HHI calculated live: sum of squared market share percentages per supplier/owner
  const supplierNameCounts = data.reduce((acc, cable) => {
    const s = cable.suppliers || 'Unknown'
    acc[s] = (acc[s] || 0) + 1
    return acc
  }, {})
  const supplierHHI = Math.round(
    Object.values(supplierNameCounts).reduce((sum, count) => {
      const share = (count / data.length) * 100
      return sum + share * share
    }, 0)
  )

  const ownerNameCounts = data.reduce((acc, cable) => {
    const o = cable.owners || 'Unknown'
    acc[o] = (acc[o] || 0) + 1
    return acc
  }, {})
  const ownerHHI = Math.round(
    Object.values(ownerNameCounts).reduce((sum, count) => {
      const share = (count / data.length) * 100
      return sum + share * share
    }, 0)
  )

  const renderBar = (bloc, count, total) => {
    const pct = parseFloat(((count / total) * 100).toFixed(1))
    const label = `${pct.toFixed(1)}%`
    const isNarrow = pct < 12
    return (
      <div key={bloc} className="flex items-center gap-4">
        <div className="min-w-[100px] text-sm font-medium text-[#212121]">{bloc}</div>
        <div className="flex-1 bg-[#E0E0E0] rounded h-9 relative">
          <div
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-[#0D47A1] to-[#0097A7] rounded transition-all duration-300"
            style={{ width: `${pct}%` }}
          />
          {isNarrow ? (
            <span
              className="absolute top-0 h-full flex items-center text-xs font-semibold text-[#212121] whitespace-nowrap"
              style={{ left: `calc(${pct}% + 8px)` }}
            >
              {label}
            </span>
          ) : (
            <span
              className="absolute top-0 h-full flex items-center text-xs font-semibold text-white"
              style={{ left: `calc(${pct}% - 8px)`, transform: 'translateX(-100%)' }}
            >
              {label}
            </span>
          )}
        </div>
        <div className="min-w-[90px] text-right text-sm text-[#616161] font-medium">{count} cables</div>
      </div>
    )
  }

  const statCards = [
    { value: data.length,        label: 'Total Cables',      sub: '↑ Infrastructure count',                                         accent: '#0D47A1' },
    { value: supplierHHI.toLocaleString(), label: 'Supplier HHI', sub: 'High concentration',                                        accent: '#0D47A1' },
    { value: `${((chineseCables / data.length) * 100).toFixed(1)}%`, label: 'Chinese Suppliers', sub: `${chineseCables} cables`,     accent: '#0D47A1' },
    { value: activeCables,       label: 'Active Cables',     sub: `${((activeCables / data.length) * 100).toFixed(1)}% operational`, accent: '#0D47A1' },
  ]

  return (
    <div>
      {/* Page Header */}
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">System Overview</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Global structural summary of submarine cable infrastructure.
          Showing {data.length} cables across {Object.keys(blocCounts).length} geopolitical blocs.
        </p>
      </div>

      {/* Key Metrics — unified light cards */}
      <section className="mb-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {statCards.map((card, i) => (
            <div
              key={i}
              className="rounded-lg p-6 flex flex-col gap-1 border border-[#E8EDF5]"
              style={{ backgroundColor: '#F0F4FA' }}
            >
              <div className="font-serif text-4xl font-bold leading-tight" style={{ color: '#0A2F6B' }}>
                {card.value}
              </div>
              <div className="text-xs font-bold uppercase tracking-widest mt-2 text-[#616161]">
                {card.label}
              </div>
              <div className="text-xs mt-0.5 text-[#9E9E9E]">
                {card.sub}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Key Findings — white cards, single dark left border */}
      <section className="mb-10">
        <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Key Findings</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
            <h3 className="text-base font-semibold mb-3 text-[#212121]">Market Concentration</h3>
            <p className="text-sm leading-relaxed text-[#616161] m-0">
              Both supplier (HHI: {supplierHHI.toLocaleString()}) and owner (HHI: {ownerHHI.toLocaleString()}) markets are highly concentrated (&gt;2500), indicating limited competition.
            </p>
          </div>
          <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
            <h3 className="text-base font-semibold mb-3 text-[#212121]">Chinese Participation</h3>
            <p className="text-sm leading-relaxed text-[#616161] m-0">
              Chinese suppliers involved in {chineseCables} cables ({((chineseCables / data.length) * 100).toFixed(1)}%), representing a 20x increase from pre-2013 levels.
            </p>
          </div>
          <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
            <h3 className="text-base font-semibold mb-3 text-[#212121]">Western Dominance</h3>
            <p className="text-sm leading-relaxed text-[#616161] m-0">
              Western suppliers build {((westernCount / data.length) * 100).toFixed(1)}% of cables ({westernCount} total), led by SubCom, ASN, and NEC.
            </p>
          </div>
          <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
            <h3 className="text-base font-semibold mb-3 text-[#212121]">Data Coverage</h3>
            <p className="text-sm leading-relaxed text-[#616161] m-0">
              {blocCounts['Unknown'] || 0} cables ({(((blocCounts['Unknown'] || 0) / data.length) * 100).toFixed(1)}%) have unknown suppliers. Owner data has 97% coverage.
            </p>
          </div>
        </div>
      </section>

      {/* Supplier Market Share */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Supplier Market Share by Bloc</h2>
          <p className="text-sm text-[#616161] mb-6">
            Distribution of cable manufacturers across geopolitical blocs.
            Supplier data provides clearer bloc-level patterns than ownership (which is highly fragmented).
          </p>
          <div className="space-y-4 mb-8">
            {Object.entries(blocCounts)
              .sort(([,a], [,b]) => b - a)
              .map(([bloc, count]) => renderBar(bloc, count, data.length))}
          </div>
          <div className="border-t border-[#E0E0E0] pt-6">
            <p className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-3">How blocs are defined</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-2">
              {[
                { bloc: 'Western', desc: 'Cables built by US, European, or Japanese manufacturers' },
                { bloc: 'Chinese', desc: 'Cables built by Chinese-owned or state-affiliated manufacturers' },
                { bloc: 'Mixed',   desc: 'Cables with both Chinese and Western manufacturers' },
                { bloc: 'Other',   desc: 'Cables built by manufacturers outside these blocs' },
                { bloc: 'Unknown', desc: 'Supplier information not publicly available' },
              ].map(({ bloc, desc }) => (
                <div key={bloc} className="flex items-start gap-2">
                  <span className="mt-1 text-[#9E9E9E] text-xs">—</span>
                  <span className="text-xs text-[#616161]">
                    <span className="font-semibold text-[#212121]">{bloc}:</span> {desc}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Owner Market Share */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Ownership Structure by Bloc</h2>
          <p className="text-sm text-[#616161] mb-6">
            Distribution of cable ownership across geopolitical blocs.
          </p>
          <div className="space-y-4 mb-8">
            {Object.entries(ownerBlocCounts)
              .sort(([,a], [,b]) => b - a)
              .map(([bloc, count]) => renderBar(bloc, count, data.length))}
          </div>
          <div className="border-t border-[#E0E0E0] pt-6">
            <p className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-3">How blocs are defined</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-2">
              {[
                { bloc: 'Western', desc: 'Cables owned by entities based in the US, Europe, Japan, or Australia' },
                { bloc: 'Chinese', desc: 'Cables owned by Chinese state or private entities' },
                { bloc: 'Mixed',   desc: 'Cables with ownership shared across Chinese and Western entities' },
                { bloc: 'Other',   desc: 'Cables owned by entities in the Global South or regional telecoms' },
                { bloc: 'Unknown', desc: 'Ownership information not publicly available' },
              ].map(({ bloc, desc }) => (
                <div key={bloc} className="flex items-start gap-2">
                  <span className="mt-1 text-[#9E9E9E] text-xs">—</span>
                  <span className="text-xs text-[#616161]">
                    <span className="font-semibold text-[#212121]">{bloc}:</span> {desc}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Concentration Indicators — all three numbers in calm red */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Market Concentration Indicators</h2>
          <p className="text-sm text-[#616161] mb-6">Key indices measuring market structure and competition</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">Supplier HHI</h3>
              <div className="font-serif text-5xl font-bold text-[#C62828] my-4">{supplierHHI.toLocaleString()}</div>
              <p className="text-sm text-[#616161]">Highly concentrated market (&gt;2500)</p>
            </div>
            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">Owner HHI</h3>
              <div className="font-serif text-5xl font-bold text-[#C62828] my-4">{ownerHHI.toLocaleString()}</div>
              <p className="text-sm text-[#616161]">Highly concentrated ownership (&gt;2500)</p>
            </div>
            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">Growth Rate</h3>
              <div className="font-serif text-5xl font-bold text-[#C62828] my-4">20x</div>
              <p className="text-sm text-[#616161]">Chinese supplier participation (Pre/Post 2013)</p>
            </div>
          </div>
        </div>
      </section>

      {/* Recent Cables */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Recent Cables</h2>
          <p className="text-sm text-[#616161] mb-6">
            Most recent submarine cable deployments (showing ownership for better data coverage)
          </p>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b-2 border-[#E0E0E0]">
                  <th className="px-4 py-3.5 text-left text-xs uppercase text-[#616161] font-semibold tracking-wider">Cable Name</th>
                  <th className="px-4 py-3.5 text-left text-xs uppercase text-[#616161] font-semibold tracking-wider">Year</th>
                  <th className="px-4 py-3.5 text-left text-xs uppercase text-[#616161] font-semibold tracking-wider">Owner Bloc</th>
                  <th className="px-4 py-3.5 text-left text-xs uppercase text-[#616161] font-semibold tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody>
                {data
                  .slice()
                  .sort((a, b) => (parseFloat(b.rfs_year) || 0) - (parseFloat(a.rfs_year) || 0))
                  .slice(0, 10)
                  .map((cable, idx) => (
                    <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3.5 text-sm text-gray-800">{cable.cable_name}</td>
                      <td className="px-4 py-3.5 text-sm text-gray-800">{cable.rfs_year || 'N/A'}</td>
                      <td className="px-4 py-3.5">
                        <span className={`inline-block px-3 py-1.5 text-xs font-semibold rounded ${
                          cable.owner_bloc?.toLowerCase() === 'chinese' ? 'bg-red-100 text-red-800' :
                          cable.owner_bloc?.toLowerCase() === 'western' ? 'bg-blue-100 text-blue-800' :
                          cable.owner_bloc?.toLowerCase() === 'mixed'   ? 'bg-purple-100 text-purple-800' :
                          cable.owner_bloc?.toLowerCase() === 'other'   ? 'bg-gray-100 text-gray-700' :
                          'bg-gray-50 text-gray-500'
                        }`}>
                          {cable.owner_bloc || 'Unknown'}
                        </span>
                      </td>
                      <td className="px-4 py-3.5 text-sm text-gray-800">{cable.status}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  )
}

export default SystemOverview