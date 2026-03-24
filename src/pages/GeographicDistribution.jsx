import { useState, useEffect, useRef } from 'react'
import { supabase } from '../lib/supabase'

function GeographicDistribution({ infrastructureType = 'cables' }) {
  const [countryData, setCountryData] = useState(null)
  const [loading, setLoading] = useState(true)
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)

  useEffect(() => {
    async function loadData() {
      const { data: countries, error } = await supabase
        .from('countries_map')
        .select('*')
        .order('cables', { ascending: false })
      
      if (error) {
        console.error('Error:', error)
        setLoading(false)
        return
      }
  
      setCountryData({
        countries: countries,
        total_countries: countries.length,
        total_cables: countries.reduce((sum, c) => sum + c.cables, 0)
      })
      setLoading(false)
    }
    
    loadData()
  }, [infrastructureType])

  useEffect(() => {
    if (!countryData || !mapRef.current || mapInstanceRef.current) return

    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)

    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.onload = () => {
      const L = window.L

      const map = L.map(mapRef.current, {
        center: [20, 0],
        zoom: 2,
        minZoom: 2,
        maxZoom: 5,
        scrollWheelZoom: true,
        zoomControl: true
      })

      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
        subdomains: 'abcd',
        maxZoom: 19
      }).addTo(map)

      const countryCoordinates = {
        'United States': [37.0902, -95.7129],
        'United Kingdom': [55.3781, -3.4360],
        'Japan': [36.2048, 138.2529],
        'Singapore': [1.3521, 103.8198],
        'France': [46.2276, 2.2137],
        'India': [20.5937, 78.9629],
        'China': [35.8617, 104.1954],
        'Australia': [-25.2744, 133.7751],
        'Brazil': [-14.2350, -51.9253],
        'South Africa': [-30.5595, 22.9375],
        'Hong Kong': [22.3193, 114.1694],
        'Taiwan': [23.6978, 120.9605],
        'Philippines': [12.8797, 121.7740],
        'Indonesia': [-0.7893, 113.9213],
        'Malaysia': [4.2105, 101.9758],
        'Thailand': [15.8700, 100.9925],
        'South Korea': [35.9078, 127.7669],
        'Germany': [51.1657, 10.4515],
        'Spain': [40.4637, -3.7492],
        'Italy': [41.8719, 12.5674],
        'Denmark': [56.2639, 9.5018],
        'Sweden': [60.1282, 18.6435],
        'Norway': [60.4720, 8.4689],
        'Netherlands': [52.1326, 5.2913],
        'Ireland': [53.4129, -8.2439],
        'Canada': [56.1304, -106.3468],
        'Mexico': [23.6345, -102.5528],
        'Egypt': [26.8206, 30.8025],
        'UAE': [23.4241, 53.8478],
        'Saudi Arabia': [23.8859, 45.0792],
        'Portugal': [39.3999, -8.2245],
        'Greece': [39.0742, 21.8243],
        'Turkey': [38.9637, 35.2433],
        'Israel': [31.0461, 34.8516],
        'New Zealand': [-40.9006, 174.8860],
        'Argentina': [-38.4161, -63.6167],
        'Chile': [-35.6751, -71.5430],
        'Colombia': [4.5709, -74.2973],
        'Venezuela': [6.4238, -66.5897],
        'Peru': [-9.1900, -75.0152],
        'Vietnam': [14.0583, 108.2772],
        'Pakistan': [30.3753, 69.3451],
        'Bangladesh': [23.6850, 90.3563],
        'Sri Lanka': [7.8731, 80.7718],
        'Myanmar': [21.9162, 95.9560],
        'Kenya': [-0.0236, 37.9062],
        'Nigeria': [9.0820, 8.6753],
        'Morocco': [31.7917, -7.0926],
        'Finland': [61.9241, 25.7482],
        'Poland': [51.9194, 19.1451],
        'Oman': [21.4735, 55.9754]
      }

      countryData.countries.forEach(country => {
        const coords = countryCoordinates[country.name]
        if (!coords) return

        const size = country.cables > 50 ? 12 :
                    country.cables > 20 ? 9 :
                    country.cables > 10 ? 7 : 5

        const color = country.cables > 50 ? '#00E5FF' :
                     country.cables > 20 ? '#00BCD4' :
                     '#4FC3F7'

        const circle = L.circleMarker(coords, {
          radius: size,
          fillColor: color,
          color: 'white',
          weight: 2,
          opacity: 0.9,
          fillOpacity: 0.8
        }).addTo(map)

        circle.bindPopup(`
          <div style="font-family: Inter, sans-serif;">
            <strong style="font-size: 0.95rem; color: #0D47A1;">${country.name}</strong><br/>
            <span style="font-size: 0.875rem; color: #616161;">${country.cables} submarine cables</span>
          </div>
        `)
      })

      mapInstanceRef.current = map
    }

    document.head.appendChild(script)

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [countryData])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <div className="w-10 h-10 border-4 border-gray-200 border-t-[#0D47A1] rounded-full animate-spin mb-4"></div>
        <p className="text-[#616161]">Loading geographic data...</p>
      </div>
    )
  }

  if (!countryData) {
    return (
      <div>
        <div className="mb-10">
          <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Geographic Distribution</h1>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <p className="text-[#616161]">Data not available. Run extract_countries_for_map.py</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-10">
        <h1 className="font-serif text-4xl font-bold text-[#212121] mb-3">Geographic Distribution</h1>
        <p className="text-base text-[#616161] leading-relaxed max-w-4xl">
          Interactive world map showing {countryData.total_countries} countries with submarine cable infrastructure
        </p>
      </div>

      {/* Interactive Map */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-2">Global Cable Landing Points</h2>
          <p className="text-sm text-[#616161] mb-6 leading-relaxed">
            Interactive map with actual geographic locations. Click markers for details.
          </p>

          <div 
            ref={mapRef} 
            className="h-[600px] w-full rounded-lg mt-6 border border-[#E0E0E0]"
          />

          <div className="mt-6 flex justify-center gap-10 text-sm text-[#616161]">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#00E5FF] border-2 border-white"></div>
              <span>Major Hub (&gt;50 cables)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-[#00BCD4] border-2 border-white"></div>
              <span>Significant (20-50)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-[#4FC3F7] border-2 border-white"></div>
              <span>Active (10-20)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-[#4FC3F7] border-2 border-white"></div>
              <span>Present (&lt;10)</span>
            </div>
          </div>

          <div className="mt-6 p-5 bg-[#E3F2FD] rounded-md">
            <p className="text-sm text-[#0D47A1] m-0 leading-relaxed">
              <strong>Interactive Features:</strong> Zoom and pan to explore. Click cyan dots to see country names and cable counts. 
              Larger, brighter dots indicate major cable hubs. For detailed cable routes and exact paths, visit{' '}
              <a href="https://www.submarinecablemap.com/" target="_blank" rel="noopener noreferrer" className="text-[#0D47A1] font-semibold underline">
                TeleGeography's Submarine Cable Map
              </a>.
            </p>
          </div>
        </div>
      </section>

      {/* Top Countries */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Top 20 Countries by Cable Infrastructure</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {countryData.countries.slice(0, 20).map((country, idx) => (
              <div 
                key={country.name} 
                className={`p-4 rounded-md flex justify-between items-center transition-all hover:-translate-y-0.5 hover:shadow-lg ${
                  idx < 5 
                    ? 'bg-[#E3F2FD] border-2 border-[#64B5F6]' 
                    : 'bg-[#FAFAFA] border border-[#E0E0E0]'
                }`}
              >
                <div>
                  <div className={`font-serif text-base ${idx < 5 ? 'font-bold' : 'font-semibold'} text-[#212121]`}>
                    {country.name}
                  </div>
                  {idx < 5 && (
                    <div className="text-xs text-[#757575] mt-0.5">
                      Rank #{idx + 1}
                    </div>
                  )}
                </div>
                <div className={`font-serif text-2xl font-bold ${idx < 5 ? 'text-[#0D47A1]' : 'text-[#616161]'}`}>
                  {country.cables}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Regional Insights */}
      <section className="mb-10">
        <div className="bg-white rounded-lg shadow-sm border border-[#E0E0E0] p-8">
          <h2 className="font-serif text-2xl font-semibold text-[#212121] mb-6">Key Geographic Insights</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div className="p-6 bg-[#E3F2FD] rounded-lg border-l-4 border-[#0D47A1]">
              <h4 className="font-serif text-base font-semibold mb-3 text-[#0D47A1]">
                Major Hubs
              </h4>
              <p className="text-sm leading-relaxed text-[#212121] m-0">
                United States (85), United Kingdom (52), and Indonesia (42) serve as primary cable landing hubs, 
                connecting major trade routes and population centers.
              </p>
            </div>

            <div className="p-6 bg-[#FFF3E0] rounded-lg border-l-4 border-[#F57C00]">
              <h4 className="font-serif text-base font-semibold mb-3 text-[#E65100]">
                European Density
              </h4>
              <p className="text-sm leading-relaxed text-[#212121] m-0">
                Europe shows highest cable density with UK, Spain, Italy, France, and Scandinavia forming 
                a concentrated network hub serving as gateway between Americas and Asia.
              </p>
            </div>

            <div className="p-6 bg-[#F3E5F5] rounded-lg border-l-4 border-[#6A1B9A]">
              <h4 className="font-serif text-base font-semibold mb-3 text-[#4A148C]">
                Asia-Pacific Growth
              </h4>
              <p className="text-sm leading-relaxed text-[#212121] m-0">
                Singapore, Japan, Hong Kong, and Indonesia anchor the Asia-Pacific network, 
                with Indonesia's 42 cables reflecting its strategic position connecting Asia to Australia.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default GeographicDistribution