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
  if (!sources || sources.length === 0) return null

  return (
    <div className="flex flex-wrap gap-2 mt-2">
      {sources.map((src, i) => (
        <a
          key={i}
          href={src.url || '#'}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1 px-3 py-1 bg-gray-700 hover:bg-gray-600
                     rounded-full text-xs text-gray-300 transition"
        >
          <span>📄</span>
          <span>{src.title}</span>
          {src.section && <span className="text-gray-500">— {src.section}</span>}
          {src.url && <span className="text-purple-400">↗</span>}
        </a>
      ))}
    </div>
  )
}
