/**
 * SOURCE CARDS — shown below each AI answer
 *
 * Props:
 * - sources: Array<{ title: string, section: string, url: string }>
 *
 * Render each source as a small card:
 * 📄 Patents Act 1970 — Section 3(p)  [↗ link]
 *
 * Style: small, subtle, pill-shaped cards
 */
export default function SourceCards({ sources }) {
  if (!sources || !Array.isArray(sources) || sources.length === 0) return null

  return (
    <div className="flex flex-wrap items-center gap-2 pt-1">
      {sources.map((src, i) => {
        const hasUrl = Boolean(src.url && src.url.trim() && src.url !== '#')
        const CardElement = hasUrl ? 'a' : 'div'

        return (
          <CardElement
            key={`${src.title || 'src'}-${i}`}
            {...(hasUrl
              ? {
                  href: src.url,
                  target: '_blank',
                  rel: 'noopener noreferrer',
                  title: `Open source: ${src.title}`,
                }
              : {})}
            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs transition-all duration-150 border ${
              hasUrl
                ? 'bg-gray-900/80 hover:bg-gray-900 border-gray-700/80 hover:border-purple-500/50 text-gray-300 hover:text-white group cursor-pointer shadow-sm'
                : 'bg-gray-900/50 border-gray-700/60 text-gray-300'
            }`}
          >
            <span className="text-xs select-none">📄</span>
            <span className="font-medium text-gray-200">{src.title}</span>
            {src.section && (
              <span className="text-gray-400 font-normal">
                — {src.section}
              </span>
            )}
            {hasUrl && (
              <span className="text-purple-400 group-hover:text-purple-300 text-[11px] font-semibold ml-0.5">
                ↗
              </span>
            )}
          </CardElement>
        )
      })}
    </div>
  )
}
