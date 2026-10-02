// Lookup tables that place countries_map rows on the world-atlas (Natural Earth 50m) map.
//
// A row is positioned by, in order:
//   1. COUNTRY_COORDINATES (explicit [lat, lon]), else
//   2. the centroid of the largest polygon of its atlas feature, found by name
//      (via NAME_TO_ATLAS when the spellings differ).
// Rows that resolve to neither are listed under the map, never silently dropped.

// countries_map name -> world-atlas properties.name, where they differ.
export const NAME_TO_ATLAS = {
  'United States': 'United States of America',
  'Democratic Republic of the Congo': 'Dem. Rep. Congo',
  'Republic of the Congo': 'Congo',
  'Dominican Republic': 'Dominican Rep.',
  'Equatorial Guinea': 'Eq. Guinea',
  'Sao Tome and Principe': 'São Tomé and Principe',
  'French Polynesia': 'Fr. Polynesia',
  'Virgin Islands (U.S.)': 'U.S. Virgin Is.',
  'Virgin Islands (British)': 'British Virgin Is.',
  'Northern Mariana Islands': 'N. Mariana Is.',
  'Solomon Islands': 'Solomon Is.',
  'Faroe Islands': 'Faeroe Is.',
  'Saint Kitts and Nevis': 'St. Kitts and Nevis',
  'Saint Vincent and the Grenadines': 'St. Vin. and Gren.',
  'Saint Martin': 'St-Martin',
  'Saint Barthélemy': 'St-Barthélemy',
  'Saint Pierre and Miquelon': 'St. Pierre and Miquelon',
  'Antigua and Barbuda': 'Antigua and Barb.',
  'Turks and Caicos Islands': 'Turks and Caicos Is.',
  'Cayman Islands': 'Cayman Is.',
  'Cook Islands': 'Cook Is.',
  'Marshall Islands': 'Marshall Is.',
  'Wallis and Futuna': 'Wallis and Futuna Is.',
  // Natural Earth groups Christmas and Cocos (Keeling) Islands; the largest polygon is Christmas Island.
  'Christmas Island': 'Indian Ocean Ter.',
  // Natural Earth groups St Helena, Ascension and Tristan da Cunha; positioned explicitly below.
  'Ascension and Tristan da Cunha': 'Saint Helena',
}

// Explicit marker positions as [lat, lon]. These take precedence over atlas centroids.
export const COUNTRY_COORDINATES = {
  // Hand-placed positions carried over from the original Leaflet map
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
  'United Arab Emirates': [23.4241, 53.8478],
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
  'Oman': [21.4735, 55.9754],

  // No polygon of their own in Natural Earth 50m (part of France / the Netherlands, or too small)
  'Martinique': [14.64, -61.02],
  'Guadeloupe': [16.27, -61.55],
  'French Guiana': [3.93, -53.13],
  'Réunion': [-21.12, 55.54],
  'Mayotte': [-12.83, 45.17],
  'Bonaire': [12.20, -68.26],
  'Sint Eustatius and Saba': [17.49, -62.97],
  'Gibraltar': [36.14, -5.35],
  'Tokelau': [-9.20, -171.85],
  'Tuvalu': [-8.52, 179.20],
  // Ascension Island, so it doesn't stack on the separate "Saint Helena" marker
  'Ascension and Tristan da Cunha': [-7.95, -14.36],
  // Combined label in the source data, not a single place; placed at Curaçao.
  // Unresolved — see DATA_DICTIONARY.md, "Known data quality notes".
  'Netherlands (Curacao/Bonaire)': [12.17, -68.99],
}
