import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom'
import Auth from './Auth'
import InfrastructureSelector from './components/InfrastructureSelector'
import './App.css'
import './components/InfrastructureSelector.css'

// Page components
import SystemOverview from './pages/SystemOverview'
import MarketStructure from './pages/MarketStructure'
import GeographicDistribution from './pages/GeographicDistribution'
import SovereigntyDependency from './pages/SovereigntyDependency'
import TemporalDynamics from './pages/TemporalDynamics'
import PolicyRegulation from './pages/PolicyRegulation'
import Methodology from './pages/Methodology'

// Navigation items matching the 7 modules
const navItems = [
  { path: '/', label: 'System Overview' },
  { path: '/market-structure', label: 'Market Structure' },
  { path: '/geographic', label: 'Geographic Distribution' },
  { path: '/sovereignty', label: 'Sovereignty & Dependency' },
  { path: '/temporal', label: 'Temporal Dynamics' },
  { path: '/policy', label: 'Policy & Regulation' },
  { path: '/methodology', label: 'Methodology' },
]

function App() {
  const [infrastructureType, setInfrastructureType] = useState('cables')
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Check if already authenticated
  useEffect(() => {
    const auth = sessionStorage.getItem('authenticated')
    if (auth === 'true') {
      setIsAuthenticated(true)
    }
  }, [])

  const handleAuthenticate = () => {
    setIsAuthenticated(true)
  }

  // Show auth page if not authenticated
  if (!isAuthenticated) {
    return <Auth onAuthenticate={handleAuthenticate} />
  }

  return (
    <Router>
      <div className="app">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <h1 className="title">Global Digital Infrastructure Political Economy Observatory</h1>
            <p className="subtitle">Phase 1: Submarine Cable Analysis</p>
            <div className="meta-info">
              <span>Data Version: 1.0</span>
              <span className="separator">|</span>
              <span>Updated: February 2026</span>
            </div>
          </div>
        </header>

        {/* Navigation Tabs */}
        <nav className="navigation">
          <div className="nav-content">
            {navItems.map(item => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => 
                  isActive ? 'nav-link nav-link-active' : 'nav-link'
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
        </nav>

        {/* Main Content Area */}
        <main className="main">
          {/* Infrastructure Type Selector */}
          <InfrastructureSelector 
            selected={infrastructureType}
            onSelect={setInfrastructureType}
          />

          {/* Routes */}
          <Routes>
            <Route path="/" element={<SystemOverview infrastructureType={infrastructureType} />} />
            <Route path="/market-structure" element={<MarketStructure infrastructureType={infrastructureType} />} />
            <Route path="/geographic" element={<GeographicDistribution infrastructureType={infrastructureType} />} />
            <Route path="/sovereignty" element={<SovereigntyDependency infrastructureType={infrastructureType} />} />
            <Route path="/temporal" element={<TemporalDynamics infrastructureType={infrastructureType} />} />
            <Route path="/policy" element={<PolicyRegulation infrastructureType={infrastructureType} />} />
            <Route path="/methodology" element={<Methodology infrastructureType={infrastructureType} />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="footer">
          <div className="footer-content">
            <div className="footer-section">
              <h3>About This Project</h3>
              <p>
                A political economy research instrument for analyzing global digital 
                infrastructure patterns, geopolitical dependencies, and market structures 
                across multiple infrastructure types.
              </p>
            </div>
            
            <div className="footer-section">
              <h3>Data Sources</h3>
              <ul>
                <li>TeleGeography Submarine Cable Database</li>
                <li>PriMetrica Infrastructure Dataset</li>
                <li>Public filings and press releases</li>
              </ul>
            </div>
            
            <div className="footer-section">
              <h3>Citation</h3>
              <p>
                Global Digital Infrastructure Political Economy Observatory. (2026). 
                Submarine Cable Analysis Dashboard. Version 1.0.
              </p>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>© 2026 Digital Infrastructure Observatory. Research use only.</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App