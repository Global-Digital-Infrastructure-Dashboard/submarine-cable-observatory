import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'

function PolicyRegulation({ infrastructureType = 'cables' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [filterJurisdiction, setFilterJurisdiction] = useState('all')
  const [timeFilter, setTimeFilter] = useState('all')
  const [search, setSearch] = useState('')

  useEffect(() => {
    async function loadPolicyData() {
      const { data: events, error } = await supabase
        .from('policy_events')
        .select('*')
        .order('event_date', { ascending: false })
      
      if (error) {
        console.error('Error loading policy events:', error)
        setLoading(false)
        return
      }

      // Group by jurisdiction
      const byJurisdiction = events.reduce((acc, e) => {
        acc[e.jurisdiction] = (acc[e.jurisdiction] || 0) + 1
        return acc
      }, {})

      setData({
        policy_events: events,
        total_events: events.length,
        by_jurisdiction: byJurisdiction
      })
      setLoading(false)
    }
    
    loadPolicyData()
  }, [infrastructureType])

  if (loading) return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="w-10 h-10 border-4 border-gray-200 border-t-[#0D47A1] rounded-full animate-spin mb-4"></div>
    </div>
  )
  
  if (!data || !data.policy_events) return (
    <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
      <p>Data not available</p>
    </div>
  )

  let events = data.policy_events

  if (filterJurisdiction !== 'all') {
    events = events.filter(e => e.jurisdiction === filterJurisdiction)
  }

  const q = search.trim().toLowerCase()
  if (q) {
    events = events.filter(e =>
      [e.policy_name, e.key_change, e.impact_on_cables, e.jurisdiction, e.affected_regions]
        .some(f => String(f ?? '').toLowerCase().includes(q))
    )
  }

  if (timeFilter === 'recent') {
    events = events.filter(e => e.year >= 2024)
  } else if (timeFilter === 'historical') {
    events = events.filter(e => e.year < 2024)
  }

  const recentEvents = data.policy_events.filter(e => e.year >= 2024).length

  // Built from the data, so every jurisdiction present is reachable.
  const jurisdictionCounts = data.policy_events.reduce((acc, e) => {
    const j = e.jurisdiction || 'Unspecified'
    acc[j] = (acc[j] || 0) + 1
    return acc
  }, {})
  const jurisdictions = ['all', ...Object.keys(jurisdictionCounts).sort(
    (a, b) => jurisdictionCounts[b] - jurisdictionCounts[a]
  )]

  return (
    <div>
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Policy & Regulation</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Comprehensive policy timeline (1884-2026) - {data.total_events} regulatory events
        </p>
      </div>

      {/* Metrics */}
      <section className="mb-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#0D47A1] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{data.total_events}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">Total Events</div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#C62828] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{data.by_jurisdiction.US || 0}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">US Actions</div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#6A1B9A] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{data.by_jurisdiction.EU || 0}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">EU Policy</div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] border-l-4 border-l-[#2E7D32] p-7 hover:-translate-y-0.5 hover:shadow-md transition-all">
            <div className="font-serif text-4xl font-bold text-[#212121] mb-2">{recentEvents}</div>
            <div className="text-sm text-[#616161] font-medium uppercase tracking-wide">Since 2024</div>
          </div>
        </div>
      </section>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6 mb-10">
        <div className="mb-6">
          <label className="text-xs font-semibold text-[#616161] uppercase block mb-3">
            Search:
          </label>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search policy name, change, or region"
            className="w-full max-w-xl border border-[#E0E0E0] rounded-md px-3 py-2.5 text-sm text-[#212121] focus:outline-none focus:ring-2 focus:ring-[#6A1B9A]/30"
          />
        </div>

        <div className="mb-6">
          <label className="text-xs font-semibold text-[#616161] uppercase block mb-3">
            Time Period:
          </label>
          <div className="flex gap-3 flex-wrap">
            {[
              { value: 'all', label: `All Time (${data.total_events})` },
              { value: 'recent', label: `2024-Present (${recentEvents})` },
              { value: 'historical', label: `Before 2024 (${data.total_events - recentEvents})` }
            ].map(option => (
              <button
                key={option.value}
                onClick={() => setTimeFilter(option.value)}
                className={`px-5 py-3 rounded-md text-sm font-semibold transition-all ${
                  timeFilter === option.value 
                    ? 'bg-[#0D47A1] text-white' 
                    : 'bg-white text-[#616161] border border-[#E0E0E0] hover:border-[#0D47A1] hover:text-[#0D47A1]'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="text-xs font-semibold text-[#616161] uppercase block mb-3">
            Jurisdiction:
          </label>
          <div className="flex gap-3 flex-wrap">
            {jurisdictions.map(j => (
              <button
                key={j}
                onClick={() => setFilterJurisdiction(j)}
                className={`px-4 py-2.5 rounded-md text-sm font-semibold transition-all ${
                  filterJurisdiction === j 
                    ? 'bg-[#6A1B9A] text-white' 
                    : 'bg-white text-[#616161] border border-[#E0E0E0] hover:border-[#6A1B9A] hover:text-[#6A1B9A]'
                }`}
              >
                {j === 'all' ? 'All' : j}
                <span className="ml-1.5 opacity-60 font-normal">
                  {j === 'all' ? data.total_events : jurisdictionCounts[j]}
                </span>
              </button>
            ))}
          </div>
        </div>

        {(filterJurisdiction !== 'all' || timeFilter !== 'all' || search.trim() !== '') && (
          <div className="mt-4 p-3 bg-[#F0F7FF] rounded text-sm text-[#0D47A1]">
            Showing {events.length} of {data.total_events} events
            <button
              onClick={() => { setFilterJurisdiction('all'); setTimeFilter('all'); setSearch('') }}
              className="ml-3 underline font-semibold hover:no-underline"
            >
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* Timeline */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-8">Regulatory Timeline</h2>

          <div className="pl-12 relative">
            <div className="absolute left-5 top-0 bottom-0 w-0.5 bg-[#E0E0E0]" />

            {events.map((event) => {
              const colors = {
                'US': '#0D47A1',
                'EU': '#6A1B9A',
                'Australia': '#00695C',
                'India': '#E65100',
                'International': '#424242'
              }
              const color = colors[event.jurisdiction] || '#757575'
              
              return (
                <div key={event.id} className="mb-10 relative">
                  <div 
                    className="absolute -left-[1.85rem] top-2 w-4 h-4 rounded-full border-[3px] border-white shadow-[0_0_0_2px_#E0E0E0]"
                    style={{ backgroundColor: color }}
                  />

                  <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] shadow-sm">
                    <div className="mb-3">
                      <div className="flex items-center gap-3 mb-2">
                        <span 
                          className="text-[0.7rem] font-bold uppercase px-3 py-1 rounded"
                          style={{ 
                            color: color,
                            backgroundColor: color + '15'
                          }}
                        >
                          {event.jurisdiction}
                        </span>
                        <span className="text-sm text-[#757575] font-medium">
                          {event.event_date}
                        </span>
                      </div>
                      <h3 className="font-serif text-lg font-bold m-0 text-[#212121]">
                        {event.policy_name}
                      </h3>
                    </div>

                    <p className="text-base leading-relaxed text-[#616161] mb-4">
                      <strong>Change:</strong> {event.key_change}
                    </p>

                    <p className="text-sm leading-relaxed text-[#616161] mb-4 italic pl-4 border-l-[3px] border-[#E0E0E0]">
                      {event.impact_on_cables}
                    </p>

                    <div className="flex justify-between text-xs">
                      <span className="text-[#9E9E9E]">{event.affected_regions}</span>
                      {event.source_url && event.source_url !== 'N/A' && (
                        <a 
                          href={event.source_url} 
                          target="_blank" 
                          rel="noopener noreferrer" 
                          className="font-semibold no-underline hover:underline"
                          style={{ color: color }}
                        >
                          Source →
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </section>
    </div>
  )
}

export default PolicyRegulation