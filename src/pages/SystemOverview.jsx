import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { supabase } from '../lib/supabase'
import CableExplorer from '../components/CableExplorer'

function SystemOverview() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [explorerFilter, setExplorerFilter] = useState(null)
  const [searchParams] = useSearchParams()

  // Deep link support: /overview?supplier=Chinese or ?owner=Western.
  // Deriving the filter during render (rather than in an effect) is the
  // pattern React recommends for reacting to a changing input.
  const paramFilter = searchParams.get('supplier')
    ? { supplierBloc: searchParams.get('supplier') }
    : searchParams.get('owner')
      ? { ownerBloc: searchParams.get('owner') }
      : null
  const paramKey = searchParams.toString()
  const [prevParamKey, setPrevParamKey] = useState(null)
  if (paramFilter && paramKey !== prevParamKey) {
    setPrevParamKey(paramKey)
    setExplorerFilter(paramFilter)
  }

  // Scrolling to the explorer is a genuine DOM side effect, so it stays in an effect.
  useEffect(() => {
    const hasParam = searchParams.get('supplier') || searchParams.get('owner')
    if (!hasParam) return
    const t = setTimeout(() => {
      document.getElementById('cable-explorer')?.scrollIntoView({ behavior: 'smooth' })
    }, 400)
    return () => clearTimeout(t)
  }, [searchParams])

  useEffect(() => {
    async function loadCables() {
      const { data: cables, error } = await supabase
        .from('submarinecables')
        .select('*')
      if (error) {
        console.error('Supabase error:', error)
        setLoading(false)
        return
      }
      setData(cables)
      setLoading(false)
    }
    loadCables()
  }, [])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <div className="w-10 h-10 border-4 border-gray-200 border-t-[#0D47A1] rounded-full animate-spin mb-4"></div>
        <p className="text-[#616161]">Loading submarine cable data...</p>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
        <p className="text-red-600">No data found. Check console for details.</p>
      </div>
    )
  }

  // ── Bloc counts ───────────────────────────────────────────────────────────
  const blocCounts = data.reduce((acc, cable) => {
    const bloc = cable.supplier_bloc || 'Unknown'
    acc[bloc] = (acc[bloc] || 0) + 1
    return acc
  }, {})

  const ownerBlocCounts = data.reduce((acc, cable) => {
    const bloc = cable.owner_bloc || 'Unknown'
    acc[bloc] = (acc[bloc] || 0) + 1
    return acc
  }, {})

  const activeCables = data.filter(c => c.status === 'In service').length
  const chineseCables = data.filter(c => c.chinese_supplier === 1 || c.chinese_supplier === '1').length
  const westernCount = blocCounts['Western'] || 0
  const unknownOwnerPct = (((ownerBlocCounts['Unknown'] || 0) / data.length) * 100).toFixed(1)

  // ── Supplier HHI — split on semicolons to count individual suppliers ───────
  const supplierNameCounts = {}
  data.forEach(cable => {
    const raw = cable.suppliers || 'Unknown'
    raw.split(';').map(s => s.trim()).filter(Boolean).forEach(supplier => {
      supplierNameCounts[supplier] = (supplierNameCounts[supplier] || 0) + 1
    })
  })
  const totalSupplierEntries = Object.values(supplierNameCounts).reduce((a, b) => a + b, 0)
  const supplierHHI = Math.round(
    Object.values(supplierNameCounts).reduce((sum, count) => {
      const share = (count / totalSupplierEntries) * 100
      return sum + share * share
    }, 0)
  )

  // ── Owner HHI — split on semicolons to count individual owners ────────────
  const ownerNameCounts = {}
  data.forEach(cable => {
    const raw = cable.owners || 'Unknown'
    raw.split(';').map(o => o.trim()).filter(Boolean).forEach(owner => {
      ownerNameCounts[owner] = (ownerNameCounts[owner] || 0) + 1
    })
  })
  // Owner HHI at bloc level — more meaningful for geopolitical analysis
const ownerHHI = Math.round(
  Object.values(ownerBlocCounts).reduce((sum, count) => {
    const share = (count / data.length) * 100
    return sum + share * share
  }, 0)
  )

  // ── HHI concentration label ───────────────────────────────────────────────
  const hhiLabel = (hhi) =>
    hhi > 2500 ? 'Highly concentrated (>2500)' :
    hhi > 1500 ? 'Moderately concentrated' :
    'Competitive (<1500)'

  // ── Render bar ────────────────────────────────────────────────────────────
  const renderBar = (bloc, count, total, dimension) => {
    const pct = parseFloat(((count / total) * 100).toFixed(1))
    const label = `${pct.toFixed(1)}%`
    const isNarrow = pct < 12
    return (
      <div
        key={bloc}
        role="button"
        tabIndex={0}
        title={`Show the ${count} cables with a ${bloc} ${dimension}`}
        onClick={() => {
          setExplorerFilter(
            dimension === 'supplier' ? { supplierBloc: bloc } : { ownerBloc: bloc }
          )
          document.getElementById('cable-explorer')?.scrollIntoView({ behavior: 'smooth' })
        }}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault()
            setExplorerFilter(
              dimension === 'supplier' ? { supplierBloc: bloc } : { ownerBloc: bloc }
            )
            document.getElementById('cable-explorer')?.scrollIntoView({ behavior: 'smooth' })
          }
        }}
        className="flex items-center gap-4 cursor-pointer rounded px-2 -mx-2 py-1 hover:bg-[#F4F8FE] transition-colors"
      >
        <div className="min-w-[100px] text-sm font-medium text-[#212121]">{bloc}</div>
        <div className="flex-1 bg-[#E0E0E0] rounded h-9 relative">
          <div
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-[#0D47A1] to-[#0097A7] rounded transition-all duration-300"
            style={{ width: `${pct}%` }}
          />
          {isNarrow ? (
            <span
              className="absolute top-0 h-full flex items-center text-xs font-semibold text-[#212121] whitespace-nowrap"
              style={{ left: `calc(${pct}% + 8px)` }}
            >
              {label}
            </span>
          ) : (
            <span
              className="absolute top-0 h-full flex items-center text-xs font-semibold text-white"
              style={{ left: `calc(${pct}% - 8px)`, transform: 'translateX(-100%)' }}
            >
              {label}
            </span>
          )}
        </div>
        <div className="min-w-[90px] text-right text-sm text-[#616161] font-medium">{count} cables</div>
      </div>
    )
  }

  const statCards = [
    { value: data.length,                                                              label: 'Total Cables',      sub: '↑ Infrastructure count' },
    { value: supplierHHI.toLocaleString(),                                             label: 'Supplier HHI',      sub: hhiLabel(supplierHHI) },
    { value: `${((chineseCables / data.length) * 100).toFixed(1)}%`,                  label: 'Chinese Suppliers', sub: `${chineseCables} cables` },
    { value: activeCables,                                                             label: 'Active Cables',     sub: `${((activeCables / data.length) * 100).toFixed(1)}% operational` },
  ]

  return (
    <div>
      {/* Page Header */}
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">System Overview</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Global structural summary of submarine cable infrastructure.
          Showing {data.length} cables across {Object.keys(blocCounts).length} geopolitical blocs.
        </p>
      </div>

      {/* Key Metrics */}
      <section className="mb-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {statCards.map((card, i) => (
            <div
              key={i}
              className="rounded-lg p-6 flex flex-col gap-1 border border-[#E8EDF5]"
              style={{ backgroundColor: '#F0F4FA' }}
            >
              <div className="font-serif text-4xl font-bold leading-tight" style={{ color: '#0A2F6B' }}>
                {card.value}
              </div>
              <div className="text-xs font-bold uppercase tracking-widest mt-2 text-[#616161]">
                {card.label}
              </div>
              <div className="text-xs mt-0.5 text-[#9E9E9E]">
                {card.sub}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Key Findings */}
      <section className="mb-10">
        <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Key Findings</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
            <h3 className="text-base font-semibold mb-3 text-[#212121]">Market Concentration</h3>
            <p className="text-sm leading-relaxed text-[#616161] m-0">
              Both supplier (HHI: {supplierHHI.toLocaleString()}) and owner (HHI: {ownerHHI.toLocaleString()}) markets are highly concentrated (&gt;2500), indicating limited competition.
            </p>
          </div>
          <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
            <h3 className="text-base font-semibold mb-3 text-[#212121]">Chinese Participation</h3>
            <p className="text-sm leading-relaxed text-[#616161] m-0">
              Chinese suppliers involved in {chineseCables} cables ({((chineseCables / data.length) * 100).toFixed(1)}%), representing a 20x increase from pre-2013 levels.
            </p>
          </div>
          <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
            <h3 className="text-base font-semibold mb-3 text-[#212121]">Western Dominance</h3>
            <p className="text-sm leading-relaxed text-[#616161] m-0">
              Western suppliers build {((westernCount / data.length) * 100).toFixed(1)}% of cables ({westernCount} total), led by SubCom, ASN, and NEC.
            </p>
          </div>
          <div className="p-6 bg-white rounded-lg border border-[#E0E0E0] border-l-4 border-l-[#212121] shadow-sm">
            <h3 className="text-base font-semibold mb-3 text-[#212121]">Data Coverage</h3>
            <p className="text-sm leading-relaxed text-[#616161] m-0">
              {blocCounts['Unknown'] || 0} cables ({(((blocCounts['Unknown'] || 0) / data.length) * 100).toFixed(1)}%) have unknown suppliers. Owner data has {(100 - parseFloat(unknownOwnerPct)).toFixed(1)}% coverage.
            </p>
          </div>
        </div>
      </section>

      {/* Supplier Market Share */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Supplier Market Share by Bloc</h2>
          <p className="text-sm text-[#616161] mb-6">
            Distribution of cable manufacturers across geopolitical blocs.
            Supplier data provides clearer bloc-level patterns than ownership (which is highly fragmented).
          </p>
          <div className="space-y-4 mb-8">
            {Object.entries(blocCounts)
              .sort(([,a], [,b]) => b - a)
              .map(([bloc, count]) => renderBar(bloc, count, data.length, 'supplier'))}
          </div>
          <div className="border-t border-[#E0E0E0] pt-6">
            <p className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-3">How blocs are defined</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-2">
              {[
                { bloc: 'Western', desc: 'Cables built by US, European, or Japanese manufacturers' },
                { bloc: 'Chinese', desc: 'Cables built by Chinese-owned or state-affiliated manufacturers' },
                { bloc: 'Mixed',   desc: 'Cables with both Chinese and Western manufacturers' },
                { bloc: 'Other',   desc: 'Cables built by manufacturers outside these blocs' },
                { bloc: 'Unknown', desc: 'Supplier information not publicly available' },
              ].map(({ bloc, desc }) => (
                <div key={bloc} className="flex items-start gap-2">
                  <span className="mt-1 text-[#9E9E9E] text-xs">—</span>
                  <span className="text-xs text-[#616161]">
                    <span className="font-semibold text-[#212121]">{bloc}:</span> {desc}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Owner Market Share */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Ownership Structure by Bloc</h2>
          <p className="text-sm text-[#616161] mb-6">
            Distribution of cable ownership across geopolitical blocs.
          </p>
          <div className="space-y-4 mb-8">
            {Object.entries(ownerBlocCounts)
              .sort(([,a], [,b]) => b - a)
              .map(([bloc, count]) => renderBar(bloc, count, data.length, 'owner'))}
          </div>
          <div className="border-t border-[#E0E0E0] pt-6">
            <p className="text-xs font-semibold uppercase tracking-wider text-[#9E9E9E] mb-3">How blocs are defined</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-2">
              {[
                { bloc: 'Western', desc: 'Cables owned by entities based in the US, Europe, Japan, or Australia' },
                { bloc: 'Chinese', desc: 'Cables owned by Chinese state or private entities' },
                { bloc: 'Mixed',   desc: 'Cables with ownership shared across Chinese and Western entities' },
                { bloc: 'Other',   desc: 'Cables owned by entities in the Global South or regional telecoms' },
                { bloc: 'Unknown', desc: 'Ownership information not publicly available' },
              ].map(({ bloc, desc }) => (
                <div key={bloc} className="flex items-start gap-2">
                  <span className="mt-1 text-[#9E9E9E] text-xs">—</span>
                  <span className="text-xs text-[#616161]">
                    <span className="font-semibold text-[#212121]">{bloc}:</span> {desc}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Market Concentration Indicators */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Market Concentration Indicators</h2>
          <p className="text-sm text-[#616161] mb-6">Key indices measuring market structure and competition</p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">Supplier HHI</h3>
              <div className="font-serif text-5xl font-bold text-[#C62828] my-4">{supplierHHI.toLocaleString()}</div>
              <p className="text-sm text-[#616161]">{hhiLabel(supplierHHI)}</p>
            </div>
            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">Owner HHI</h3>
              <div className="font-serif text-5xl font-bold text-[#C62828] my-4">{ownerHHI.toLocaleString()}</div>
              <p className="text-sm text-[#616161]">Bloc-level concentration</p>
            </div>
            <div className="text-center p-6">
              <h3 className="text-sm text-[#616161] uppercase font-semibold tracking-wide mb-2">Growth Rate</h3>
              <div className="font-serif text-5xl font-bold text-[#C62828] my-4">20x</div>
              <p className="text-sm text-[#616161]">Chinese supplier participation (Pre/Post 2013)</p>
            </div>
          </div>
        </div>
      </section>

      {/* Explore the cables (interactive) */}
      <section className="mb-10" id="cable-explorer">
        <CableExplorer cables={data} externalFilter={explorerFilter} />
      </section>

    </div>
  )
}

export default SystemOverview