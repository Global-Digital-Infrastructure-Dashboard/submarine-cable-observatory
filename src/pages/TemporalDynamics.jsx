import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

function TemporalDynamics({ infrastructureType = 'cables' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState([1989, 2028])

  useEffect(() => {
    async function loadData() {
      // Load temporal data
      const { data: temporal, error: temporalError } = await supabase
        .from('temporal_dynamics')
        .select('*')
        .order('year', { ascending: true })

      if (temporalError) {
        console.error('Error:', temporalError)
        setLoading(false)
        return
      }

      // Load status breakdown live from cables table
      const { data: cables, error: cablesError } = await supabase
        .from('submarinecables')
        .select('status')

      if (cablesError) {
        console.error('Cables error:', cablesError)
      }

      const statusBreakdown = cables
        ? cables.reduce((acc, c) => {
            const s = c.status || 'Unknown'
            acc[s] = (acc[s] || 0) + 1
            return acc
          }, {})
        : {}

      const cables_per_year = temporal.map(t => ({
        year:    t.year,
        total:   t.total_cables,
        Chinese: t.china_count,
        Western: t.western_count,
        Other:   t.other_count,
        Unknown: t.unknown_count,
      }))

      const pre2013  = temporal.filter(t => t.year < 2013)
      const post2013 = temporal.filter(t => t.year >= 2013)

      setData({
        cables_per_year,
        year_range: { min: temporal[0].year, max: temporal[temporal.length - 1].year },
        comparison_2013: {
          pre_2013: {
            total: pre2013.reduce((sum, t) => sum + t.total_cables, 0),
            avg_per_year: pre2013.reduce((sum, t) => sum + t.total_cables, 0) / pre2013.length,
            blocs: {
              Chinese: pre2013.reduce((sum, t) => sum + t.china_count,   0),
              Western: pre2013.reduce((sum, t) => sum + t.western_count, 0),
              Other:   pre2013.reduce((sum, t) => sum + t.other_count,   0),
            }
          },
          post_2013: {
            total: post2013.reduce((sum, t) => sum + t.total_cables, 0),
            avg_per_year: post2013.reduce((sum, t) => sum + t.total_cables, 0) / post2013.length,
            blocs: {
              Chinese: post2013.reduce((sum, t) => sum + t.china_count,   0),
              Western: post2013.reduce((sum, t) => sum + t.western_count, 0),
              Other:   post2013.reduce((sum, t) => sum + t.other_count,   0),
            }
          }
        },
        status_breakdown: statusBreakdown
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

  // Chinese market entry % pre vs post
  const preTotal = data.comparison_2013.pre_2013.total
  const postTotal = data.comparison_2013.post_2013.total
  const preChinaPct = preTotal > 0
    ? ((data.comparison_2013.pre_2013.blocs.Chinese / preTotal) * 100).toFixed(1)
    : '0.0'
  const postChinaPct = postTotal > 0
    ? ((data.comparison_2013.post_2013.blocs.Chinese / postTotal) * 100).toFixed(1)
    : '0.0'

  return (
    <div>
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Temporal Dynamics</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Time-series analysis from {data.year_range.min} to {data.year_range.max}.
          Currently showing {timeRange[0]}–{timeRange[1]}.
        </p>
      </div>

      {/* Time Filter */}
      <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6 mb-10">
        <h3 className="text-sm font-semibold mb-4 uppercase text-[#616161]">Time Period Filter</h3>
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
            className="px-6 py-3 mt-6 bg-[#0D47A1] text-white rounded text-sm cursor-pointer font-medium hover:bg-[#0A2F6B] transition-colors"
          >
            Reset
          </button>
        </div>

        <div className="mt-4 p-3 bg-[#F0F4FA] rounded text-sm text-[#0D47A1]">
          <strong>Filtered range:</strong> {totalInRange} cables deployed between {timeRange[0]}–{timeRange[1]}
        </div>
      </div>

      {/* Period Summary */}
      <section className="mb-10">
        <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Selected Period Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#0A2F6B] mb-2">{totalInRange}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">Total Cables</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#0A2F6B] mb-2">{blocTotals['Chinese'] || 0}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide mb-2">Chinese Suppliers</div>
            <div className="text-xs text-[#9E9E9E]">
              {totalInRange > 0 ? (((blocTotals['Chinese'] || 0) / totalInRange) * 100).toFixed(1) : 0}%
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#0A2F6B] mb-2">{blocTotals['Western'] || 0}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide mb-2">Western Suppliers</div>
            <div className="text-xs text-[#9E9E9E]">
              {totalInRange > 0 ? (((blocTotals['Western'] || 0) / totalInRange) * 100).toFixed(1) : 0}%
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#0A2F6B] mb-2">
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
            <div className="p-6 bg-[#F0F4FA] rounded-lg border border-[#E8EDF5] border-l-4 border-l-[#0D47A1]">
              <h3 className="text-lg font-semibold mb-4 text-[#212121]">Pre-2013</h3>
              <div className="mb-6 text-center">
                <div className="text-5xl font-bold font-serif text-[#212121]">{data.comparison_2013.pre_2013.total}</div>
                <div className="text-sm text-[#616161] mt-1">~{data.comparison_2013.pre_2013.avg_per_year.toFixed(1)}/year</div>
              </div>
              <div className="space-y-3">
                {Object.entries(data.comparison_2013.pre_2013.blocs)
                  .sort(([,a], [,b]) => b - a)
                  .slice(0, 4)
                  .map(([bloc, count]) => {
                    const pct = ((count / data.comparison_2013.pre_2013.total) * 100).toFixed(1)
                    return (
                      <div key={bloc}>
                        <div className="text-sm mb-1.5 flex justify-between font-medium">
                          <span>{bloc}</span><span>{pct}%</span>
                        </div>
                        <div className="h-2.5 bg-[#E0E0E0] rounded overflow-hidden">
                          <div className="h-full bg-gradient-to-r from-[#0D47A1] to-[#0097A7] rounded transition-all duration-300" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    )
                  })}
              </div>
            </div>

            <div className="p-6 bg-[#F0F4FA] rounded-lg border border-[#E8EDF5] border-l-4 border-l-[#0D47A1]">
              <h3 className="text-lg font-semibold mb-4 text-[#212121]">Post-2013</h3>
              <div className="mb-6 text-center">
                <div className="text-5xl font-bold font-serif text-[#212121]">{data.comparison_2013.post_2013.total}</div>
                <div className="text-sm text-[#616161] mt-1">~{data.comparison_2013.post_2013.avg_per_year.toFixed(1)}/year</div>
              </div>
              <div className="space-y-3">
                {Object.entries(data.comparison_2013.post_2013.blocs)
                  .sort(([,a], [,b]) => b - a)
                  .slice(0, 4)
                  .map(([bloc, count]) => {
                    const pct = ((count / data.comparison_2013.post_2013.total) * 100).toFixed(1)
                    return (
                      <div key={bloc}>
                        <div className="text-sm mb-1.5 flex justify-between font-medium">
                          <span>{bloc}</span><span>{pct}%</span>
                        </div>
                        <div className="h-2.5 bg-[#E0E0E0] rounded overflow-hidden">
                          <div className="h-full bg-gradient-to-r from-[#0D47A1] to-[#0097A7] rounded transition-all duration-300" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    )
                  })}
              </div>
            </div>
          </div>

          {/* Key Insights — inline stat row, no more cards */}
          <div className="mt-8 pt-6 border-t border-[#E0E0E0] grid grid-cols-3 divide-x divide-[#E0E0E0]">
            <div className="px-6 first:pl-0">
              <div className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-1">Chinese Market Entry</div>
              <div className="font-serif text-2xl font-bold text-[#212121]">{preChinaPct}% → {postChinaPct}%</div>
              <div className="text-xs text-[#9E9E9E] mt-1">supplier share pre vs post 2013</div>
            </div>
            <div className="px-6">
              <div className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-1">Deployment Rate</div>
              <div className="font-serif text-2xl font-bold text-[#212121]">{data.comparison_2013.pre_2013.avg_per_year.toFixed(1)} → {data.comparison_2013.post_2013.avg_per_year.toFixed(1)}</div>
              <div className="text-xs text-[#9E9E9E] mt-1">cables/year average</div>
            </div>
            <div className="px-6">
              <div className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-1">Growth Factor</div>
              <div className="font-serif text-2xl font-bold text-[#212121]">
                {preChinaPct > 0 ? (postChinaPct / preChinaPct).toFixed(1) : '20'}×
              </div>
              <div className="text-xs text-[#9E9E9E] mt-1">increase in Chinese participation</div>
            </div>
          </div>
        </div>
      </section>

      {/* Deployment by Bloc — uniform teal bars */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">
            Deployment by Bloc ({timeRange[0]}–{timeRange[1]})
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
                        className="h-full bg-gradient-to-r from-[#0D47A1] to-[#0097A7] rounded flex items-center pl-3 transition-all duration-300"
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

      {/* Status Breakdown — inline stat row */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Status Breakdown</h2>
          <div className={`grid divide-x divide-[#E0E0E0]`} style={{ gridTemplateColumns: `repeat(${Object.keys(data.status_breakdown).length}, 1fr)` }}>
            {Object.entries(data.status_breakdown)
              .sort(([,a], [,b]) => b - a)
              .map(([status, count], i) => (
                <div key={status} className="px-6 first:pl-0 last:pr-0">
                  <div className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-1">{status}</div>
                  <div className="font-serif text-3xl font-bold text-[#212121]">{count}</div>
                  <div className="text-xs text-[#9E9E9E] mt-1">{((count / Object.values(data.status_breakdown).reduce((a,b) => a+b, 0)) * 100).toFixed(1)}% of total</div>
                </div>
              ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default TemporalDynamics