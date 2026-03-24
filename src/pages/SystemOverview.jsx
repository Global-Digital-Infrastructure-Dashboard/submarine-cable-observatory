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

  // Calculate metrics - USING SUPPLIER BLOCS
  const blocCounts = data.reduce((acc, cable) => {
    const bloc = cable.supplier_bloc
    acc[bloc] = (acc[bloc] || 0) + 1
    return acc
  }, {})

  const activeCables = data.filter(c => c.status === 'In service').length
  const chineseCables = data.filter(c => c.chinese_supplier === 1 || c.chinese_supplier === '1').length

  const supplierHHI = 3020
  const ownerHHI = 3780

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

      {/* Key Metrics */}
      <section className="mb-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-6 hover:shadow-md transition-shadow">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{data.length}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide mb-2">Total Cables</div>
            <div className="text-xs text-[#9E9E9E] flex items-center gap-1">
              <span className="text-green-600">↑</span> Infrastructure count
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#C62828] p-6 hover:shadow-md transition-shadow">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{supplierHHI.toLocaleString()}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide mb-2">Supplier HHI</div>
            <div className="text-xs text-[#9E9E9E]">High concentration</div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#6A1B9A] p-6 hover:shadow-md transition-shadow">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">
              {((chineseCables / data.length) * 100).toFixed(1)}%
            </div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide mb-2">Chinese Suppliers</div>
            <div className="text-xs text-[#9E9E9E]">{chineseCables} cables</div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#2E7D32] p-6 hover:shadow-md transition-shadow">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{activeCables}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide mb-2">Active Cables</div>
            <div className="text-xs text-[#9E9E9E]">
              {((activeCables / data.length) * 100).toFixed(1)}% operational
            </div>
          </div>
        </div>
      </section>

      {/* Key Findings */}
      <section className="mb-10">
        <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Key Findings</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="p-6 bg-[#FFF3E0] rounded-lg border-l-4 border-[#FF9800]">
            <h3 className="text-base font-semibold mb-3 text-[#E65100]">Market Concentration</h3>
            <p className="text-sm leading-relaxed text-[#212121] m-0">
              Both supplier (HHI: {supplierHHI}) and owner (HHI: {ownerHHI}) markets are highly concentrated (&gt;2500), indicating limited competition.
            </p>
          </div>

          <div className="p-6 bg-[#FFEBEE] rounded-lg border-l-4 border-[#E74C3C]">
            <h3 className="text-base font-semibold mb-3 text-[#C62828]">Chinese Participation</h3>
            <p className="text-sm leading-relaxed text-[#212121] m-0">
              Chinese suppliers involved in {chineseCables} cables ({((chineseCables / data.length) * 100).toFixed(1)}%), representing a 20x increase from pre-2013 levels.
            </p>
          </div>

          <div className="p-6 bg-[#F3E5F5] rounded-lg border-l-4 border-[#9C27B0]">
            <h3 className="text-base font-semibold mb-3 text-[#6A1B9A]">European Dominance</h3>
            <p className="text-sm leading-relaxed text-[#212121] m-0">
              Europe maintains the largest supplier market share at {((blocCounts['Europe'] / data.length) * 100).toFixed(1)}% of total cables.
            </p>
          </div>

          <div className="p-6 bg-[#E3F2FD] rounded-lg border-l-4 border-[#2196F3]">
            <h3 className="text-base font-semibold mb-3 text-[#1565C0]">Data Coverage</h3>
            <p className="text-sm leading-relaxed text-[#212121] m-0">
              {blocCounts['Unknown'] || 0} cables ({((blocCounts['Unknown'] / data.length) * 100).toFixed(1)}%) have unknown suppliers. Owner data has 97% coverage.
            </p>
          </div>
        </div>
      </section>

      {/* Market Share */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Supplier Market Share by Bloc</h2>
          <p className="text-sm text-[#616161] mb-6">
            Distribution of cable manufacturers across geopolitical blocs. 
            Supplier data provides clearer bloc-level patterns than ownership (which is highly fragmented).
          </p>

          <div className="space-y-4">
            {Object.entries(blocCounts)
              .filter(([bloc]) => bloc !== 'Unknown')
              .sort(([,a], [,b]) => b - a)
              .map(([bloc, count]) => {
                const percentage = ((count / data.length) * 100).toFixed(1)
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
      </section>

      {/* Concentration Indicators */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Market Concentration Indicators</h2>
          <p className="text-sm text-[#616161] mb-6">Key indices measuring market structure and competition</p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">
                Supplier HHI
              </h3>
              <div className="font-serif text-5xl font-bold text-[#212121] my-4">
                {supplierHHI.toLocaleString()}
              </div>
              <p className="text-sm text-[#616161]">
                Highly concentrated market (&gt;2500)
              </p>
            </div>

            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">
                Owner HHI
              </h3>
              <div className="font-serif text-5xl font-bold text-[#212121] my-4">
                {ownerHHI.toLocaleString()}
              </div>
              <p className="text-sm text-[#616161]">
                Highly concentrated ownership (&gt;2500)
              </p>
            </div>

            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">
                Growth Rate
              </h3>
              <div className="font-serif text-5xl font-bold text-[#212121] my-4">20x</div>
              <p className="text-sm text-[#616161]">
                Chinese supplier participation (Pre/Post 2013)
              </p>
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
                  <th className="px-4 py-3.5 text-left text-xs uppercase text-[#616161] font-semibold tracking-wider">
                    Cable Name
                  </th>
                  <th className="px-4 py-3.5 text-left text-xs uppercase text-[#616161] font-semibold tracking-wider">
                    Year
                  </th>
                  <th className="px-4 py-3.5 text-left text-xs uppercase text-[#616161] font-semibold tracking-wider">
                    Owner Bloc
                  </th>
                  <th className="px-4 py-3.5 text-left text-xs uppercase text-[#616161] font-semibold tracking-wider">
                    Status
                  </th>
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
                          cable.owner_bloc?.toLowerCase() === 'china' ? 'bg-red-100 text-red-800' :
                          cable.owner_bloc?.toLowerCase() === 'us' ? 'bg-blue-100 text-blue-800' :
                          cable.owner_bloc?.toLowerCase() === 'europe' ? 'bg-purple-100 text-purple-800' :
                          cable.owner_bloc?.toLowerCase() === 'japan' ? 'bg-teal-100 text-teal-800' :
                          cable.owner_bloc?.toLowerCase() === 'india' ? 'bg-orange-100 text-orange-800' :
                          cable.owner_bloc?.toLowerCase() === 'mixed' ? 'bg-indigo-100 text-indigo-800' :
                          cable.owner_bloc?.toLowerCase() === 'other' ? 'bg-gray-100 text-gray-700' :
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