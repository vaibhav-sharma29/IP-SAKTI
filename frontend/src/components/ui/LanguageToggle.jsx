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
    { val: 'en', label: 'EN' },
    { val: 'hi', label: 'हिं' },
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
