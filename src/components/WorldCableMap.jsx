import { useState, useEffect, useMemo, useRef } from 'react'
import { geoNaturalEarth1, geoPath, geoCentroid, geoArea, zoom, zoomIdentity, select } from 'd3'
import { feature } from 'topojson-client'
import { NAME_TO_ATLAS, COUNTRY_COORDINATES } from '../data/countryGeo'

// Self-contained vector map: country borders come from the bundled world-atlas
// TopoJSON (Natural Earth 50m), so there are no tile servers or runtime network calls.

const WIDTH = 960
const HEIGHT = 500
const MAX_ZOOM = 8

const COLORS = {
  ocean: '#0A1F44',
  land: '#1A2F5A',
  landingCountry: '#0E4A5C',
  border: '#2E4A7A',
  markerStroke: '#FFFFFF',
}

const ZOOM_BUTTON_CLASS =
  'w-8 h-8 bg-[#0D1B3A] text-white text-lg leading-none hover:bg-[#1A2F5A] border-b border-[#2E4A7A] last:border-b-0 cursor-pointer disabled:opacity-50'

function markerStyle(cables) {
  return {
    radius: cables > 50 ? 12 : cables > 20 ? 9 : cables > 10 ? 7 : 5,
    color: cables > 50 ? '#00E5FF' : cables > 20 ? '#00BCD4' : '#4FC3F7',
  }
}

// Centroid of a feature's largest polygon, so overseas territories
// don't pull a country's marker out to sea.
function largestPolygonCentroid(f) {
  const polygons = f.geometry.type === 'MultiPolygon' ? f.geometry.coordinates : [f.geometry.coordinates]
  const largest = polygons
    .map(coordinates => ({ type: 'Polygon', coordinates }))
    .reduce((a, b) => (geoArea(b) > geoArea(a) ? b : a))
  return geoCentroid(largest)
}

function WorldCableMap({ countries }) {
  const [atlas, setAtlas] = useState(null)
  const [transform, setTransform] = useState(zoomIdentity)
  const [selected, setSelected] = useState(null)
  const svgRef = useRef(null)
  const zoomRef = useRef(null)

  // Bundled with the app (code-split into its own chunk), not fetched from a third party
  useEffect(() => {
    import('world-atlas/countries-50m.json').then(topo => {
      const data = topo.default
      // Antarctica has no cable landings and takes up a large strip of the map
      setAtlas(feature(data, data.objects.countries).features.filter(f => f.properties.name !== 'Antarctica'))
    })
  }, [])

  // Fit to the land shown (Antarctica excluded) so the freed space isn't left as empty ocean
  const projection = useMemo(
    () => geoNaturalEarth1().fitExtent(
      [[8, 8], [WIDTH - 8, HEIGHT - 8]],
      atlas ? { type: 'FeatureCollection', features: atlas } : { type: 'Sphere' }
    ),
    [atlas]
  )
  const path = useMemo(() => geoPath(projection), [projection])

  const { markers, unplotted, landingAtlasNames } = useMemo(() => {
    if (!atlas) return { markers: [], unplotted: [], landingAtlasNames: new Set() }
    const featuresByName = new Map(atlas.map(f => [f.properties.name, f]))
    const markers = []
    const unplotted = []
    const landingAtlasNames = new Set()

    countries.forEach(country => {
      const atlasFeature = featuresByName.get(NAME_TO_ATLAS[country.name] || country.name)
      if (atlasFeature) landingAtlasNames.add(atlasFeature.properties.name)

      const explicit = COUNTRY_COORDINATES[country.name]
      const lonLat = explicit ? [explicit[1], explicit[0]] : atlasFeature ? largestPolygonCentroid(atlasFeature) : null
      if (!lonLat) {
        unplotted.push(country)
        return
      }
      const [x, y] = projection(lonLat)
      markers.push({ ...country, x, y, ...markerStyle(country.cables) })
    })

    // Draw big hubs first so smaller markers stay on top and clickable
    markers.sort((a, b) => b.cables - a.cables)
    return { markers, unplotted, landingAtlasNames }
  }, [atlas, countries, projection])

  useEffect(() => {
    if (unplotted.length > 0) {
      console.warn('Countries not shown on map (no atlas match or coordinates):', unplotted.map(c => c.name))
    }
  }, [unplotted])

  // Zoom and pan
  useEffect(() => {
    const svg = svgRef.current
    if (!svg) return
    const behavior = zoom()
      .scaleExtent([1, MAX_ZOOM])
      .translateExtent([[0, 0], [WIDTH, HEIGHT]])
      .on('zoom', event => setTransform(event.transform))
    select(svg).call(behavior)
    zoomRef.current = behavior
    return () => select(svg).on('.zoom', null)
  }, [])

  useEffect(() => {
    const onKey = e => { if (e.key === 'Escape') setSelected(null) }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  const zoomBy = factor => select(svgRef.current).transition().duration(250).call(zoomRef.current.scaleBy, factor)
  const resetZoom = () => select(svgRef.current).transition().duration(250).call(zoomRef.current.transform, zoomIdentity)

  const k = transform.k
  const popupPoint = selected ? transform.apply([selected.x, selected.y]) : null

  return (
    <div>
      <div className="relative w-full aspect-[960/500] rounded-lg overflow-hidden border border-[#E0E0E0]" style={{ backgroundColor: COLORS.ocean }}>
        {!atlas && (
          <div className="absolute inset-0 flex items-center justify-center text-sm text-[#B0BEC5]">Loading map…</div>
        )}

        <svg
          ref={svgRef}
          viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
          className="w-full h-full cursor-grab active:cursor-grabbing"
          role="img"
          aria-label="World map of submarine cable landing countries"
          onClick={() => setSelected(null)}
        >
          <g transform={transform.toString()}>
            <path d={path({ type: 'Sphere' })} fill={COLORS.ocean} />
            {atlas && atlas.map(f => (
              <path
                key={f.id ?? f.properties.name}
                d={path(f)}
                fill={landingAtlasNames.has(f.properties.name) ? COLORS.landingCountry : COLORS.land}
                stroke={COLORS.border}
                strokeWidth={0.5}
                vectorEffect="non-scaling-stroke"
              />
            ))}
            {markers.map(m => (
              <circle
                key={m.name}
                cx={m.x}
                cy={m.y}
                r={m.radius / k}
                fill={m.color}
                fillOpacity={0.8}
                stroke={COLORS.markerStroke}
                strokeOpacity={0.9}
                strokeWidth={2}
                vectorEffect="non-scaling-stroke"
                className="cursor-pointer focus:outline-none"
                role="button"
                tabIndex={0}
                aria-label={`${m.name}: ${m.cables} submarine cables`}
                onClick={e => { e.stopPropagation(); setSelected(m) }}
                onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setSelected(m) } }}
              />
            ))}
          </g>
        </svg>

        {selected && popupPoint && (
          <div
            className="absolute z-10 -translate-x-1/2 -translate-y-full pointer-events-none"
            style={{ left: `${(popupPoint[0] / WIDTH) * 100}%`, top: `calc(${(popupPoint[1] / HEIGHT) * 100}% - 14px)` }}
          >
            <div className="bg-white rounded-md shadow-lg px-3 py-2 whitespace-nowrap" style={{ fontFamily: 'Inter, sans-serif' }}>
              <strong className="block text-[0.95rem] text-[#0D47A1]">{selected.name}</strong>
              <span className="text-sm text-[#616161]">{selected.cables} submarine cables</span>
            </div>
          </div>
        )}

        <div className="absolute top-3 left-3 flex flex-col rounded-md overflow-hidden shadow border border-[#2E4A7A]">
          <button type="button" title="Zoom in" aria-label="Zoom in" disabled={!atlas} className={ZOOM_BUTTON_CLASS} onClick={() => zoomBy(1.6)}>+</button>
          <button type="button" title="Zoom out" aria-label="Zoom out" disabled={!atlas} className={ZOOM_BUTTON_CLASS} onClick={() => zoomBy(1 / 1.6)}>−</button>
          <button type="button" title="Reset view" aria-label="Reset view" disabled={!atlas} className={ZOOM_BUTTON_CLASS} onClick={resetZoom}>⟲</button>
        </div>
      </div>

      {unplotted.length > 0 && (
        <div className="mt-4 p-4 bg-[#FFF3E0] border border-[#FFB74D] rounded-md text-sm text-[#E65100]">
          <strong>Not shown on map ({unplotted.length}):</strong>{' '}
          {unplotted.map(c => `${c.name} (${c.cables})`).join(', ')}. These countries have no matching map shape or
          coordinates; add them to <code>src/data/countryGeo.js</code>.
        </div>
      )}
    </div>
  )
}

export default WorldCableMap
