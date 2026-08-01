const EMOJI_BASE = 'https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/svg'

const EMOJI_PATHS = {
  sun: `${EMOJI_BASE}/2600.svg`,
  cloudSun: `${EMOJI_BASE}/1f324.svg`,
  cloud: `${EMOJI_BASE}/2601.svg`,
  fog: `${EMOJI_BASE}/1f32b.svg`,
  rain: `${EMOJI_BASE}/1f327.svg`,
  snow: `${EMOJI_BASE}/2744.svg`,
  storm: `${EMOJI_BASE}/26c8.svg`,
}

function pickIconKey(condition = '') {
  if (condition.includes('뇌우')) return 'storm'
  if (condition.includes('눈')) return 'snow'
  if (condition.includes('비') || condition.includes('이슬비') || condition.includes('소나기')) return 'rain'
  if (condition.includes('안개')) return 'fog'
  if (condition.includes('대체로 맑') || condition.includes('구름 조금')) return 'cloudSun'
  if (condition.includes('흐림') || condition.includes('구름')) return 'cloud'
  if (condition.includes('맑음')) return 'sun'
  return 'cloud'
}

export default function WeatherIcon({ condition, className }) {
  const key = pickIconKey(condition)
  return (
    <img
      className={className}
      src={EMOJI_PATHS[key]}
      alt={condition || ''}
      loading="lazy"
    />
  )
}
