import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

function SovereigntyDependency({ infrastructureType = 'cables' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [perspective, setPerspective] = useState('owner')
  const [hoveredCountry, setHoveredCountry] = useState(null)
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  const [searchTerm, setSearchTerm] = useState('')
  const [highlightedCountry, setHighlightedCountry] = useState(null)

  useEffect(() => {
    async function loadData() {
      const { data: countries, error } = await supabase
        .from('sovereignty_countries')
        .select('*')
      
      if (error) {
        console.error('Error:', error)
        setLoading(false)
        return
      }
  
      const formattedData = {
        countries: countries,
        global_stats: {
          supplier_perspective: {
            avg_sovereignty_index: countries.reduce((sum, c) => sum + c.supplier_sovereignty_index, 0) / countries.length,
            avg_diversification: countries.reduce((sum, c) => sum + c.supplier_diversification, 0) / countries.length,
            single_supplier_dependent: countries.filter(c => c.supplier_diversification < 0.5).length
          },
          owner_perspective: {
            avg_sovereignty_index: countries.reduce((sum, c) => sum + c.owner_sovereignty_index, 0) / countries.length,
            avg_diversification: countries.reduce((sum, c) => sum + c.owner_diversification, 0) / countries.length,
            single_owner_dependent: countries.filter(c => c.owner_diversification < 0.5).length
          }
        }
      }
      
      setData(formattedData)
      setLoading(false)
    }
    
    loadData()
  }, [infrastructureType])

  // Handle search
  const handleSearch = (value) => {
    setSearchTerm(value)
    if (value.trim() === '') {
      setHighlightedCountry(null)
      return
    }
    
    const found = countriesForViz.find(c => 
      c.country.toLowerCase().includes(value.toLowerCase())
    )
    setHighlightedCountry(found ? found.country : null)
  }

  if (loading) return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="w-10 h-10 border-4 border-gray-200 border-t-[#0D47A1] rounded-full animate-spin mb-4"></div>
    </div>
  )
  
  if (!data || !data.countries) return (
    <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
      Data not available
    </div>
  )

  const metrics = perspective === 'supplier' 
    ? {
        sovereignty: 'supplier_sovereignty_index',
        diversification: 'supplier_diversification',
        cn_pct: 'pct_chinese_supplier'
      }
    : {
        sovereignty: 'owner_sovereignty_index',
        diversification: 'owner_diversification',
        cn_pct: 'pct_chinese_owner'
      }

  const stats = perspective === 'supplier' 
    ? data.global_stats.supplier_perspective
    : data.global_stats.owner_perspective

  const countriesForViz = data.countries.filter(c => c.total_cables >= 3)

  const concentrationRisks = data.countries
    .filter(c => c[metrics.sovereignty] < 0.6 && c.total_cables >= 10)
    .map(c => ({
      ...c,
      riskType: c[metrics.cn_pct] > 20 ? 'High Chinese supplier share (>20%)' :
                c[metrics.diversification] < 0.4 ? 'Limited supplier diversification' :
                'Single-bloc dominance (>50%)'
    }))

  const groupedRisks = concentrationRisks.reduce((acc, c) => {
    if (!acc[c.riskType]) acc[c.riskType] = []
    acc[c.riskType].push(c)
    return acc
  }, {})

  return (
    <div>
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Sovereignty & Dependency</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Infrastructure sovereignty analysis across {data.countries.length} countries
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6 mb-10">
        <label className="text-sm font-semibold text-[#616161] mr-3">Analysis Perspective:</label>
        <select 
          value={perspective}
          onChange={e => setPerspective(e.target.value)}
          className="px-4 py-2.5 rounded border border-[#E0E0E0] text-sm font-medium bg-white"
        >
          <option value="owner">Owner Perspective</option>
          <option value="supplier">Supplier Perspective</option>
        </select>
      </div>

      <section className="mb-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{data.countries.length}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">Countries</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{stats.avg_sovereignty_index.toFixed(3)}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">Global Average</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">
              {countriesForViz.filter(c => c[metrics.sovereignty] > 0.7).length}
            </div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">High Sovereignty</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{concentrationRisks.length}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">High Concentration Risk</div>
          </div>
        </div>
      </section>

      {/* Scatter Plot with Search */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Sovereignty vs Infrastructure Density</h2>
              <p className="text-sm text-[#616161] leading-relaxed">
                Search for a country or hover over dots for details (showing countries with 3+ cables)
              </p>
            </div>

            {/* Search Bar */}
            <div className="ml-6 w-80">
              <input
                type="text"
                placeholder="Search country (e.g., China, Singapore)..."
                value={searchTerm}
                onChange={(e) => handleSearch(e.target.value)}
                className="w-full px-4 py-2.5 border border-[#E0E0E0] rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-[#0D47A1] focus:border-transparent"
              />
              {highlightedCountry && (
                <div className="mt-2 text-xs text-[#0D47A1]">
                  ✓ Highlighting: {highlightedCountry}
                </div>
              )}
              {searchTerm && !highlightedCountry && (
                <div className="mt-2 text-xs text-[#C62828]">
                  No country found matching "{searchTerm}"
                </div>
              )}
            </div>
          </div>

          <div className="mt-8 bg-[#FAFAFA] p-8 rounded-lg relative">
            <svg 
              viewBox="0 0 1000 500" 
              className="w-full h-auto"
              onMouseMove={(e) => {
                const rect = e.currentTarget.getBoundingClientRect()
                setMousePos({ 
                  x: e.clientX - rect.left, 
                  y: e.clientY - rect.top 
                })
              }}
              onMouseLeave={() => setHoveredCountry(null)}
            >
              <defs>
                <linearGradient id="riskGradient" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#FFEBEE" />
                  <stop offset="50%" stopColor="#FFF3E0" />
                  <stop offset="100%" stopColor="#E8F5E9" />
                </linearGradient>
                <filter id="highlightGlow">
                  <feGaussianBlur stdDeviation="4" result="blur"/>
                  <feMerge>
                    <feMergeNode in="blur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>

              <rect x="80" y="40" width="880" height="400" fill="url(#riskGradient)" opacity="0.25" />

              <g stroke="#E0E0E0" strokeWidth="1">
                {[0.2, 0.4, 0.6, 0.8].map(val => (
                  <line key={`h${val}`} x1="80" y1={440 - val * 400} x2="960" y2={440 - val * 400} />
                ))}
                {[20, 40, 60, 80].map(val => (
                  <line key={`v${val}`} x1={80 + val * 11} y1="40" x2={80 + val * 11} y2="440" />
                ))}
              </g>

              <line x1="80" y1="440" x2="960" y2="440" stroke="#424242" strokeWidth="2" />
              <line x1="80" y1="40" x2="80" y2="440" stroke="#424242" strokeWidth="2" />

              {[0, 0.2, 0.4, 0.6, 0.8, 1.0].map(val => (
                <text key={val} x="60" y={440 - val * 400 + 5} fontSize="12" fill="#616161" textAnchor="end">
                  {val.toFixed(1)}
                </text>
              ))}

              {[0, 20, 40, 60, 80, 100].map(val => (
                <text key={val} x={80 + val * 11} y="460" fontSize="12" fill="#616161" textAnchor="middle">
                  {val}
                </text>
              ))}

              <text x="500" y="490" fontSize="14" fill="#212121" textAnchor="middle" fontWeight="600">
                Number of Cables →
              </text>
              <text x="30" y="240" fontSize="14" fill="#212121" textAnchor="middle" fontWeight="600" transform="rotate(-90 30 240)">
                Sovereignty Index →
              </text>

              {countriesForViz.map(c => {
                const x = 80 + Math.min(c.total_cables, 100) * 8.8
                const y = 440 - c[metrics.sovereignty] * 400
                const size = Math.min(Math.max(c.total_cables / 3, 6), 20)
                
                const isHighlighted = highlightedCountry === c.country
                const isHovered = hoveredCountry === c.country
                
                const color = c[metrics.sovereignty] > 0.7 ? '#2E7D32' :
                             c[metrics.sovereignty] > 0.6 ? '#689F38' :
                             c[metrics.sovereignty] > 0.5 ? '#FFA726' :
                             '#D32F2F'

                return (
                  <circle
                    key={c.country}
                    cx={x}
                    cy={y}
                    r={isHighlighted ? size * 1.5 : size}
                    fill={color}
                    opacity={isHighlighted ? 1 : (isHovered ? 1 : 0.7)}
                    stroke={isHighlighted ? '#0D47A1' : (isHovered ? '#212121' : 'white')}
                    strokeWidth={isHighlighted ? 4 : (isHovered ? 3 : 2)}
                    className="cursor-pointer transition-all"
                    filter={isHighlighted ? "url(#highlightGlow)" : "none"}
                    onMouseEnter={() => setHoveredCountry(c.country)}
                    onMouseLeave={() => setHoveredCountry(null)}
                  />
                )
              })}

              <text x="850" y="100" fontSize="13" fill="#2E7D32" fontWeight="600" opacity="0.5">High Sovereignty, Major Infrastructure</text>
              <text x="820" y="420" fontSize="13" fill="#D32F2F" fontWeight="600" opacity="0.5">Concentration Risk</text>
            </svg>

            {/* Tooltip */}
            {(hoveredCountry || highlightedCountry) && (
              <div 
                className="absolute bg-gray-900/95 text-white px-4 py-3 rounded-md text-sm pointer-events-none z-50 shadow-xl min-w-[200px]"
                style={{ 
                  left: highlightedCountry ? '50%' : mousePos.x + 15, 
                  top: highlightedCountry ? 20 : mousePos.y - 10,
                  transform: highlightedCountry ? 'translateX(-50%)' : 'none'
                }}
              >
                {(() => {
                  const displayCountry = hoveredCountry || highlightedCountry
                  const c = countriesForViz.find(country => country.country === displayCountry)
                  if (!c) return null
                  return (
                    <>
                      <div className="font-bold text-base mb-2">{c.country}</div>
                      <div className="text-sm opacity-90 space-y-0.5">
                        <div>Cables: {c.total_cables}</div>
                        <div>Sovereignty: {c[metrics.sovereignty].toFixed(3)}</div>
                        <div>Diversification: {c[metrics.diversification].toFixed(3)}</div>
                        <div>Chinese: {c[metrics.cn_pct].toFixed(1)}%</div>
                      </div>
                    </>
                  )
                })()}
              </div>
            )}

            <div className="mt-8 flex justify-center gap-10 text-sm text-[#616161]">
              <div className="flex items-center gap-2">
                <div className="w-3.5 h-3.5 rounded-full bg-[#2E7D32] border-2 border-white"></div>
                <span>High (&gt;0.7)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3.5 h-3.5 rounded-full bg-[#FFA726] border-2 border-white"></div>
                <span>Medium (0.5-0.6)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3.5 h-3.5 rounded-full bg-[#D32F2F] border-2 border-white"></div>
                <span>Low (&lt;0.5)</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Rest of component stays the same... */}
      {/* Dependency Assessment */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Infrastructure Dependency Assessment</h2>
          <p className="text-sm text-[#616161] mb-8 leading-relaxed">
            Countries with significant infrastructure (≥10 cables) and high concentration risk (sovereignty &lt;0.6)
          </p>

          {Object.keys(groupedRisks).length > 0 ? (
            <div className="space-y-10">
              {Object.entries(groupedRisks).map(([type, countries]) => (
                <div key={type}>
                  <div className="p-3 bg-[#F5F5F5] border-l-4 border-[#E65100] mb-4 rounded">
                    <h3 className="font-serif text-base font-semibold m-0 text-[#212121]">{type}</h3>
                    <p className="text-xs text-[#757575] mt-1 m-0">
                      {countries.length} {countries.length === 1 ? 'country' : 'countries'} • {countries.reduce((sum, c) => sum + c.total_cables, 0)} total cables
                    </p>
                  </div>

                  <table className="w-full text-sm border-collapse">
                    <thead>
                      <tr className="border-b-2 border-[#E0E0E0]">
                        <th className="text-left py-3 px-3 font-semibold text-[#616161] text-xs uppercase">Country</th>
                        <th className="text-right py-3 px-3 font-semibold text-[#616161] text-xs uppercase">Cables</th>
                        <th className="text-right py-3 px-3 font-semibold text-[#616161] text-xs uppercase">Sovereignty</th>
                        <th className="text-right py-3 px-3 font-semibold text-[#616161] text-xs uppercase">Dominant Bloc</th>
                      </tr>
                    </thead>
                    <tbody>
                      {countries.map((c, idx) => {
                        // Get ALL bloc percentages
                        const allBlocs = {
                          'China': c[perspective === 'supplier' ? 'pct_chinese_supplier' : 'pct_chinese_owner'] || 0,
                          'US': c[perspective === 'supplier' ? 'pct_us_supplier' : 'pct_us_owner'] || 0,
                          'EU': c[perspective === 'supplier' ? 'pct_eu_supplier' : 'pct_eu_owner'] || 0,
                          'Japan': c[perspective === 'supplier' ? 'pct_japan_supplier' : 'pct_japan_owner'] || 0,
                          'India': c[perspective === 'supplier' ? 'pct_india_supplier' : 'pct_india_owner'] || 0,
                          'Mixed': c[perspective === 'supplier' ? 'pct_mixed_supplier' : 'pct_mixed_owner'] || 0,
                          'Other': c[perspective === 'supplier' ? 'pct_other_supplier' : 'pct_other_owner'] || 0
                        }
                        
                        // Find true dominant
                        const [dominantName, dominantPct] = Object.entries(allBlocs)
                          .sort(([,a], [,b]) => b - a)[0]
                        
                        const blocColor = dominantName === 'China' ? 'bg-red-100 text-red-800' :
                                        dominantName === 'US' ? 'bg-blue-100 text-blue-800' :
                                        dominantName === 'EU' ? 'bg-purple-100 text-purple-800' :
                                        dominantName === 'Japan' ? 'bg-teal-100 text-teal-800' :
                                        dominantName === 'India' ? 'bg-orange-100 text-orange-800' :
                                        dominantName === 'Mixed' ? 'bg-indigo-100 text-indigo-800' :
                                        'bg-gray-100 text-gray-700'
                        
                        return (
                          <tr key={c.country} className={idx < countries.length - 1 ? 'border-b border-[#F0F0F0]' : ''}>
                            <td className="py-3 px-3 font-medium">{c.country}</td>
                            <td className="py-3 px-3 text-right text-[#616161]">{c.total_cables}</td>
                            <td className="py-3 px-3 text-right">
                              <span className="font-semibold text-[#D32F2F]">
                                {c[metrics.sovereignty].toFixed(3)}
                              </span>
                            </td>
                            <td className="py-3 px-3 text-right">
                              <span className={`inline-block px-2.5 py-1 text-xs font-semibold rounded ${blocColor}`}>
                                {dominantName} ({dominantPct.toFixed(0)}%)
                              </span>
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
          ) : (
            <div className="mt-8 p-8 text-center bg-[#F5F5F5] rounded-lg border border-[#E0E0E0]">
              <p className="text-base text-[#616161] m-0">
                No countries meet high concentration criteria (sovereignty &lt;0.6 with ≥10 cables)
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Rankings */}
      <section className="mb-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Highest Sovereignty Scores</h2>
            
            {data.countries
              .sort((a, b) => b[metrics.sovereignty] - a[metrics.sovereignty])
              .slice(0, 8)
              .map((c, idx) => (
                <div key={c.country} className={`py-3 flex justify-between ${idx < 7 ? 'border-b border-[#F0F0F0]' : ''}`}>
                  <div className="flex gap-4">
                    <span className="font-bold text-[#9E9E9E] text-base w-5">{idx + 1}</span>
                    <div>
                      <div className="font-semibold text-base">{c.country}</div>
                      <div className="text-xs text-[#9E9E9E]">{c.total_cables} cables</div>
                    </div>
                  </div>
                  <div className="font-bold text-base text-[#2E7D32]">
                    {c[metrics.sovereignty].toFixed(3)}
                  </div>
                </div>
              ))}
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
            <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Highest Concentration Risk</h2>
            
            {data.countries
              .filter(c => c.total_cables >= 5)
              .sort((a, b) => a[metrics.sovereignty] - b[metrics.sovereignty])
              .slice(0, 8)
              .map((c, idx) => (
                <div key={c.country} className={`py-3 flex justify-between ${idx < 7 ? 'border-b border-[#F0F0F0]' : ''}`}>
                  <div className="flex gap-4">
                    <span className="text-base w-5">⚠️</span>
                    <div>
                      <div className="font-semibold text-base">{c.country}</div>
                      <div className="text-xs text-[#9E9E9E]">{c.total_cables} cables</div>
                    </div>
                  </div>
                  <div className="font-bold text-base text-[#D32F2F]">
                    {c[metrics.sovereignty].toFixed(3)}
                  </div>
                </div>
              ))}
          </div>
        </div>
      </section>

      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h3 className="font-serif text-base font-semibold mb-3">Methodology (Updated)</h3>
          <p className="text-sm leading-relaxed text-[#616161] m-0">
            Sovereignty Index = 40% Diversification + 30% Independence (domestic control) + 20% No Dominance + 10% Redundancy. 
            <strong className="text-[#0D47A1]">Independence now measures % domestic suppliers/owners (bloc-neutral)</strong>, 
            not specifically Chinese presence. This allows all countries, including China, to score high sovereignty when infrastructure is domestically controlled.
          </p>
        </div>
      </section>
    </div>
  )
}

export default SovereigntyDependency