import { useState, useEffect } from 'react'

function TemporalDynamics({ infrastructureType = 'cables' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState([1989, 2028])

  useEffect(() => {
    fetch('/data/temporal_dynamics.json')
      .then(r => r.json())
      .then(data => {
        setData(data)
        setTimeRange([data.year_range.min, data.year_range.max])
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading data:', err)
        setLoading(false)
      })
  }, [infrastructureType])

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p className="loading-text">Loading temporal analysis...</p>
      </div>
    )
  }

  if (!data) return <div className="card">Error loading data</div>

  // Filter data by time range
  const filteredData = data.cables_per_year.filter(d => 
    d.year >= timeRange[0] && d.year <= timeRange[1]
  )

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Temporal Dynamics</h1>
        <p className="page-description">
          Time-series analysis of cable deployment patterns, market share evolution, 
          and structural changes from {data.year_range.min} to {data.year_range.max}.
        </p>
      </div>

      {/* Time Range Filter */}
      <div className="card">
        <h3 style={{ fontSize: '0.875rem', fontWeight: 600, marginBottom: '1rem', textTransform: 'uppercase', color: '#666' }}>
          Time Period Filter
        </h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: '0.75rem', color: '#666', display: 'block', marginBottom: '0.5rem' }}>
              Start Year
            </label>
            <select
              value={timeRange[0]}
              onChange={(e) => setTimeRange([parseInt(e.target.value), timeRange[1]])}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '0.95rem',
                backgroundColor: 'white',
                cursor: 'pointer'
              }}
            >
              {Array.from({ length: data.year_range.max - data.year_range.min + 1 }, (_, i) => data.year_range.min + i).map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>

          <div style={{ fontSize: '0.875rem', color: '#999', paddingTop: '1.5rem' }}>to</div>

          <div style={{ flex: 1 }}>
            <label style={{ fontSize: '0.75rem', color: '#666', display: 'block', marginBottom: '0.5rem' }}>
              End Year
            </label>
            <select
              value={timeRange[1]}
              onChange={(e) => setTimeRange([timeRange[0], parseInt(e.target.value)])}
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '0.95rem',
                backgroundColor: 'white',
                cursor: 'pointer'
              }}
            >
              {Array.from({ length: data.year_range.max - data.year_range.min + 1 }, (_, i) => data.year_range.min + i).map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>

          <button
            onClick={() => setTimeRange([data.year_range.min, data.year_range.max])}
            style={{
              padding: '0.75rem 1.5rem',
              marginTop: '1.5rem',
              backgroundColor: '#f5f5f5',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontSize: '0.875rem',
              cursor: 'pointer',
              fontWeight: 500,
              color: '#666'
            }}
          >
            Reset
          </button>
        </div>
      </div>

      {/* Pre-2013 vs Post-2013 Comparison */}
      <section className="section">
        <div className="card">
          <h2 className="card-title">Pre-2013 vs Post-2013 Comparison</h2>
          <p className="card-description">
            Structural shifts in the submarine cable market before and after 2013
          </p>

          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '2rem',
            marginTop: '2rem'
          }}>
            {/* Pre-2013 */}
            <div>
              <h3 style={{ 
                fontSize: '1.25rem', 
                fontWeight: 600, 
                marginBottom: '1rem',
                color: '#666'
              }}>
                Pre-2013 (1989-2012)
              </h3>

              <div style={{ marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1a1a1a' }}>
                  {data.comparison_2013.pre_2013.total}
                </div>
                <div style={{ fontSize: '0.875rem', color: '#666' }}>
                  Total cables deployed
                </div>
                <div style={{ fontSize: '0.8rem', color: '#999', marginTop: '0.25rem' }}>
                  ~{data.comparison_2013.pre_2013.avg_per_year.toFixed(1)} cables/year
                </div>
              </div>

              <div className="bar-chart">
                {Object.entries(data.comparison_2013.pre_2013.blocs)
                  .filter(([bloc]) => bloc !== 'Unknown')
                  .sort(([,a], [,b]) => b - a)
                  .slice(0, 5)
                  .map(([bloc, count]) => {
                    const pct = ((count / data.comparison_2013.pre_2013.total) * 100).toFixed(1)
                    return (
                      <div key={bloc} style={{ marginBottom: '0.75rem' }}>
                        <div style={{ fontSize: '0.8rem', marginBottom: '0.25rem', display: 'flex', justifyContent: 'space-between' }}>
                          <span>{bloc}</span>
                          <span style={{ fontWeight: 600 }}>{pct}%</span>
                        </div>
                        <div style={{ height: '8px', backgroundColor: '#e0e0e0', borderRadius: '4px' }}>
                          <div style={{ 
                            height: '100%', 
                            width: `${pct}%`, 
                            backgroundColor: '#9e9e9e',
                            borderRadius: '4px'
                          }}></div>
                        </div>
                      </div>
                    )
                  })}
              </div>
            </div>

            {/* Post-2013 */}
            <div>
              <h3 style={{ 
                fontSize: '1.25rem', 
                fontWeight: 600, 
                marginBottom: '1rem',
                color: '#2196f3'
              }}>
                Post-2013 (2013-2025)
              </h3>

              <div style={{ marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1a1a1a' }}>
                  {data.comparison_2013.post_2013.total}
                </div>
                <div style={{ fontSize: '0.875rem', color: '#666' }}>
                  Total cables deployed
                </div>
                <div style={{ fontSize: '0.8rem', color: '#999', marginTop: '0.25rem' }}>
                  ~{data.comparison_2013.post_2013.avg_per_year.toFixed(1)} cables/year
                </div>
              </div>

              <div className="bar-chart">
                {Object.entries(data.comparison_2013.post_2013.blocs)
                  .filter(([bloc]) => bloc !== 'Unknown')
                  .sort(([,a], [,b]) => b - a)
                  .slice(0, 5)
                  .map(([bloc, count]) => {
                    const pct = ((count / data.comparison_2013.post_2013.total) * 100).toFixed(1)
                    return (
                      <div key={bloc} style={{ marginBottom: '0.75rem' }}>
                        <div style={{ fontSize: '0.8rem', marginBottom: '0.25rem', display: 'flex', justifyContent: 'space-between' }}>
                          <span>{bloc}</span>
                          <span style={{ fontWeight: 600 }}>{pct}%</span>
                        </div>
                        <div style={{ height: '8px', backgroundColor: '#e0e0e0', borderRadius: '4px' }}>
                          <div style={{ 
                            height: '100%', 
                            width: `${pct}%`, 
                            backgroundColor: '#2196f3',
                            borderRadius: '4px'
                          }}></div>
                        </div>
                      </div>
                    )
                  })}
              </div>
            </div>
          </div>

          {/* Key Changes */}
          <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#f0f7ff', borderRadius: '4px' }}>
            <h4 style={{ margin: '0 0 0.75rem 0', fontSize: '0.875rem', fontWeight: 600 }}>
              Key Structural Changes Post-2013:
            </h4>
            <ul style={{ margin: 0, paddingLeft: '1.5rem', fontSize: '0.875rem', lineHeight: 1.8 }}>
              <li>
                <strong>Chinese market entry:</strong> Increased from 0.4% to 8.5% of market share (20x growth)
              </li>
              <li>
                <strong>Deployment rate:</strong> Average cables per year increased from {data.comparison_2013.pre_2013.avg_per_year.toFixed(1)} 
                to {data.comparison_2013.post_2013.avg_per_year.toFixed(1)}
              </li>
              <li>
                <strong>Market diversification:</strong> More blocs actively participating in cable deployment
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Status Breakdown */}
      <section className="section">
        <div className="card">
          <h2 className="card-title">Cable Status Distribution</h2>
          <p className="card-description">
            Breakdown of operational vs planned submarine cables
          </p>

          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1.5rem',
            marginTop: '1.5rem'
          }}>
            {Object.entries(data.status_breakdown).map(([status, count]) => (
              <div key={status} style={{ textAlign: 'center', padding: '1.5rem' }}>
                <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#1a1a1a' }}>
                  {count}
                </div>
                <div style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem' }}>
                  {status}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Cables Per Year Chart Placeholder */}
      <section className="section">
        <div className="card">
          <h2 className="card-title">Annual Cable Deployments by Bloc</h2>
          <p className="card-description">
            Stacked area chart showing cables deployed each year (filtered by selected time range)
          </p>

          <div style={{ 
            height: '350px', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            backgroundColor: '#f9f9f9',
            borderRadius: '4px',
            border: '2px dashed #ddd',
            margin: '1rem 0'
          }}>
            <div style={{ textAlign: 'center', color: '#999' }}>
              <p style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                📊 D3.js Stacked Area Chart Coming Soon
              </p>
              <p style={{ fontSize: '0.75rem' }}>
                Will show {filteredData.length} years of deployment data
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default TemporalDynamics
