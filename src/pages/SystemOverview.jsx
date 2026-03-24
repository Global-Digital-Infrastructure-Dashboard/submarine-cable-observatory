import { useState, useEffect } from 'react'

function SystemOverview() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/data/cables_data.json')
      .then(res => res.json())
      .then(data => {
        setData(data.cables)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading data:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <p className="loading-text">Loading submarine cable data...</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="card">
        <p style={{ color: 'red' }}>Error loading data. Check console for details.</p>
      </div>
    )
  }

  // Calculate metrics
  const blocCounts = data.reduce((acc, cable) => {
    const bloc = cable.supplier_bloc
    acc[bloc] = (acc[bloc] || 0) + 1
    return acc
  }, {})

  const activeCables = data.filter(c => c.status === 'In service').length
  const chineseCables = data.filter(c => c.chinese_supplier === 1).length
  const filteredBlocCounts = Object.entries(blocCounts).filter(([bloc]) => bloc !== 'Unknown')

  // Calculate HHI (placeholder - we'll compute this properly later)
  const supplierHHI = 3020
  const ownerHHI = 3780

  return (
    <div>
      {/* Page Header */}
      <div className="page-header">
        <h1 className="page-title">System Overview</h1>
        <p className="page-description">
          Global structural summary of submarine cable infrastructure. 
          Showing {data.length} cables across {Object.keys(blocCounts).length} geopolitical blocs.
        </p>
      </div>

      {/* Key Metrics Section */}
      <section className="section">
        <div className="metrics-grid">
          <div className="metric-card metric-card-blue">
            <div className="metric-value">{data.length}</div>
            <div className="metric-label">Total Cables</div>
            <div className="metric-change metric-change-positive">
              ↑ Infrastructure count
            </div>
          </div>

          <div className="metric-card metric-card-red">
            <div className="metric-value">{supplierHHI.toLocaleString()}</div>
            <div className="metric-label">Supplier HHI</div>
            <div className="metric-change">
              High concentration
            </div>
          </div>

          <div className="metric-card metric-card-purple">
            <div className="metric-value">{((chineseCables / data.length) * 100).toFixed(1)}%</div>
            <div className="metric-label">Chinese Suppliers</div>
            <div className="metric-change">
              {chineseCables} cables
            </div>
          </div>

          <div className="metric-card metric-card-green">
            <div className="metric-value">{activeCables}</div>
            <div className="metric-label">Active Cables</div>
            <div className="metric-change">
              {((activeCables / data.length) * 100).toFixed(1)}% operational
            </div>
          </div>
        </div>
      </section>

      {/* Market Share Section */}
      <section className="section">
        <div className="card">
          <h2 className="card-title">Supplier Market Share by Bloc</h2>
          <p className="card-description">
            Distribution of cable suppliers across geopolitical blocs 
            (excluding {blocCounts['Unknown'] || 0} cables with unknown suppliers)
          </p>

          <div className="bar-chart">
            {filteredBlocCounts
              .sort(([,a], [,b]) => b - a)
              .map(([bloc, count]) => {
                const percentage = ((count / data.length) * 100).toFixed(1)
                return (
                  <div key={bloc} className="bar-row">
                    <div className="bar-label">{bloc}</div>
                    <div className="bar-container">
                      <div className="bar-fill" style={{ width: `${percentage}%` }}>
                        <span className="bar-text">{percentage}%</span>
                      </div>
                    </div>
                    <div className="bar-count">{count} cables</div>
                  </div>
                )
              })}
          </div>
        </div>
      </section>

      {/* Additional Metrics Section */}
      <section className="section">
        <div className="card">
          <h2 className="card-title">Market Concentration Indicators</h2>
          <p className="card-description">
            Key indices measuring market structure and competition
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
            <div>
              <h3 style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem', textTransform: 'uppercase', fontWeight: 600 }}>
                Supplier HHI
              </h3>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1a1a1a' }}>
                {supplierHHI.toLocaleString()}
              </div>
              <p style={{ fontSize: '0.875rem', color: '#666', marginTop: '0.5rem' }}>
                Highly concentrated market (&gt;2500)
              </p>
            </div>

            <div>
              <h3 style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem', textTransform: 'uppercase', fontWeight: 600 }}>
                Owner HHI
              </h3>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1a1a1a' }}>
                {ownerHHI.toLocaleString()}
              </div>
              <p style={{ fontSize: '0.875rem', color: '#666', marginTop: '0.5rem' }}>
                Highly concentrated ownership (&gt;2500)
              </p>
            </div>

            <div>
              <h3 style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem', textTransform: 'uppercase', fontWeight: 600 }}>
                Growth Rate (Pre/Post 2013)
              </h3>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#1a1a1a' }}>
                20x
              </div>
              <p style={{ fontSize: '0.875rem', color: '#666', marginTop: '0.5rem' }}>
                Chinese supplier participation increased
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Recent Cables Table */}
      <section className="section">
        <div className="card">
          <h2 className="card-title">Recent Cables</h2>
          <p className="card-description">
            Most recent submarine cable deployments
          </p>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Cable Name</th>
                  <th>Year</th>
                  <th>Supplier Bloc</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {data
                  .slice()
                  .sort((a, b) => (b.rfs_year || 0) - (a.rfs_year || 0))
                  .slice(0, 10)
                  .map((cable, idx) => (
                    <tr key={idx}>
                      <td>{cable.cable_name}</td>
                      <td>{cable.rfs_year || 'N/A'}</td>
                      <td>
                        <span className={`badge badge-${cable.supplier_bloc?.toLowerCase() || 'unknown'}`}>
                          {cable.supplier_bloc || 'Unknown'}
                        </span>
                      </td>
                      <td>{cable.status}</td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Key Insights Section */}
      <section className="section">
        <div className="card">
          <h2 className="card-title">Key Findings</h2>
          <ul style={{ lineHeight: '1.8', color: '#333', paddingLeft: '1.5rem' }}>
            <li>
              <strong>Market Concentration:</strong> Both supplier (HHI: {supplierHHI}) and 
              owner (HHI: {ownerHHI}) markets are highly concentrated (&gt;2500), indicating 
              limited competition.
            </li>
            <li>
              <strong>Chinese Participation:</strong> Chinese suppliers involved in {chineseCables} cables 
              ({((chineseCables / data.length) * 100).toFixed(1)}%), representing a significant 
              increase from pre-2013 levels.
            </li>
            <li>
              <strong>European Dominance:</strong> Europe maintains the largest supplier market share 
              at {((blocCounts['Europe'] / data.length) * 100).toFixed(1)}% of total cables.
            </li>
            <li>
              <strong>Data Quality:</strong> {blocCounts['Unknown']} cables ({((blocCounts['Unknown'] / data.length) * 100).toFixed(1)}%) 
              have unknown suppliers, indicating need for additional data collection.
            </li>
          </ul>
        </div>
      </section>
    </div>
  )
}

export default SystemOverview