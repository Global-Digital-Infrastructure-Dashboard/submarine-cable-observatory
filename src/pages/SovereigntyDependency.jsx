import { useState, useEffect } from 'react'

function SovereigntyDependency({ infrastructureType = 'cables' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [sortBy, setSortBy] = useState('sovereignty_index')
  const [sortOrder, setSortOrder] = useState('desc')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetch('/data/sovereignty_dependency.json')
      .then(r => r.json())
      .then(data => {
        setData(data)
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
        <p className="loading-text">Loading sovereignty analysis...</p>
      </div>
    )
  }

  if (!data) return <div className="card">Error loading data</div>

  // Filter and sort countries
  let countries = data.countries.filter(c => 
    c.country.toLowerCase().includes(searchTerm.toLowerCase())
  )

  countries = countries.sort((a, b) => {
    const aVal = a[sortBy]
    const bVal = b[sortBy]
    return sortOrder === 'desc' ? bVal - aVal : aVal - bVal
  })

  // Get top/bottom countries
  const mostSovereign = countries.slice(0, 10)
  const mostVulnerable = countries.filter(c => c.total_cables >= 5).slice(-10).reverse()

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Sovereignty & Dependency</h1>
        <p className="page-description">
          Country-level infrastructure dependency analysis and Cable Sovereignty Index rankings. 
          Analyzing {data.countries.length} countries across {data.global_stats.total_countries} jurisdictions.
        </p>
      </div>

      {/* Global Statistics */}
      <section className="section">
        <div className="metrics-grid">
          <div className="metric-card metric-card-blue">
            <div className="metric-value">{data.global_stats.total_countries}</div>
            <div className="metric-label">Countries Analyzed</div>
          </div>

          <div className="metric-card metric-card-purple">
            <div className="metric-value">{data.global_stats.avg_sovereignty_index.toFixed(3)}</div>
            <div className="metric-label">Avg Sovereignty Index</div>
            <div className="metric-change">Global average</div>
          </div>

          <div className="metric-card metric-card-green">
            <div className="metric-value">{data.global_stats.avg_diversification.toFixed(3)}</div>
            <div className="metric-label">Avg Supplier Diversification</div>
            <div className="metric-change">Higher = more diverse</div>
          </div>

          <div className="metric-card metric-card-orange">
            <div className="metric-value">
              {countries.filter(c => c.single_supplier_dominance === 1).length}
            </div>
            <div className="metric-label">Single-Supplier Dependent</div>
            <div className="metric-change">Countries with &gt;50% from one bloc</div>
          </div>
        </div>
      </section>

      {/* Top/Bottom Rankings */}
      <section className="section">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
          {/* Most Sovereign */}
          <div className="card">
            <h2 className="card-title">Most Sovereign Countries</h2>
            <p className="card-description">
              Highest Cable Sovereignty Index scores (weighted: diversification, independence, redundancy)
            </p>

            <div style={{ marginTop: '1rem' }}>
              {mostSovereign.map((country, index) => (
                <div key={country.country} style={{ 
                  padding: '0.875rem',
                  borderBottom: '1px solid #eee',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem'
                }}>
                  <div style={{ 
                    fontSize: '1.25rem', 
                    fontWeight: 'bold',
                    color: index < 3 ? '#4caf50' : '#999',
                    width: '30px'
                  }}>
                    {index + 1}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>
                      {country.country}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#666' }}>
                      {country.total_cables} cables, {country.distinct_suppliers} suppliers
                    </div>
                  </div>
                  <div style={{ 
                    fontSize: '1.1rem', 
                    fontWeight: 'bold',
                    color: '#4caf50'
                  }}>
                    {country.sovereignty_index.toFixed(3)}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Most Vulnerable */}
          <div className="card">
            <h2 className="card-title">Most Vulnerable Countries</h2>
            <p className="card-description">
              Lowest sovereignty scores among countries with 5+ cables
            </p>

            <div style={{ marginTop: '1rem' }}>
              {mostVulnerable.map((country, index) => (
                <div key={country.country} style={{ 
                  padding: '0.875rem',
                  borderBottom: '1px solid #eee',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem'
                }}>
                  <div style={{ 
                    fontSize: '1.25rem', 
                    fontWeight: 'bold',
                    color: index < 3 ? '#e74c3c' : '#999',
                    width: '30px'
                  }}>
                    ⚠️
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>
                      {country.country}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#666' }}>
                      {country.total_cables} cables, {country.distinct_suppliers} suppliers
                    </div>
                  </div>
                  <div style={{ 
                    fontSize: '1.1rem', 
                    fontWeight: 'bold',
                    color: '#e74c3c'
                  }}>
                    {country.sovereignty_index.toFixed(3)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Full Country Ranking Table */}
      <section className="section">
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <div>
              <h2 className="card-title" style={{ marginBottom: '0.25rem' }}>
                Complete Country Rankings
              </h2>
              <p className="card-description" style={{ marginBottom: 0 }}>
                Sortable table of all countries with sovereignty metrics
              </p>
            </div>

            <input
              type="text"
              placeholder="Search countries..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                padding: '0.5rem 1rem',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '0.875rem',
                width: '250px'
              }}
            />
          </div>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th style={{ cursor: 'pointer' }} onClick={() => {
                    setSortBy('country')
                    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
                  }}>
                    Country {sortBy === 'country' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th style={{ cursor: 'pointer' }} onClick={() => {
                    setSortBy('total_cables')
                    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
                  }}>
                    Cables {sortBy === 'total_cables' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th style={{ cursor: 'pointer' }} onClick={() => {
                    setSortBy('sovereignty_index')
                    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
                  }}>
                    Sov. Index {sortBy === 'sovereignty_index' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                  <th>CN%</th>
                  <th>US%</th>
                  <th>EU%</th>
                  <th style={{ cursor: 'pointer' }} onClick={() => {
                    setSortBy('supplier_diversification')
                    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
                  }}>
                    Div. {sortBy === 'supplier_diversification' && (sortOrder === 'asc' ? '↑' : '↓')}
                  </th>
                </tr>
              </thead>
              <tbody>
                {countries.slice(0, 50).map((country) => (
                  <tr key={country.country}>
                    <td style={{ fontWeight: 600 }}>{country.country}</td>
                    <td>{country.total_cables}</td>
                    <td>
                      <span style={{
                        padding: '0.25rem 0.5rem',
                        borderRadius: '4px',
                        fontWeight: 600,
                        fontSize: '0.85rem',
                        backgroundColor: country.sovereignty_index > 0.7 ? '#e8f5e9' :
                                       country.sovereignty_index > 0.5 ? '#fff3e0' : '#ffebee',
                        color: country.sovereignty_index > 0.7 ? '#2e7d32' :
                               country.sovereignty_index > 0.5 ? '#f57c00' : '#c62828'
                      }}>
                        {country.sovereignty_index.toFixed(3)}
                      </span>
                    </td>
                    <td>{country.pct_chinese_supplier.toFixed(1)}%</td>
                    <td>{country.pct_us_supplier.toFixed(1)}%</td>
                    <td>{country.pct_eu_supplier.toFixed(1)}%</td>
                    <td>{country.supplier_diversification.toFixed(3)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {countries.length > 50 && (
            <div style={{ marginTop: '1rem', textAlign: 'center', color: '#666', fontSize: '0.875rem' }}>
              Showing top 50 of {countries.length} countries
            </div>
          )}
        </div>
      </section>

      {/* Methodology Note */}
      <section className="section">
        <div className="card">
          <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1rem' }}>
            About the Cable Sovereignty Index
          </h3>
          <p style={{ fontSize: '0.875rem', lineHeight: 1.6, color: '#666' }}>
            The Cable Sovereignty Index is a composite measure (0-1 scale) combining:
          </p>
          <ul style={{ fontSize: '0.875rem', lineHeight: 1.8, color: '#666', marginTop: '0.5rem' }}>
            <li><strong>Supplier Diversification (40%)</strong>: Based on 1-HHI of supplier blocs</li>
            <li><strong>Foreign Ownership Independence (30%)</strong>: Lower foreign ownership increases sovereignty</li>
            <li><strong>No Single-Supplier Dominance (20%)</strong>: No single bloc controls &gt;50% of cables</li>
            <li><strong>Route Redundancy (10%)</strong>: Number of distinct supplier blocs (normalized)</li>
          </ul>
          <p style={{ fontSize: '0.875rem', lineHeight: 1.6, color: '#666', marginTop: '1rem' }}>
            <strong>Interpretation:</strong> Higher scores indicate greater infrastructure sovereignty. 
            Countries with scores &lt;0.3 may be vulnerable to supply chain disruptions or political leverage.
          </p>
        </div>
      </section>
    </div>
  )
}

export default SovereigntyDependency