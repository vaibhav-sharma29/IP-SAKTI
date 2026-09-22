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
  high: {
    label: 'High Confidence',
    emoji: '✅',
    cls: 'bg-emerald-950/80 text-emerald-300 border border-emerald-500/30',
  },
  medium: {
    label: 'Verify with Expert',
    emoji: '⚠️',
    cls: 'bg-amber-950/80 text-amber-300 border border-amber-500/30',
  },
  low: {
    label: 'Consult Attorney',
    emoji: '❌',
    cls: 'bg-rose-950/80 text-rose-300 border border-rose-500/30',
  },
}

export default function ConfidenceBadge({ level }) {
  const normalizedLevel = level?.toLowerCase()
  const cfg = CONFIG[normalizedLevel] || CONFIG.medium

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${cfg.cls}`}
    >
      <span>{cfg.label}</span>
      <span>{cfg.emoji}</span>
    </span>
  )
}
