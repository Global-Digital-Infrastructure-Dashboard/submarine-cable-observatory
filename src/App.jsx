import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, NavLink, useLocation } from 'react-router-dom'
//import Auth from './Auth'
import Hero from './components/Hero'
import InfrastructureSelector from './components/InfrastructureSelector'
import './components/InfrastructureSelector.css'

import About from './pages/About'
import SystemOverview from './pages/SystemOverview'
import MarketStructure from './pages/MarketStructure'
import GeographicDistribution from './pages/GeographicDistribution'
import SovereigntyDependency from './pages/SovereigntyDependency'
import TemporalDynamics from './pages/TemporalDynamics'
import PolicyRegulation from './pages/PolicyRegulation'
import Methodology from './pages/Methodology'

const navItems = [
  { path: '/', label: 'About' },
  { path: '/overview', label: 'System Overview' },
  { path: '/market-structure', label: 'Market Structure' },
  { path: '/geographic', label: 'Geographic Distribution' },
  { path: '/sovereignty', label: 'Sovereignty & Dependency' },
  { path: '/temporal', label: 'Temporal Dynamics' },
  { path: '/policy', label: 'Policy & Regulation' },
  { path: '/methodology', label: 'Methodology' },
]

function AppLayout() {
  const [infrastructureType, setInfrastructureType] = useState('cables')
  const location = useLocation()
  const isAboutPage = location.pathname === '/'

  return (
    <div className="min-h-screen flex flex-col bg-[#FAFAFA]">
      <Hero />

      {/* Navigation - matching original design exactly */}
      <nav className="bg-white">
        <div className="max-w-[1400px] mx-auto px-8 flex gap-2 overflow-x-auto">
          {navItems.map(item => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `px-5 py-4 text-sm font-medium whitespace-nowrap transition-all border-b-[3px] ${
                  isActive
                    ? 'text-[#0D47A1] border-b-[#0D47A1] font-semibold'
                    : 'text-[#616161] border-b-transparent hover:text-[#0D47A1] hover:bg-[#FAFAFA]'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 max-w-[1400px] mx-auto w-full px-8 py-8">
        {!isAboutPage && (
          <InfrastructureSelector
            selected={infrastructureType}
            onSelect={setInfrastructureType}
          />
        )}

        <Routes>
          <Route path="/" element={<About />} />
          <Route path="/overview" element={<SystemOverview infrastructureType={infrastructureType} />} />
          <Route path="/market-structure" element={<MarketStructure infrastructureType={infrastructureType} />} />
          <Route path="/geographic" element={<GeographicDistribution infrastructureType={infrastructureType} />} />
          <Route path="/sovereignty" element={<SovereigntyDependency infrastructureType={infrastructureType} />} />
          <Route path="/temporal" element={<TemporalDynamics infrastructureType={infrastructureType} />} />
          <Route path="/policy" element={<PolicyRegulation infrastructureType={infrastructureType} />} />
          <Route path="/methodology" element={<Methodology infrastructureType={infrastructureType} />} />
        </Routes>
      </main>

      {/* Footer - matching original design */}
      <footer className="bg-[#212121] text-white/70 mt-auto pt-12 pb-6 px-8 border-t border-[#424242]">
        <div className="max-w-[1400px] mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-[2fr_1fr_1fr] gap-12 mb-8">
            <div>
              <h3 className="font-serif text-base font-semibold mb-4 text-white">About This Project</h3>
              <p className="text-sm leading-relaxed">
                A research platform mapping who owns, builds, and supplies the physical infrastructure
                behind AI and the internet, starting with the world's submarine cables. Built by
                Professor Tsai and Professor Shen as part of their work on technology and politics at
                Northeastern University.
              </p>
            </div>
          </div>

          <div className="border-t border-[#424242] pt-6 text-center">
            <p className="text-xs text-white/50">
              © 2026 Digital Infrastructure Observatory | Northeastern University | Open source (MIT License)
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

function App() {
  return (
    <Router>
      <AppLayout />
    </Router>
  )
}

export default App