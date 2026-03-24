function Methodology() {
    const titles = {
      'MarketStructure': 'Market Structure',
      'GeographicDistribution': 'Geographic Distribution',
      'SovereigntyDependency': 'Sovereignty & Dependency',
      'TemporalDynamics': 'Temporal Dynamics',
      'PolicyRegulation': 'Policy & Regulation',
      'Methodology': 'Methodology & Data'
    }
    
    const descriptions = {
      'MarketStructure': 'Industrial organization perspective on supplier competition, ownership structure, and supplier-owner divergence.',
      'GeographicDistribution': 'Network mapping, regional clustering analysis, and cross-region connectivity patterns.',
      'SovereigntyDependency': 'Country-level infrastructure dependency analysis and Cable Sovereignty Index calculations.',
      'TemporalDynamics': 'Time-series analysis of cable deployment, market share evolution, and pre/post-2013 comparisons.',
      'PolicyRegulation': 'Policy event tracking, national security reviews, and infrastructure strategy initiatives.',
      'Methodology': 'Variable definitions, coding rules, index formulas, and data sources.'
    }
    
    return (
      <div>
        <div className="page-header">
          <h1 className="page-title">{titles['Methodology']}</h1>
          <p className="page-description">{descriptions['Methodology']}</p>
        </div>
  
        <div className="card">
          <div style={{ textAlign: 'center', padding: '3rem 0' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🚧</div>
            <h2 style={{ fontSize: '1.5rem', color: '#666', marginBottom: '0.5rem' }}>
              Coming Soon
            </h2>
            <p style={{ color: '#999' }}>
              This module is under development
            </p>
          </div>
        </div>
      </div>
    )
  }
  
  export default Methodology