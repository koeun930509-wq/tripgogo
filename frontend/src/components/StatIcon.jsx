const ICONS = {
  drop: (
    <path d="M12 2.5C9.5 6.5 6 10.8 6 14.5a6 6 0 0 0 12 0c0-3.7-3.5-8-6-12Z" />
  ),
  umbrella: (
    <>
      <path d="M12 3a9 9 0 0 0-9 9h4.5a1.5 1.5 0 0 1 3 0v.2a1.5 1.5 0 0 0 3 0V12a1.5 1.5 0 0 1 3 0h4.5a9 9 0 0 0-9-9Z" />
      <path
        d="M12 12v5.5a2.2 2.2 0 0 1-2.2 2.2 2.2 2.2 0 0 1-2.1-1.5"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.7"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </>
  ),
  wind: (
    <path
      d="M3 8h10a2.5 2.5 0 1 0-2.5-2.5M3 12h14a2.5 2.5 0 1 1-2.5 2.5M3 16h7a2 2 0 1 1-2 2"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
    />
  ),
  smile: (
    <>
      <circle cx="12" cy="12" r="9" />
      <circle cx="9" cy="10" r="1.3" fill="#fff" />
      <circle cx="15" cy="10" r="1.3" fill="#fff" />
      <path d="M8 14c1 1.5 2.5 2.3 4 2.3s3-.8 4-2.3" fill="none" stroke="#fff" strokeWidth="1.6" strokeLinecap="round" />
    </>
  ),
}

export default function StatIcon({ type, className }) {
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
    >
      {ICONS[type]}
    </svg>
  )
}
