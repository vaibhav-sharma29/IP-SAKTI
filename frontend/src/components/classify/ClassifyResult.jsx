export default function ClassifyResult({ result, onReset }) {
  if (!result) return null

  return (
    <div className="w-full max-w-2xl mx-auto space-y-5 animate-fadeIn">

      {/* Category Header */}
      <div className="relative overflow-hidden bg-gradient-to-r from-purple-950/80 via-gray-900 to-slate-900 border border-purple-700/60 rounded-2xl p-6 shadow-xl backdrop-blur-xl">
        <div className="absolute top-0 right-0 w-32 h-32 bg-purple-600/10 rounded-full blur-2xl pointer-events-none" />
        <p className="text-xs font-semibold text-purple-400 uppercase tracking-widest mb-1">Product Category</p>
        <h2 className="text-2xl md:text-3xl font-extrabold text-gray-100 tracking-tight">
          {result.category || 'Unclassified'}
        </h2>
      </div>

      {/* Patent Status + IP Posture */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className={`p-5 rounded-2xl border backdrop-blur-md flex items-center gap-4 shadow-md ${
          result.patent_possible
            ? 'bg-emerald-950/30 border-emerald-700/50'
            : 'bg-rose-950/30 border-rose-700/50'
        }`}>
          <span className="text-3xl p-3 bg-gray-900/80 rounded-xl border border-gray-700/50">
            {result.patent_possible ? '✅' : '❌'}
          </span>
          <div>
            <p className="font-bold text-base text-gray-100">
              Patent {result.patent_possible ? 'Possible' : 'Not Possible'}
            </p>
            <p className="text-xs text-gray-400 mt-0.5">Based on present formulation rules</p>
          </div>
        </div>

        <div className="bg-gray-800/80 border border-gray-700/70 rounded-2xl p-5 shadow-md backdrop-blur-md">
          <p className="text-xs font-medium text-gray-400 uppercase tracking-wider mb-1.5">IP Position</p>
          <p className="text-sm font-semibold text-gray-200 leading-relaxed">
            {result.ip_posture || 'No IP posture details provided'}
          </p>
        </div>
      </div>

      {/* Regulatory Track */}
      <div className="bg-gray-800/80 border border-gray-700/70 rounded-2xl p-5 shadow-md backdrop-blur-md">
        <p className="text-xs font-medium text-gray-400 uppercase tracking-wider mb-1.5">Regulatory Track</p>
        <p className="text-sm font-medium text-purple-300 leading-relaxed">
          {result.regulatory_track || 'Standard Compliance Track'}
        </p>
      </div>

      {/* Recommended Actions */}
      {result.key_actions && result.key_actions.length > 0 && (
        <div className="bg-gray-800/80 border border-gray-700/70 rounded-2xl p-6 shadow-md backdrop-blur-md">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Recommended Actions</p>
          <ol className="space-y-3">
            {result.key_actions.map((action, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-gray-200">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-900/60 border border-purple-600/50 text-purple-300 font-bold text-xs flex items-center justify-center">
                  {i + 1}
                </span>
                <span className="leading-snug pt-0.5">{action}</span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* ABS Compliance */}
      {result.abs_required && result.abs_checklist && result.abs_checklist.length > 0 && (
        <div className="bg-amber-950/20 border border-amber-700/50 rounded-2xl p-6 shadow-md backdrop-blur-md">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-xl">🌿</span>
            <p className="text-sm font-semibold text-amber-300 uppercase tracking-wider">
              ABS Compliance Required
            </p>
          </div>
          <p className="text-xs text-amber-200/70 mb-4">
            Biological Diversity Act 2002 — NBA approval needed before commercial use or patent filing.
          </p>
          <ol className="space-y-2">
            {result.abs_checklist.map((item, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-amber-100">
                <span className="flex-shrink-0 w-5 h-5 rounded-full bg-amber-900/60 border border-amber-600/50 text-amber-300 font-bold text-xs flex items-center justify-center mt-0.5">
                  {i + 1}
                </span>
                <span className="leading-snug">{item}</span>
              </li>
            ))}
          </ol>
          <a
            href="https://nbaindia.org"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 mt-4 text-xs text-amber-400 hover:text-amber-300 underline"
          >
            Apply at nbaindia.org ↗
          </a>
        </div>
      )}

      {/* Warning */}
      {result.warning && (
        <div className="bg-amber-950/40 border border-amber-600/60 rounded-2xl p-5 shadow-lg flex items-start gap-3 text-amber-200">
          <span className="text-xl flex-shrink-0">⚠️</span>
          <p className="text-sm font-medium leading-relaxed">{result.warning}</p>
        </div>
      )}

      {/* Reset Button */}
      <button
        onClick={onReset}
        className="w-full py-3.5 px-6 border border-gray-700 hover:border-purple-500/80 bg-gray-900/80 hover:bg-gray-800 rounded-2xl text-gray-300 hover:text-white font-medium text-sm transition-all duration-200 shadow-lg flex items-center justify-center gap-2 cursor-pointer"
      >
        ← Classify Another Product
      </button>

    </div>
  )
}
