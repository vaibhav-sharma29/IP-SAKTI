/**
 * CONFIDENCE BADGE
 *
 * Props:
 * - level: "high" | "medium" | "low"
 *
 * high   → green  badge  "High Confidence ✅"
 * medium → yellow badge  "Verify with Expert ⚠️"
 * low    → red    badge  "Consult Attorney ❌"
 */
const CONFIG = {
  high:   { label: 'High Confidence',    emoji: '✅', cls: 'bg-green-900  text-green-300'  },
  medium: { label: 'Verify with Expert', emoji: '⚠️', cls: 'bg-yellow-900 text-yellow-300' },
  low:    { label: 'Consult Attorney',   emoji: '❌', cls: 'bg-red-900    text-red-300'    },
}

export default function ConfidenceBadge({ level }) {
  const cfg = CONFIG[level] || CONFIG.medium
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${cfg.cls}`}>
      {cfg.emoji} {cfg.label}
    </span>
  )
}
