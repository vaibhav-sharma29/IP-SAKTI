/**
 * LANGUAGE TOGGLE
 *
 * Props:
 * - value: "en" | "hi"
 * - onChange: function(newValue)
 *
 * Renders as: [ EN | हिं ]
 */
export default function LanguageToggle({ value, onChange }) {
  const options = [
    { val: 'en', label: 'EN', title: 'English' },
    { val: 'hi', label: 'हिं', title: 'हिंदी (Hindi)', isHindi: true },
  ]

  return (
    <div
      role="group"
      aria-label="Select language"
      className="inline-flex rounded-lg overflow-hidden border border-gray-700 divide-x divide-gray-700 bg-gray-950/60 shadow-sm"
    >
      {options.map(opt => {
        const isActive = value === opt.val
        return (
          <button
            key={opt.val}
            type="button"
            title={opt.title}
            aria-pressed={isActive}
            aria-label={opt.title}
            onClick={() => onChange(opt.val)}
            className={`min-w-[44px] px-3 py-1.5 sm:px-4 sm:py-2 text-sm font-medium transition-colors text-center ${
              opt.isHindi ? 'font-hindi' : ''
            } ${
              isActive
                ? 'bg-purple-600 text-white shadow-sm font-semibold'
                : 'bg-transparent text-gray-400 hover:text-white hover:bg-gray-800/50'
            }`}
          >
            {opt.label}
          </button>
        )
      })}
    </div>
  )
}
