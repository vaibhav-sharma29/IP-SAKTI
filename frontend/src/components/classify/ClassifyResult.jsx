/**
 * CLASSIFY RESULT — Shows backend classification response
 *
 * Props:
 * - result: {
 *     category: string,
 *     ip_posture: string,
 *     regulatory_track: string,
 *     patent_possible: boolean,
 *     key_actions: string[],
 *     warning: string
 *   }
 * - onReset: function() — "Classify Another Product" button
 */
export default function ClassifyResult({ result, onReset }) {
  return (
    <div className="space-y-5">

      {/* Category badge */}
      <div className="bg-purple-900/40 border border-purple-700 rounded-xl p-4">
        <p className="text-xs text-purple-400 uppercase tracking-wider mb-1">Product Category</p>
        <p className="text-2xl font-bold">{result.category}</p>
      </div>

      {/* Patent possible */}
      <div className="bg-gray-800 rounded-xl p-4 flex items-center gap-3">
        <span className="text-3xl">{result.patent_possible ? '✅' : '❌'}</span>
        <div>
          <p className="font-medium">Patent {result.patent_possible ? 'Possible' : 'Not Possible'}</p>
          <p className="text-sm text-gray-400">on this formulation</p>
        </div>
      </div>

      {/* IP Posture */}
      <div className="bg-gray-800 rounded-xl p-4">
        <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">IP Position</p>
        <p className="text-gray-200">{result.ip_posture}</p>
      </div>

      {/* Regulatory track */}
      <div className="bg-gray-800 rounded-xl p-4">
        <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Regulatory Track</p>
        <p className="text-gray-200">{result.regulatory_track}</p>
      </div>

      {/* Key Actions */}
      <div className="bg-gray-800 rounded-xl p-4">
        <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Recommended Actions</p>
        <ol className="space-y-2">
          {result.key_actions.map((action, i) => (
            <li key={i} className="flex gap-3 text-gray-200">
              <span className="text-purple-400 font-bold">{i + 1}.</span>
              <span>{action}</span>
            </li>
          ))}
        </ol>
      </div>

      {/* Warning box — only if warning exists */}
      {result.warning && (
        <div className="bg-yellow-900/30 border border-yellow-700 rounded-xl p-4">
          <p className="text-yellow-300">⚠️ {result.warning}</p>
        </div>
      )}

      {/* Reset button */}
      <button
        onClick={onReset}
        className="w-full py-3 border border-gray-600 hover:border-purple-500
                   rounded-xl text-gray-400 hover:text-white transition"
      >
        ← Classify Another Product
      </button>
    </div>
  )
}
