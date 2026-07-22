import { useState, useMemo } from 'react'

// Splits the semicolon-separated list fields used throughout the dataset.
const toList = (v) =>
  !v ? [] : String(v).split(';').map((s) => s.trim()).filter(Boolean)

const num = (v) => {
  const n = parseFloat(String(v ?? '').replace(/[^0-9.]/g, ''))
  return Number.isFinite(n) ? n : null
}

const PAGE_SIZE = 25

const BLOC_STYLES = {
  Western: 'bg-[#E8F0FB] text-[#0D47A1]',
  Chinese: 'bg-[#FDECEC] text-[#B3261E]',
  Mixed: 'bg-[#F3EAFB] text-[#6A3AB2]',
  Other: 'bg-[#EAF6EE] text-[#1E6B3A]',
  Unknown: 'bg-[#F0F0F0] text-[#757575]',
}

function Pill({ value }) {
  const cls = BLOC_STYLES[value] || BLOC_STYLES.Unknown
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${cls}`}>
      {value || 'Unknown'}
    </span>
  )
}

function Th({ label, sortable, sortKey, sortDir, k, onSort }) {
  return (
    <th className="text-left px-4 py-3 font-semibold text-[#616161]">
      {sortable ? (
        <button
          onClick={() => onSort(k)}
          className="inline-flex items-center gap-1 hover:text-[#0D47A1] transition-colors"
        >
          {label}
          <span className="text-[10px] text-[#0D47A1]">
            {sortKey === k ? (sortDir === 'asc' ? '\u25B2' : '\u25BC') : ''}
          </span>
        </button>
      ) : (
        label
      )}
    </th>
  )
}

function CableExplorer({ cables }) {
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('all')
  const [supplierBloc, setSupplierBloc] = useState('all')
  const [ownerBloc, setOwnerBloc] = useState('all')
  const [sortKey, setSortKey] = useState('cable_name')
  const [sortDir, setSortDir] = useState('asc')
  const [expanded, setExpanded] = useState(null)
  const [visible, setVisible] = useState(PAGE_SIZE)

  // Build filter dropdown options from the data itself, so they never go stale.
  const options = useMemo(() => {
    const uniq = (key) =>
      [...new Set(cables.map((c) => c[key]).filter(Boolean))].sort()
    return {
      status: uniq('status'),
      supplierBloc: uniq('supplier_bloc'),
      ownerBloc: uniq('owner_bloc'),
    }
  }, [cables])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    let rows = cables.filter((c) => {
      if (status !== 'all' && c.status !== status) return false
      if (supplierBloc !== 'all' && (c.supplier_bloc || 'Unknown') !== supplierBloc) return false
      if (ownerBloc !== 'all' && (c.owner_bloc || 'Unknown') !== ownerBloc) return false
      if (!q) return true
      return [c.cable_name, c.owners, c.suppliers, c.landing_countries, c.owner_country, c.suppliers_country]
        .some((f) => String(f ?? '').toLowerCase().includes(q))
    })

    rows = [...rows].sort((a, b) => {
      let av = a[sortKey]
      let bv = b[sortKey]
      if (sortKey === 'length_km' || sortKey === 'rfs_year') {
        const an = num(av)
        const bn = num(bv)
        if (an === null && bn === null) return 0
        if (an === null) return 1 // blanks always last
        if (bn === null) return -1
        return sortDir === 'asc' ? an - bn : bn - an
      }
      av = String(av ?? '').toLowerCase()
      bv = String(bv ?? '').toLowerCase()
      if (av === bv) return 0
      if (!av) return 1
      if (!bv) return -1
      return sortDir === 'asc' ? (av < bv ? -1 : 1) : (av < bv ? 1 : -1)
    })

    return rows
  }, [cables, query, status, supplierBloc, ownerBloc, sortKey, sortDir])

  const toggleSort = (key) => {
    if (sortKey === key) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortKey(key)
      setSortDir('asc')
    }
    setVisible(PAGE_SIZE)
  }

  const resetAll = () => {
    setQuery('')
    setStatus('all')
    setSupplierBloc('all')
    setOwnerBloc('all')
    setVisible(PAGE_SIZE)
  }

  const isFiltered =
    query.trim() !== '' || status !== 'all' || supplierBloc !== 'all' || ownerBloc !== 'all'

  const selectCls =
    'border border-[#E0E0E0] rounded-md px-3 py-2 text-sm text-[#212121] bg-white focus:outline-none focus:ring-2 focus:ring-[#0D47A1]/30'

  return (
    <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-6">
      <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Explore the cables</h2>
      <p className="text-[#616161] text-sm mb-5">
        Search and filter the full dataset. Select any cable to see its owners, suppliers, landing
        points, and source.
      </p>

      {/* Controls */}
      <div className="flex flex-wrap gap-3 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value)
            setVisible(PAGE_SIZE)
          }}
          placeholder="Search cable, owner, supplier, or country"
          className={`${selectCls} flex-1 min-w-[260px]`}
        />
        <select
          value={status}
          onChange={(e) => {
            setStatus(e.target.value)
            setVisible(PAGE_SIZE)
          }}
          className={selectCls}
        >
          <option value="all">All statuses</option>
          {options.status.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <select
          value={supplierBloc}
          onChange={(e) => {
            setSupplierBloc(e.target.value)
            setVisible(PAGE_SIZE)
          }}
          className={selectCls}
        >
          <option value="all">All supplier blocs</option>
          {options.supplierBloc.map((s) => (
            <option key={s} value={s}>{s} supplier</option>
          ))}
        </select>
        <select
          value={ownerBloc}
          onChange={(e) => {
            setOwnerBloc(e.target.value)
            setVisible(PAGE_SIZE)
          }}
          className={selectCls}
        >
          <option value="all">All owner blocs</option>
          {options.ownerBloc.map((s) => (
            <option key={s} value={s}>{s} owner</option>
          ))}
        </select>
      </div>

      <div className="flex items-center justify-between mb-3">
        <p className="text-sm text-[#616161]">
          Showing <span className="font-semibold text-[#212121]">{Math.min(visible, filtered.length)}</span>{' '}
          of <span className="font-semibold text-[#212121]">{filtered.length}</span> cables
          {isFiltered && <span className="text-[#9E9E9E]"> (filtered from {cables.length})</span>}
        </p>
        {isFiltered && (
          <button
            onClick={resetAll}
            className="text-sm text-[#0D47A1] hover:underline font-medium"
          >
            Clear filters
          </button>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto border border-[#E0E0E0] rounded-md">
        <table className="w-full text-sm min-w-[720px]">
          <thead className="bg-[#FAFAFA] border-b border-[#E0E0E0]">
            <tr>
              <Th label="Cable" sortable k="cable_name" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
              <Th label="RFS" sortable k="rfs_year" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
              <Th label="Length (km)" sortable k="length_km" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
              <Th label="Status" sortable k="status" sortKey={sortKey} sortDir={sortDir} onSort={toggleSort} />
              <Th label="Supplier bloc" />
              <Th label="Owner bloc" />
            </tr>
          </thead>
          <tbody>
            {filtered.slice(0, visible).map((c) => {
              const open = expanded === c.id
              return (
                <tr key={c.id} className="border-b border-[#EEEEEE] last:border-0 align-top">
                  <td colSpan={6} className="p-0">
                    <button
                      onClick={() => setExpanded(open ? null : c.id)}
                      className={`w-full text-left grid grid-cols-[2fr_0.6fr_0.9fr_1.2fr_1fr_1fr] gap-2 px-4 py-3 hover:bg-[#F7F9FC] transition-colors ${
                        open ? 'bg-[#F4F8FE]' : ''
                      }`}
                    >
                      <span className="font-medium text-[#212121]">{c.cable_name}</span>
                      <span className="text-[#616161]">{c.rfs_year || '—'}</span>
                      <span className="text-[#616161]">
                        {num(c.length_km) ? num(c.length_km).toLocaleString() : '—'}
                      </span>
                      <span className="text-[#616161]">{c.status || '—'}</span>
                      <span><Pill value={c.supplier_bloc} /></span>
                      <span><Pill value={c.owner_bloc} /></span>
                    </button>

                    {open && (
                      <div className="px-4 pb-5 pt-1 bg-[#F4F8FE] border-t border-[#E3EBF5]">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 text-sm">
                          <Detail label="Owners" items={toList(c.owners)} />
                          <Detail label="Suppliers" items={toList(c.suppliers)} />
                          <Detail label="Landing countries" items={toList(c.landing_countries)} />
                          <Detail label="Regions" items={toList(c.regions)} />
                          <Detail
                            label="Landing stations"
                            items={toList(c.landing_stations)}
                            className="md:col-span-2"
                            limit={12}
                          />
                        </div>
                        {c.source && (
                          <div className="mt-4">
                            <a
                              href={toList(c.source)[0]}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-[#0D47A1] text-sm font-medium hover:underline"
                            >
                              View source →
                            </a>
                          </div>
                        )}
                      </div>
                    )}
                  </td>
                </tr>
              )
            })}

            {filtered.length === 0 && (
              <tr>
                <td colSpan={6} className="px-4 py-10 text-center text-[#616161]">
                  No cables match those filters.{' '}
                  <button onClick={resetAll} className="text-[#0D47A1] hover:underline font-medium">
                    Clear filters
                  </button>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {visible < filtered.length && (
        <div className="text-center mt-4">
          <button
            onClick={() => setVisible((v) => v + PAGE_SIZE)}
            className="px-5 py-2.5 border border-[#0D47A1] text-[#0D47A1] text-sm font-semibold rounded-md hover:bg-[#F4F8FE] transition-colors"
          >
            Show {Math.min(PAGE_SIZE, filtered.length - visible)} more
          </button>
        </div>
      )}
    </div>
  )
}

function Detail({ label, items, className = '', limit = 0 }) {
  if (!items.length) return null
  const shown = limit && items.length > limit ? items.slice(0, limit) : items
  const rest = limit && items.length > limit ? items.length - limit : 0
  return (
    <div className={className}>
      <div className="text-xs uppercase tracking-wide text-[#0D47A1] font-semibold mb-1.5">
        {label}
      </div>
      <div className="flex flex-wrap gap-1.5">
        {shown.map((it, i) => (
          <span
            key={`${it}-${i}`}
            className="bg-white border border-[#E0E0E0] rounded px-2 py-0.5 text-[#424242] text-xs"
          >
            {it}
          </span>
        ))}
        {rest > 0 && <span className="text-xs text-[#9E9E9E] px-1 py-0.5">+{rest} more</span>}
      </div>
    </div>
  )
}

export default CableExplorer
