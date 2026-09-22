/**
 * JURISDICTION TOGGLE
 *
 * Props:
 * - value: "india" | "international" | "both"
 * - onChange: function(newValue)
 *
 * Renders as a segmented control:
 * [ 🇮🇳 India | 🌍 International ]
 *
 * Active button = purple filled
 * Inactive = gray outline
 */
export default function JurisdictionToggle({ value, onChange }) {
  const options = [
    { val: 'india',         label: '🇮🇳 India' },
    { val: 'international', label: '🌍 International' },
  ]

  return (
    <div className="inline-flex rounded-lg overflow-hidden border border-gray-700 divide-x divide-gray-700 bg-gray-950/60 shadow-sm">
      {options.map(opt => {
        const isActive = value === opt.val
        return (
          <button
            key={opt.val}
            type="button"
            onClick={() => onChange(opt.val)}
            className={`px-4 py-2 text-sm font-medium transition-colors ${
              isActive
                ? 'bg-purple-600 text-white shadow-sm'
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
