import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

function TemporalDynamics({ infrastructureType = 'cables' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState([1989, 2028])

  useEffect(() => {
    async function loadData() {
      const { data: temporal, error } = await supabase
        .from('temporal_dynamics')
        .select('*')
        .order('year', { ascending: true })
      
      if (error) {
        console.error('Error:', error)
        setLoading(false)
        return
      }
  
      // Rebuild data structure
      const cables_per_year = temporal.map(t => ({
        year: t.year,
        total: t.total_cables,
        China: t.china_count,
        Europe: t.europe_count,
        US: t.us_count,
        Japan: t.japan_count,
        India: t.india_count,
        Mixed: t.mixed_count,
        Other: t.other_count,
        Unknown: t.unknown_count
      }))
  
      const pre2013 = temporal.filter(t => t.year < 2013)
      const post2013 = temporal.filter(t => t.year >= 2013)
  
      setData({
        cables_per_year: cables_per_year,
        year_range: { min: temporal[0].year, max: temporal[temporal.length - 1].year },
        comparison_2013: {
          pre_2013: {
            total: pre2013.reduce((sum, t) => sum + t.total_cables, 0),
            avg_per_year: pre2013.reduce((sum, t) => sum + t.total_cables, 0) / pre2013.length,
            blocs: {
              China: pre2013.reduce((sum, t) => sum + t.china_count, 0),
              Europe: pre2013.reduce((sum, t) => sum + t.europe_count, 0),
              US: pre2013.reduce((sum, t) => sum + t.us_count, 0),
              Japan: pre2013.reduce((sum, t) => sum + t.japan_count, 0)
            }
          },
          post_2013: {
            total: post2013.reduce((sum, t) => sum + t.total_cables, 0),
            avg_per_year: post2013.reduce((sum, t) => sum + t.total_cables, 0) / post2013.length,
            blocs: {
              China: post2013.reduce((sum, t) => sum + t.china_count, 0),
              Europe: post2013.reduce((sum, t) => sum + t.europe_count, 0),
              US: post2013.reduce((sum, t) => sum + t.us_count, 0),
              Japan: post2013.reduce((sum, t) => sum + t.japan_count, 0)
            }
          }
        },
        status_breakdown: { 'In service': 398, 'Planned': 55 } // You can calculate this from cables table
      })
      setTimeRange([temporal[0].year, temporal[temporal.length - 1].year])
      setLoading(false)
    }
    
    loadData()
  }, [infrastructureType])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <div className="w-10 h-10 border-4 border-gray-200 border-t-[#0D47A1] rounded-full animate-spin mb-4"></div>
        <p className="text-[#616161]">Loading temporal analysis...</p>
      </div>
    )
  }

  if (!data) return (
    <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
      Error loading data
    </div>
  )

  const filteredData = data.cables_per_year.filter(d => 
    d.year >= timeRange[0] && d.year <= timeRange[1]
  )

  const totalInRange = filteredData.reduce((sum, d) => sum + d.total, 0)
  const blocTotals = filteredData.reduce((acc, d) => {
    Object.keys(d).forEach(key => {
      if (key !== 'year' && key !== 'total' && key !== 'Unknown') {
        acc[key] = (acc[key] || 0) + (d[key] || 0)
      }
    })
    return acc
  }, {})

  return (
    <div>
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Temporal Dynamics</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Time-series analysis from {data.year_range.min} to {data.year_range.max}. 
          Currently showing {timeRange[0]}-{timeRange[1]}.
        </p>
      </div>

      {/* Time Filter */}
      <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6 mb-10">
        <h3 className="text-sm font-semibold mb-4 uppercase text-[#616161]">
          Time Period Filter
        </h3>
        <div className="flex items-center gap-6 flex-wrap">
          <div className="flex-1 min-w-[200px]">
            <label className="text-xs text-[#616161] block mb-2">Start Year</label>
            <select
              value={timeRange[0]}
              onChange={(e) => setTimeRange([parseInt(e.target.value), timeRange[1]])}
              className="w-full px-3 py-3 border border-[#E0E0E0] rounded text-base bg-white cursor-pointer"
            >
              {Array.from({ length: timeRange[1] - data.year_range.min + 1 }, (_, i) => data.year_range.min + i).map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>

          <div className="text-sm text-[#9E9E9E] pt-6">to</div>

          <div className="flex-1 min-w-[200px]">
            <label className="text-xs text-[#616161] block mb-2">End Year</label>
            <select
              value={timeRange[1]}
              onChange={(e) => setTimeRange([timeRange[0], parseInt(e.target.value)])}
              className="w-full px-3 py-3 border border-[#E0E0E0] rounded text-base bg-white cursor-pointer"
            >
              {Array.from({ length: data.year_range.max - timeRange[0] + 1 }, (_, i) => timeRange[0] + i).map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>

          <button
            onClick={() => setTimeRange([data.year_range.min, data.year_range.max])}
            className="px-6 py-3 mt-6 bg-[#2196F3] text-white rounded text-sm cursor-pointer font-medium hover:bg-[#1976D2] transition-colors"
          >
            Reset
          </button>
        </div>

        <div className="mt-4 p-3 bg-[#F0F7FF] rounded text-sm text-[#1565C0]">
          <strong>Filtered range:</strong> {totalInRange} cables deployed between {timeRange[0]}-{timeRange[1]}
        </div>
      </div>

      {/* Period Summary */}
      <section className="mb-10">
        <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Selected Period Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{totalInRange}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">Total Cables</div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#C62828] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{(blocTotals['China'] || 0)}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide mb-2">Chinese Suppliers</div>
            <div className="text-xs text-[#9E9E9E]">
              {totalInRange > 0 ? ((blocTotals['China'] || 0) / totalInRange * 100).toFixed(1) : 0}%
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#6A1B9A] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{(blocTotals['Europe'] || 0)}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide mb-2">European Suppliers</div>
            <div className="text-xs text-[#9E9E9E]">
              {totalInRange > 0 ? ((blocTotals['Europe'] || 0) / totalInRange * 100).toFixed(1) : 0}%
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#2E7D32] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">
              {filteredData.length > 0 ? (totalInRange / filteredData.length).toFixed(1) : 0}
            </div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">Avg/Year</div>
          </div>
        </div>
      </section>

      {/* Pre/Post 2013 Comparison */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Pre-2013 vs Post-2013</h2>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Pre-2013 */}
            <div className="p-6 bg-[#FAFAFA] rounded-lg border-2 border-[#9E9E9E]">
              <h3 className="text-lg font-semibold mb-4 text-[#616161]">Pre-2013</h3>

              <div className="mb-6 text-center">
                <div className="text-5xl font-bold font-serif text-[#212121]">{data.comparison_2013.pre_2013.total}</div>
                <div className="text-sm text-[#616161] mt-1">
                  ~{data.comparison_2013.pre_2013.avg_per_year.toFixed(1)}/year
                </div>
              </div>

              <div className="space-y-3">
                {Object.entries(data.comparison_2013.pre_2013.blocs)
                  .filter(([bloc]) => bloc !== 'Unknown')
                  .sort(([,a], [,b]) => b - a)
                  .slice(0, 4)
                  .map(([bloc, count]) => {
                    const pct = ((count / data.comparison_2013.pre_2013.total) * 100).toFixed(1)
                    return (
                      <div key={bloc}>
                        <div className="text-sm mb-1.5 flex justify-between font-medium">
                          <span>{bloc}</span>
                          <span>{pct}%</span>
                        </div>
                        <div className="h-2.5 bg-[#E0E0E0] rounded overflow-hidden">
                          <div className="h-full bg-[#757575] rounded transition-all duration-300" style={{ width: `${pct}%` }}></div>
                        </div>
                      </div>
                    )
                  })}
              </div>
            </div>

            {/* Post-2013 */}
            <div className="p-6 bg-[#E3F2FD] rounded-lg border-2 border-[#2196F3]">
              <h3 className="text-lg font-semibold mb-4 text-[#1976D2]">Post-2013</h3>

              <div className="mb-6 text-center">
                <div className="text-5xl font-bold font-serif text-[#212121]">{data.comparison_2013.post_2013.total}</div>
                <div className="text-sm text-[#616161] mt-1">
                  ~{data.comparison_2013.post_2013.avg_per_year.toFixed(1)}/year
                </div>
              </div>

              <div className="space-y-3">
                {Object.entries(data.comparison_2013.post_2013.blocs)
                  .filter(([bloc]) => bloc !== 'Unknown')
                  .sort(([,a], [,b]) => b - a)
                  .slice(0, 4)
                  .map(([bloc, count]) => {
                    const pct = ((count / data.comparison_2013.post_2013.total) * 100).toFixed(1)
                    return (
                      <div key={bloc}>
                        <div className="text-sm mb-1.5 flex justify-between font-medium">
                          <span>{bloc}</span>
                          <span>{pct}%</span>
                        </div>
                        <div className="h-2.5 bg-[#E0E0E0] rounded overflow-hidden">
                          <div className="h-full bg-[#1976D2] rounded transition-all duration-300" style={{ width: `${pct}%` }}></div>
                        </div>
                      </div>
                    )
                  })}
              </div>
            </div>
          </div>

          {/* Key Insights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-8">
            <div className="p-6 bg-[#FFEBEE] rounded-lg border-l-4 border-[#E74C3C]">
              <h4 className="text-base font-semibold mb-3 text-[#C62828]">Chinese Market Entry</h4>
              <p className="text-sm leading-relaxed text-[#212121] m-0">
                From 0.4% to 8.5% — 20x growth
              </p>
            </div>

            <div className="p-6 bg-[#E8F5E9] rounded-lg border-l-4 border-[#4CAF50]">
              <h4 className="text-base font-semibold mb-3 text-[#2E7D32]">Deployment Acceleration</h4>
              <p className="text-sm leading-relaxed text-[#212121] m-0">
                {data.comparison_2013.pre_2013.avg_per_year.toFixed(1)} → {data.comparison_2013.post_2013.avg_per_year.toFixed(1)} cables/year
              </p>
            </div>

            <div className="p-6 bg-[#F3E5F5] rounded-lg border-l-4 border-[#9C27B0]">
              <h4 className="text-base font-semibold mb-3 text-[#6A1B9A]">Market Diversification</h4>
              <p className="text-sm leading-relaxed text-[#212121] m-0">
                More blocs actively deploying
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Deployment by Bloc */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">
            Deployment by Bloc ({timeRange[0]}-{timeRange[1]})
          </h2>

          <div className="space-y-4">
            {Object.entries(blocTotals)
              .sort(([,a], [,b]) => b - a)
              .map(([bloc, count]) => {
                const pct = totalInRange > 0 ? ((count / totalInRange) * 100).toFixed(1) : 0
                return (
                  <div key={bloc}>
                    <div className="text-sm mb-1.5 flex justify-between font-medium">
                      <span>{bloc}</span>
                      <span className="text-[#616161]">{count} cables ({pct}%)</span>
                    </div>
                    <div className="h-7 bg-[#E0E0E0] rounded overflow-hidden">
                      <div 
                        className="h-full bg-[#2196F3] rounded flex items-center pl-3 transition-all duration-300"
                        style={{ width: `${pct}%` }}
                      >
                        {parseFloat(pct) > 5 && (
                          <span className="text-xs text-white font-semibold">{pct}%</span>
                        )}
                      </div>
                    </div>
                  </div>
                )
              })}
          </div>
        </div>
      </section>

      {/* Status Breakdown */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Status Breakdown</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {Object.entries(data.status_breakdown).map(([status, count]) => (
              <div 
                key={status} 
                className={`p-8 rounded-lg border-2 text-center ${
                  status === 'In service' 
                    ? 'bg-[#E8F5E9] border-[#4CAF50]' 
                    : 'bg-[#FFF3E0] border-[#FF9800]'
                }`}
              >
                <div className="font-serif text-5xl font-bold text-[#212121]">{count}</div>
                <div className="text-base text-[#616161] mt-2 font-semibold">{status}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default TemporalDynamics