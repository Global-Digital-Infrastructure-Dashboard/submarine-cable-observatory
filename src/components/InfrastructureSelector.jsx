import { useState } from 'react'

const INFRASTRUCTURE_TYPES = [
  { 
    id: 'cables', 
    label: 'Submarine Cables', 
    available: true,
    description: 'Undersea fiber optic cable networks',
    dataVersion: 'V1.0 (453 cables)'
  },
  { 
    id: '5g', 
    label: '5G Networks', 
    available: false,
    description: 'Fifth-generation cellular networks',
    dataVersion: 'Coming soon'
  },
  { 
    id: 'cloud', 
    label: 'Cloud Infrastructure', 
    available: false,
    description: 'Data centers and cloud computing facilities',
    dataVersion: 'Coming soon'
  },
  { 
    id: 'ai', 
    label: 'AI Infrastructure', 
    available: false,
    description: 'AI training and deployment infrastructure',
    dataVersion: 'Coming soon'
  },
]

function InfrastructureSelector({ selected, onSelect }) {
  const [isOpen, setIsOpen] = useState(false)
  
  const selectedInfra = INFRASTRUCTURE_TYPES.find(i => i.id === selected)

  return (
    <div className="infrastructure-selector">
      <label className="selector-label">Infrastructure Type:</label>
      
      <div className="selector-wrapper">
        <button 
          className="selector-button"
          onClick={() => setIsOpen(!isOpen)}
        >
          <span className="selector-text">
            <span className="selector-title">{selectedInfra.label}</span>
            <span className="selector-version">{selectedInfra.dataVersion}</span>
          </span>
          <span className="selector-arrow">{isOpen ? '▲' : '▼'}</span>
        </button>

        {isOpen && (
          <div className="selector-dropdown">
            {INFRASTRUCTURE_TYPES.map(infra => (
              <button
                key={infra.id}
                className={`dropdown-item ${!infra.available ? 'dropdown-item-disabled' : ''} ${infra.id === selected ? 'dropdown-item-active' : ''}`}
                onClick={() => {
                  if (infra.available) {
                    onSelect(infra.id)
                    setIsOpen(false)
                  }
                }}
                disabled={!infra.available}
              >
                <div className="dropdown-item-content">
                  <div className="dropdown-item-header">
                    <span className="dropdown-item-label">{infra.label}</span>
                    {!infra.available && (
                      <span className="badge-coming-soon">Coming Soon</span>
                    )}
                  </div>
                  <div className="dropdown-item-description">{infra.description}</div>
                  <div className="dropdown-item-version">{infra.dataVersion}</div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Info banner about future infrastructure types */}
      <div className="infrastructure-info">
        <span className="info-icon">ℹ️</span>
        <span className="info-text">
          Future phases will add 5G, cloud, and AI infrastructure datasets using the same analytical framework
        </span>
      </div>
    </div>
  )
}

export default InfrastructureSelector