import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import WorldCableMap from '../components/WorldCableMap'

function GeographicDistribution({ infrastructureType = 'cables' }) {
  const [countryData, setCountryData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      const { data: countries, error } = await supabase
        .from('countries_map')
        .select('*')
        .order('cables', { ascending: false })
      
      if (error) {
        console.error('Error:', error)
        setLoading(false)
        return
      }
  
      setCountryData({
        countries: countries,
        total_countries: countries.length,
        total_cables: countries.reduce((sum, c) => sum + c.cables, 0)
      })
      setLoading(false)
    }
    
    loadData()
  }, [infrastructureType])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <div className="w-10 h-10 border-4 border-gray-200 border-t-[#0D47A1] rounded-full animate-spin mb-4"></div>
        <p className="text-[#616161]">Loading geographic data...</p>
      </div>
    )
  }

  if (!countryData) {
    return (
      <div>
        <div className="mb-10">
          <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Geographic Distribution</h1>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <p className="text-[#616161]">Data not available. Run extract_countries_for_map.py</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Geographic Distribution</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Interactive world map showing {countryData.total_countries} countries with submarine cable infrastructure
        </p>
      </div>

      {/* Interactive Map */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Global Cable Landing Points</h2>
          <p className="text-sm text-[#616161] mb-6 leading-relaxed">
            Interactive map with actual geographic locations. Click markers for details.
          </p>

          <div className="mt-6">
            <WorldCableMap countries={countryData.countries} />
          </div>

          <div className="mt-6 flex justify-center gap-10 text-sm text-[#616161]">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#00E5FF] border-2 border-white"></div>
              <span>Major Hub (&gt;50 cables)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-[#00BCD4] border-2 border-white"></div>
              <span>Significant (20-50)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-[#4FC3F7] border-2 border-white"></div>
              <span>Active (10-20)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-[#4FC3F7] border-2 border-white"></div>
              <span>Present (&lt;10)</span>
            </div>
          </div>

          <div className="mt-6 p-5 bg-[#E3F2FD] rounded-md">
            <p className="text-sm text-[#0D47A1] m-0 leading-relaxed">
              <strong>Interactive Features:</strong> Scroll or use the +/− buttons to zoom, drag to pan. Click cyan dots to see country names and cable counts. Highlighted countries have at least one cable landing. 
              Larger, brighter dots indicate major cable hubs. For detailed cable routes and exact paths, visit{' '}
              <a href="https://www.submarinecablemap.com/" target="_blank" rel="noopener noreferrer" className="text-[#0D47A1] font-semibold underline">
                TeleGeography's Submarine Cable Map
              </a>.
            </p>
          </div>
        </div>
      </section>

      {/* Top Countries */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Top 20 Countries by Cable Infrastructure</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {countryData.countries.slice(0, 20).map((country, idx) => (
              <div 
                key={country.name} 
                className={`p-4 rounded-md flex justify-between items-center transition-all hover:-translate-y-0.5 hover:shadow-lg ${
                  idx < 5 
                    ? 'bg-[#E3F2FD] border-2 border-[#64B5F6]' 
                    : 'bg-[#FAFAFA] border border-[#E0E0E0]'
                }`}
              >
                <div>
                  <div className={`font-serif text-base ${idx < 5 ? 'font-bold' : 'font-semibold'} text-[#212121]`}>
                    {country.name}
                  </div>
                  {idx < 5 && (
                    <div className="text-xs text-[#757575] mt-0.5">
                      Rank #{idx + 1}
                    </div>
                  )}
                </div>
                <div className={`font-serif text-2xl font-bold ${idx < 5 ? 'text-[#0D47A1]' : 'text-[#616161]'}`}>
                  {country.cables}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Regional Insights */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Key Geographic Insights</h2>
          
          {(() => {
            const top = countryData.countries
            const top3 = top.slice(0, 3)

            const europeRegion = ['United Kingdom', 'France', 'Germany', 'Spain', 'Italy', 'Portugal', 'Netherlands', 'Denmark', 'Sweden', 'Norway', 'Finland', 'Ireland', 'Poland', 'Greece']
            const apacRegion = ['Japan', 'Singapore', 'China', 'Hong Kong', 'Taiwan', 'South Korea', 'Australia', 'Indonesia', 'Philippines', 'Malaysia', 'Thailand', 'Vietnam', 'India', 'New Zealand']

            const topEurope = top.filter(c => europeRegion.includes(c.name)).slice(0, 3)
            const topAPAC = top.filter(c => apacRegion.includes(c.name)).slice(0, 3)

            return (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                <div className="p-6 bg-[#F0F4FA] rounded-lg border border-[#E8EDF5] border-l-4 border-l-[#0D47A1]">
                  <h4 className="font-serif text-base font-semibold mb-3 text-[#212121]">Major Hubs</h4>
                  <p className="text-sm leading-relaxed text-[#616161] m-0">
                    {top3.map(c => `${c.name} (${c.cables})`).join(', ')} serve as the top cable landing hubs globally, connecting major trade routes and population centers.
                  </p>
                </div>

                <div className="p-6 bg-[#F0F4FA] rounded-lg border border-[#E8EDF5] border-l-4 border-l-[#0D47A1]">
                  <h4 className="font-serif text-base font-semibold mb-3 text-[#212121]">European Density</h4>
                  <p className="text-sm leading-relaxed text-[#616161] m-0">
                    {topEurope.length > 0
                      ? `${topEurope.map(c => `${c.name} (${c.cables})`).join(', ')} lead European cable infrastructure, forming a concentrated network hub serving as gateway between the Americas and Asia.`
                      : 'European cable infrastructure data loading...'}
                  </p>
                </div>

                <div className="p-6 bg-[#F0F4FA] rounded-lg border border-[#E8EDF5] border-l-4 border-l-[#0D47A1]">
                  <h4 className="font-serif text-base font-semibold mb-3 text-[#212121]">Asia-Pacific Growth</h4>
                  <p className="text-sm leading-relaxed text-[#616161] m-0">
                    {topAPAC.length > 0
                      ? `${topAPAC.map(c => `${c.name} (${c.cables})`).join(', ')} anchor the Asia-Pacific network, reflecting the region's strategic role in global digital infrastructure.`
                      : 'Asia-Pacific cable infrastructure data loading...'}
                  </p>
                </div>
              </div>
            )
          })()}
        </div>
      </section>
    </div>
  )
}

export default GeographicDistribution