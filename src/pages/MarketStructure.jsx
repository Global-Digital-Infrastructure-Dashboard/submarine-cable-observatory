import { useState, useEffect } from 'react'

function MarketStructure({ infrastructureType = 'cables' }) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeSection, setActiveSection] = useState('supplier-competition')

  useEffect(() => {
    Promise.all([
      fetch('/data/market_structure.json').then(r => r.json()),
      fetch('/data/cables_data.json').then(r => r.json())
    ])
      .then(([marketData, cablesData]) => {
        setData({ ...marketData, totalCables: cablesData.total_cables })
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
        <p className="loading-text">Loading market structure data...</p>
      </div>
    )
  }

  if (!data) return <div className="card">Error loading data</div>

  const sections = [
    { id: 'supplier-competition', label: 'A. Supplier Competition' },
    { id: 'ownership-structure', label: 'B. Ownership Structure' },
    { id: 'supplier-owner-divergence', label: 'C. Supplier-Owner Divergence' }
  ]

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Market Structure</h1>
        <p className="page-description">
          Industrial organization perspective on supplier competition, ownership patterns, 
          and control dynamics in submarine cable infrastructure.
        </p>
      </div>

      {/* Section Selector */}
      <div className="card">
        <div className="section-tabs">
          {sections.map(section => (
            <button
              key={section.id}
              className={`section-tab ${activeSection === section.id ? 'section-tab-active' : ''}`}
              onClick={() => setActiveSection(section.id)}
            >
              {section.label}
            </button>
          ))}
        </div>
      </div>

      {/* A. Supplier Competition */}
      {activeSection === 'supplier-competition' && (
        <div className="section">
          <div className="card">
            <h2 className="card-title">Market Share by Supplier Bloc</h2>
            <p className="card-description">
              Current distribution of submarine cable suppliers across geopolitical blocs
            </p>

            <div className="bar-chart">
              {Object.entries(data.supplier_competition.market_share)
                .filter(([bloc]) => bloc !== 'Unknown')
                .sort(([,a], [,b]) => b - a)
                .map(([bloc, count]) => {
                  const percentage = ((count / data.totalCables) * 100).toFixed(1)
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

          <div className="card">
            <h2 className="card-title">Entry Timing by Bloc</h2>
            <p className="card-description">
              Timeline showing when each geopolitical bloc entered the submarine cable market
            </p>

            <div style={{ padding: '2rem 1rem' }}>
              {Object.entries(data.supplier_competition.entry_timing)
                .filter(([bloc]) => bloc !== 'Unknown')
                .sort(([,a], [,b]) => a - b)
                .map(([bloc, year], index) => (
                  <div key={bloc} style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    marginBottom: '1.5rem',
                    position: 'relative'
                  }}>
                    <div style={{ 
                      width: '80px', 
                      fontSize: '1.25rem', 
                      fontWeight: 'bold',
                      color: '#2196f3'
                    }}>
                      {Math.round(year)}
                    </div>
                    <div style={{ 
                      width: '4px', 
                      height: '60px', 
                      backgroundColor: '#2196f3',
                      margin: '0 1.5rem',
                      borderRadius: '2px'
                    }}></div>
                    <div>
                      <span className={`badge badge-${bloc.toLowerCase()}`}>{bloc}</span>
                      <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.25rem' }}>
                        First cable deployment
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      )}

      {/* B. Ownership Structure */}
      {activeSection === 'ownership-structure' && (
        <div className="section">
          <div className="card">
            <h2 className="card-title">Ownership Market Share by Bloc</h2>
            <p className="card-description">
              Distribution of cable ownership across geopolitical blocs
            </p>

            <div className="bar-chart">
              {Object.entries(data.ownership_structure.market_share)
                .filter(([bloc]) => bloc !== 'Unknown')
                .sort(([,a], [,b]) => b - a)
                .map(([bloc, count]) => {
                  const percentage = ((count / data.totalCables) * 100).toFixed(1)
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

          <div className="card">
            <h2 className="card-title">Ownership Concentration</h2>
            <div style={{ padding: '3rem 2rem', textAlign: 'center' }}>
              <div style={{ fontSize: '4rem', fontWeight: 'bold', color: '#e74c3c' }}>
                {data.ownership_structure.global_hhi.toLocaleString()}
              </div>
              <div style={{ fontSize: '1.25rem', color: '#666', marginTop: '1rem' }}>
                Owner HHI Score
              </div>
              <div style={{ 
                fontSize: '0.9rem', 
                color: '#999', 
                marginTop: '0.75rem',
                maxWidth: '500px',
                margin: '0.75rem auto 0'
              }}>
                Highly concentrated ownership market. Values &gt;2500 indicate limited competition.
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="card-title">Ownership Type Analysis</h2>
            <p className="card-description">
              State-owned vs private ownership patterns (data collection in progress)
            </p>
            <div style={{ padding: '2rem', textAlign: 'center', color: '#999' }}>
              <p>🚧 Ownership type classification requires additional data coding</p>
              <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                Coming in future update
              </p>
            </div>
          </div>
        </div>
      )}

      {/* C. Supplier-Owner Divergence */}
      {activeSection === 'supplier-owner-divergence' && (
        <div className="section">
          <div className="card">
            <h2 className="card-title">Supplier-Owner Control Patterns</h2>
            <p className="card-description">
              Analysis of alignment and divergence between cable suppliers and owners reveals 
              the complexity of infrastructure control beyond simple national affiliations.
            </p>

            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '1.5rem',
              marginTop: '2rem'
            }}>
              <div style={{ 
                padding: '2rem', 
                backgroundColor: '#fff3e0', 
                borderRadius: '8px',
                border: '2px solid #ff9800'
              }}>
                <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#f57c00' }}>
                  {data.supplier_owner_divergence.chinese_supplier_western_owner}
                </div>
                <div style={{ fontSize: '0.9rem', fontWeight: 600, marginTop: '0.5rem', color: '#333' }}>
                  Chinese Supplier + Western Owner
                </div>
                <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.5rem' }}>
                  Western entities own cables built by Chinese suppliers
                </div>
              </div>

              <div style={{ 
                padding: '2rem', 
                backgroundColor: '#e3f2fd', 
                borderRadius: '8px',
                border: '2px solid #2196f3'
              }}>
                <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#1976d2' }}>
                  {data.supplier_owner_divergence.western_supplier_chinese_owner}
                </div>
                <div style={{ fontSize: '0.9rem', fontWeight: 600, marginTop: '0.5rem', color: '#333' }}>
                  Western Supplier + Chinese Owner
                </div>
                <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.5rem' }}>
                  Chinese entities own cables built by Western suppliers
                </div>
              </div>

              <div style={{ 
                padding: '2rem', 
                backgroundColor: '#ffebee', 
                borderRadius: '8px',
                border: '2px solid #e74c3c'
              }}>
                <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#c62828' }}>
                  {data.supplier_owner_divergence.fully_chinese}
                </div>
                <div style={{ fontSize: '0.9rem', fontWeight: 600, marginTop: '0.5rem', color: '#333' }}>
                  Fully Chinese-Controlled
                </div>
                <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.5rem' }}>
                  Both supplier and owner are Chinese entities
                </div>
              </div>

              <div style={{ 
                padding: '2rem', 
                backgroundColor: '#f3e5f5', 
                borderRadius: '8px',
                border: '2px solid #9c27b0'
              }}>
                <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#7b1fa2' }}>
                  {data.supplier_owner_divergence.fully_western}
                </div>
                <div style={{ fontSize: '0.9rem', fontWeight: 600, marginTop: '0.5rem', color: '#333' }}>
                  Fully Western-Controlled
                </div>
                <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.5rem' }}>
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