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

      // Calculate market structure from raw cables
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

      // Entry timing - earliest year for each bloc
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

      // Supplier-Owner divergence patterns
      let chineseSupplierWesternOwner = 0
      let westernSupplierChineseOwner = 0
      let fullyChineseControlled = 0
      let fullyWesternControlled = 0

      cables.forEach(cable => {
        const supplier = cable.supplier_bloc
        const owner = cable.owner_bloc
        
        if (supplier === 'China' && (owner === 'US' || owner === 'Europe')) {
          chineseSupplierWesternOwner++
        }
        if ((supplier === 'US' || supplier === 'Europe') && owner === 'China') {
          westernSupplierChineseOwner++
        }
        if (supplier === 'China' && owner === 'China') {
          fullyChineseControlled++
        }
        if ((supplier === 'US' || supplier === 'Europe') && (owner === 'US' || owner === 'Europe')) {
          fullyWesternControlled++
        }
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

            <div className="space-y-4">
              {Object.entries(data.supplier_competition.market_share)
                .filter(([bloc]) => bloc !== 'Unknown')
                .sort(([,a], [,b]) => b - a)
                .map(([bloc, count]) => {
                  const percentage = ((count / data.totalCables) * 100).toFixed(1)
                  return (
                    <div key={bloc} className="flex items-center gap-4">
                      <div className="min-w-[100px] text-sm font-medium text-[#212121]">{bloc}</div>
                      <div className="flex-1 bg-[#E0E0E0] rounded h-9 relative overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-[#0D47A1] to-[#0097A7] rounded flex items-center justify-end pr-3 transition-all duration-300"
                          style={{ width: `${percentage}%` }}
                        >
                          <span className="text-white text-xs font-semibold">{percentage}%</span>
                        </div>
                      </div>
                      <div className="min-w-[90px] text-right text-sm text-[#616161] font-medium">
                        {count} cables
                      </div>
                    </div>
                  )
                })}
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
                  
                  const blocColors = {
                    'China': 'bg-red-100 text-red-800',
                    'Europe': 'bg-purple-100 text-purple-800',
                    'Japan': 'bg-teal-100 text-teal-800',
                    'India': 'bg-orange-100 text-orange-800',
                    'US': 'bg-blue-100 text-blue-800',
                    'Mixed': 'bg-indigo-100 text-indigo-800',
                    'Other': 'bg-gray-100 text-gray-700'
                  }
                  
                  return (
                    <div 
                      key={bloc} 
                      className="grid grid-cols-[100px_100px_1fr_120px] gap-4 p-4 bg-white rounded-md mb-3 border border-[#E0E0E0] items-center transition-shadow cursor-pointer hover:shadow-md"
                    >
                      <div className="text-xl font-bold text-[#2196f3]">
                        {Math.round(year)}
                      </div>
                      
                      <div className="text-base text-[#616161]">
                        {yearsActive} years
                      </div>

                      <div>
                        <div className="flex items-center gap-2 mb-1.5">
                          <span className={`inline-block px-3 py-1 text-xs font-semibold rounded ${blocColors[bloc] || 'bg-gray-100 text-gray-700'}`}>
                            {bloc}
                          </span>
                          <span className="text-sm font-semibold text-[#212121]">
                            {percentage}%
                          </span>
                        </div>
                        <div className="h-2 bg-[#F0F0F0] rounded overflow-hidden">
                          <div 
                            className="h-full rounded transition-all duration-300"
                            style={{ 
                              width: `${percentage}%`,
                              backgroundColor: bloc === 'China' ? '#E74C3C' :
                                             bloc === 'Europe' ? '#9C27B0' :
                                             bloc === 'Japan' ? '#00BCD4' :
                                             bloc === 'India' ? '#FF9800' : '#757575'
                            }}
                          ></div>
                        </div>
                      </div>

                      <div className="text-right text-base font-semibold">
                        {currentShare}
                      </div>
                    </div>
                  )
                })}
            </div>

            <div className="mt-6 p-4 bg-[#F0F7FF] rounded border border-[#64B5F6]">
              <p className="text-sm text-[#1565C0] m-0 leading-relaxed">
                <strong>Insight:</strong> China entered most recently (2009) but has achieved 4.4% market share in just 17 years. 
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

            <div className="space-y-4">
              {Object.entries(data.ownership_structure.market_share)
                .filter(([bloc]) => bloc !== 'Unknown')
                .sort(([,a], [,b]) => b - a)
                .map(([bloc, count]) => {
                  const percentage = ((count / data.totalCables) * 100).toFixed(1)
                  return (
                    <div key={bloc} className="flex items-center gap-4">
                      <div className="min-w-[100px] text-sm font-medium text-[#212121]">{bloc}</div>
                      <div className="flex-1 bg-[#E0E0E0] rounded h-9 relative overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-[#0D47A1] to-[#0097A7] rounded flex items-center justify-end pr-3 transition-all duration-300"
                          style={{ width: `${percentage}%` }}
                        >
                          <span className="text-white text-xs font-semibold">{percentage}%</span>
                        </div>
                      </div>
                      <div className="min-w-[90px] text-right text-sm text-[#616161] font-medium">
                        {count} cables
                      </div>
                    </div>
                  )
                })}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-8">Ownership Concentration</h2>
            <div className="py-12 text-center">
              <div className="text-6xl font-bold text-[#E74C3C] font-serif">
                {data.ownership_structure.global_hhi.toLocaleString()}
              </div>
              <div className="text-xl text-[#616161] mt-4">
                Owner HHI Score
              </div>
              <div className="text-sm text-[#9E9E9E] mt-3 max-w-lg mx-auto leading-relaxed">
                Highly concentrated ownership market. Values &gt;2500 indicate limited competition.
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Ownership Type Analysis</h2>
            <p className="text-sm text-[#616161] mb-6 leading-relaxed">
              State-owned vs private ownership patterns (data collection in progress)
            </p>
            <div className="py-8 text-center text-[#9E9E9E]">
              <p className="text-base">🚧 Ownership type classification requires additional data coding</p>
              <p className="text-sm mt-2">Coming in future update</p>
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
              <div className="p-8 bg-[#FFF3E0] rounded-lg border-2 border-[#FF9800]">
                <div className="text-5xl font-bold text-[#F57C00] font-serif">
                  {data.supplier_owner_divergence.chinese_supplier_western_owner}
                </div>
                <div className="text-base font-semibold mt-2 text-[#212121]">
                  Chinese Supplier + Western Owner
                </div>
                <div className="text-sm text-[#616161] mt-2 leading-relaxed">
                  Western entities own cables built by Chinese suppliers
                </div>
              </div>

              <div className="p-8 bg-[#E3F2FD] rounded-lg border-2 border-[#2196F3]">
                <div className="text-5xl font-bold text-[#1976D2] font-serif">
                  {data.supplier_owner_divergence.western_supplier_chinese_owner}
                </div>
                <div className="text-base font-semibold mt-2 text-[#212121]">
                  Western Supplier + Chinese Owner
                </div>
                <div className="text-sm text-[#616161] mt-2 leading-relaxed">
                  Chinese entities own cables built by Western suppliers
                </div>
              </div>

              <div className="p-8 bg-[#FFEBEE] rounded-lg border-2 border-[#E74C3C]">
                <div className="text-5xl font-bold text-[#C62828] font-serif">
                  {data.supplier_owner_divergence.fully_chinese}
                </div>
                <div className="text-base font-semibold mt-2 text-[#212121]">
                  Fully Chinese-Controlled
                </div>
                <div className="text-sm text-[#616161] mt-2 leading-relaxed">
                  Both supplier and owner are Chinese entities
                </div>
              </div>

              <div className="p-8 bg-[#F3E5F5] rounded-lg border-2 border-[#9C27B0]">
                <div className="text-5xl font-bold text-[#7B1FA2] font-serif">
                  {data.supplier_owner_divergence.fully_western}
                </div>
                <div className="text-base font-semibold mt-2 text-[#212121]">
                  Fully Western-Controlled
                </div>
                <div className="text-sm text-[#616161] mt-2 leading-relaxed">
                  Both supplier and owner are US or European
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