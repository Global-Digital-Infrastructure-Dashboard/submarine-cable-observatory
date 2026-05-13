import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

function MarketStructure({ infrastructureType = 'cables' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeSection, setActiveSection] = useState('supplier-competition')

  useEffect(() => {
    async function loadAndProcess() {
      const { data: cables, error } = await supabase
        .from('submarinecables')
        .select('*')
      
      if (error) {
        console.error('Error loading cables:', error)
        setLoading(false)
        return
      }

      const supplierMarketShare = cables.reduce((acc, cable) => {
        const bloc = cable.supplier_bloc || 'Unknown'
        acc[bloc] = (acc[bloc] || 0) + 1
        return acc
      }, {})

      const ownerMarketShare = cables.reduce((acc, cable) => {
        const bloc = cable.owner_bloc || 'Unknown'
        acc[bloc] = (acc[bloc] || 0) + 1
        return acc
      }, {})

      const entryTiming = {}
      cables.forEach(cable => {
        const bloc = cable.supplier_bloc
        const year = parseFloat(cable.rfs_year)
        if (bloc && year && !isNaN(year)) {
          if (!entryTiming[bloc] || year < entryTiming[bloc]) {
            entryTiming[bloc] = year
          }
        }
      })

      // Fixed: use actual bloc values 'Chinese' and 'Western'
      let chineseSupplierWesternOwner = 0
      let westernSupplierChineseOwner = 0
      let fullyChineseControlled = 0
      let fullyWesternControlled = 0

      cables.forEach(cable => {
        const supplier = cable.supplier_bloc
        const owner = cable.owner_bloc
        if (supplier === 'Chinese' && owner === 'Western') chineseSupplierWesternOwner++
        if (supplier === 'Western' && owner === 'Chinese') westernSupplierChineseOwner++
        if (supplier === 'Chinese' && owner === 'Chinese') fullyChineseControlled++
        if (supplier === 'Western' && owner === 'Western') fullyWesternControlled++
      })

      setData({
        supplier_competition: {
          market_share: supplierMarketShare,
          entry_timing: entryTiming,
          global_hhi: 3020
        },
        ownership_structure: {
          market_share: ownerMarketShare,
          global_hhi: 3780
        },
        supplier_owner_divergence: {
          chinese_supplier_western_owner: chineseSupplierWesternOwner,
          western_supplier_chinese_owner: westernSupplierChineseOwner,
          fully_chinese: fullyChineseControlled,
          fully_western: fullyWesternControlled
        },
        totalCables: cables.length
      })
      setLoading(false)
    }
    
    loadAndProcess()
  }, [infrastructureType])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <div className="w-10 h-10 border-4 border-gray-200 border-t-[#0D47A1] rounded-full animate-spin mb-4"></div>
        <p className="text-[#616161]">Loading market structure data...</p>
      </div>
    )
  }

  if (!data) return (
    <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
      Error loading data
    </div>
  )

  const sections = [
    { id: 'supplier-competition', label: 'A. Supplier Competition' },
    { id: 'ownership-structure', label: 'B. Ownership Structure' },
    { id: 'supplier-owner-divergence', label: 'C. Supplier-Owner Divergence' }
  ]

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

  const supplierLegend = [
    { bloc: 'Western', desc: 'Cables built by US, European, or Japanese manufacturers' },
    { bloc: 'Chinese', desc: 'Cables built by Chinese-owned or state-affiliated manufacturers' },
    { bloc: 'Mixed',   desc: 'Cables with both Chinese and Western manufacturers' },
    { bloc: 'Other',   desc: 'Cables built by manufacturers outside these blocs' },
    { bloc: 'Unknown', desc: 'Supplier information not publicly available' },
  ]

  const ownerLegend = [
    { bloc: 'Western', desc: 'Cables owned by entities based in the US, Europe, Japan, or Australia' },
    { bloc: 'Chinese', desc: 'Cables owned by Chinese state or private entities' },
    { bloc: 'Mixed',   desc: 'Cables with ownership shared across Chinese and Western entities' },
    { bloc: 'Other',   desc: 'Cables owned by entities in the Global South or regional telecoms' },
    { bloc: 'Unknown', desc: 'Ownership information not publicly available' },
  ]

  return (
    <div>
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Market Structure</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Industrial organization perspective on supplier competition, ownership patterns,
          and control dynamics in submarine cable infrastructure.
        </p>
      </div>

      {/* Section Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-2 mb-10">
        <div className="flex gap-2 flex-wrap">
          {sections.map(section => (
            <button
              key={section.id}
              className={`flex-1 min-w-[200px] px-5 py-3 text-sm font-medium rounded transition-all ${
                activeSection === section.id
                  ? 'bg-[#0D47A1] text-white shadow-md'
                  : 'bg-white text-[#616161] hover:bg-[#FAFAFA] hover:text-[#0D47A1]'
              }`}
              onClick={() => setActiveSection(section.id)}
            >
              {section.label}
            </button>
          ))}
        </div>
      </div>

      {/* A. Supplier Competition */}
      {activeSection === 'supplier-competition' && (
        <div className="space-y-10">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Market Share by Supplier Bloc</h2>
            <p className="text-sm text-[#616161] mb-6 leading-relaxed">
              Current distribution of submarine cable suppliers across geopolitical blocs
            </p>
            <div className="space-y-4 mb-8">
              {Object.entries(data.supplier_competition.market_share)
                .sort(([,a], [,b]) => b - a)
                .map(([bloc, count]) => renderBar(bloc, count, data.totalCables))}
            </div>
            <div className="border-t border-[#E0E0E0] pt-6">
              <p className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-3">How blocs are defined</p>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-2">
                {supplierLegend.map(({ bloc, desc }) => (
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

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Market Entry & Evolution</h2>
            <p className="text-sm text-[#616161] mb-6 leading-relaxed">
              When blocs entered the market, years active, and current market position
            </p>

            <div className="mt-6">
              <div className="grid grid-cols-[100px_100px_1fr_120px] gap-4 p-3 bg-[#F5F5F5] rounded mb-3 text-xs font-semibold text-[#616161] uppercase">
                <div>Entry Year</div>
                <div>Years Active</div>
                <div>Current Market Share</div>
                <div className="text-right">Cables</div>
              </div>

              {Object.entries(data.supplier_competition.entry_timing)
                .filter(([bloc]) => bloc !== 'Unknown')
                .sort(([,a], [,b]) => a - b)
                .map(([bloc, year]) => {
                  const yearsActive = 2026 - Math.round(year)
                  const currentShare = data.supplier_competition.market_share[bloc] || 0
                  const percentage = ((currentShare / data.totalCables) * 100).toFixed(1)
                  return (
                    <div
                      key={bloc}
                      className="grid grid-cols-[100px_100px_1fr_120px] gap-4 p-4 bg-white rounded-md mb-3 border border-[#E0E0E0] items-center hover:shadow-md transition-shadow"
                    >
                      <div className="text-xl font-bold text-[#0D47A1] font-serif">
                        {Math.round(year)}
                      </div>
                      <div className="text-base text-[#616161]">
                        {yearsActive} years
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-1.5">
                          <span className="inline-block px-3 py-1 text-xs font-semibold rounded bg-[#F5F5F5] text-[#212121]">
                            {bloc}
                          </span>
                          <span className="text-sm font-semibold text-[#212121]">{percentage}%</span>
                        </div>
                        <div className="h-2 bg-[#F0F0F0] rounded overflow-hidden">
                          <div
                            className="h-full bg-[#9E9E9E] rounded transition-all duration-300"
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                      </div>
                      <div className="text-right text-base font-semibold text-[#212121]">
                        {currentShare}
                      </div>
                    </div>
                  )
                })}
            </div>

            <div className="mt-6 p-4 bg-[#F5F5F5] rounded border-l-4 border-l-[#0D47A1]">
              <p className="text-sm text-[#424242] m-0 leading-relaxed">
                <span className="font-semibold">Insight:</span> China entered most recently (2009) but has achieved 4.4% market share in just 17 years.
                Europe, the earliest entrant (1990), maintains market leadership at 32%. Late entry doesn't prevent market impact.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* B. Ownership Structure */}
      {activeSection === 'ownership-structure' && (
        <div className="space-y-10">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Ownership Market Share by Bloc</h2>
            <p className="text-sm text-[#616161] mb-6 leading-relaxed">
              Distribution of cable ownership across geopolitical blocs
            </p>
            <div className="space-y-4 mb-8">
              {Object.entries(data.ownership_structure.market_share)
                .sort(([,a], [,b]) => b - a)
                .map(([bloc, count]) => renderBar(bloc, count, data.totalCables))}
            </div>
            <div className="border-t border-[#E0E0E0] pt-6">
              <p className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-3">How blocs are defined</p>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-2">
                {ownerLegend.map(({ bloc, desc }) => (
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

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Ownership Concentration</h2>
            <p className="text-sm text-[#616161] mb-6">Key indices measuring ownership structure and competition</p>
            <div className="py-12 text-center">
              <div className="font-serif text-6xl font-bold text-[#C62828]">
                {data.ownership_structure.global_hhi.toLocaleString()}
              </div>
              <div className="text-xl text-[#616161] mt-4">Owner HHI Score</div>
              <div className="text-sm text-[#9E9E9E] mt-3 max-w-lg mx-auto leading-relaxed">
                Highly concentrated ownership market. Values &gt;2500 indicate limited competition.
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Ownership Type Analysis</h2>
            <p className="text-sm text-[#616161] mb-6 leading-relaxed">
              State-owned vs private ownership breakdown
            </p>
            <div className="py-10 text-center border border-dashed border-[#E0E0E0] rounded-lg">
              <p className="text-sm font-medium text-[#616161]">Coming in a future update</p>
              <p className="text-xs text-[#9E9E9E] mt-1">Ownership type classification requires additional data coding</p>
            </div>
          </div>
        </div>
      )}

      {/* C. Supplier-Owner Divergence */}
      {activeSection === 'supplier-owner-divergence' && (
        <div className="space-y-10">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Supplier-Owner Control Patterns</h2>
            <p className="text-sm text-[#616161] mb-8 leading-relaxed">
              Analysis of alignment and divergence between cable suppliers and owners reveals
              the complexity of infrastructure control beyond simple national affiliations.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="p-8 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
                <div className="font-serif text-5xl font-bold text-[#212121] mb-3">
                  {data.supplier_owner_divergence.chinese_supplier_western_owner}
                </div>
                <div className="text-sm font-semibold text-[#212121] mb-2">
                  Chinese Supplier + Western Owner
                </div>
                <div className="text-xs text-[#616161] leading-relaxed">
                  Western entities own cables built by Chinese suppliers
                </div>
              </div>

              <div className="p-8 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
                <div className="font-serif text-5xl font-bold text-[#212121] mb-3">
                  {data.supplier_owner_divergence.western_supplier_chinese_owner}
                </div>
                <div className="text-sm font-semibold text-[#212121] mb-2">
                  Western Supplier + Chinese Owner
                </div>
                <div className="text-xs text-[#616161] leading-relaxed">
                  Chinese entities own cables built by Western suppliers
                </div>
              </div>

              <div className="p-8 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
                <div className="font-serif text-5xl font-bold text-[#212121] mb-3">
                  {data.supplier_owner_divergence.fully_chinese}
                </div>
                <div className="text-sm font-semibold text-[#212121] mb-2">
                  Fully Chinese-Controlled
                </div>
                <div className="text-xs text-[#616161] leading-relaxed">
                  Both supplier and owner are Chinese entities
                </div>
              </div>

              <div className="p-8 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
                <div className="font-serif text-5xl font-bold text-[#212121] mb-3">
                  {data.supplier_owner_divergence.fully_western}
                </div>
                <div className="text-sm font-semibold text-[#212121] mb-2">
                  Fully Western-Controlled
                </div>
                <div className="text-xs text-[#616161] leading-relaxed">
                  Both supplier and owner are Western entities
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default MarketStructure