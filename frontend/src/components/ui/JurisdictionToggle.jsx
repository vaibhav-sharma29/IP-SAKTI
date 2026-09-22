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
    <div className="flex rounded-lg overflow-hidden border border-gray-700">
      {options.map(opt => (
        <button
          key={opt.val}
          onClick={() => onChange(opt.val)}
          className={`px-4 py-2 text-sm font-medium transition ${
            value === opt.val
              ? 'bg-purple-600 text-white'
              : 'bg-gray-900 text-gray-400 hover:text-white'
          }`}
        >
          {opt.label}
        </button>
      ))}
    </div>
  )
}
