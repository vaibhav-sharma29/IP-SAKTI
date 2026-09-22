/**
 * TYPING INDICATOR — shown while backend is processing
 * 3 animated dots — WhatsApp style with subtle neon accent
 */
export default function TypingIndicator() {
  return (
    <div className="flex justify-start my-2">
      <div className="bg-slate-900/80 backdrop-blur-md border border-slate-700/50 rounded-2xl px-4 py-3 flex gap-1.5 items-center shadow-lg">
        <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce [animation-delay:0ms]" />
        <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce [animation-delay:150ms]" />
        <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce [animation-delay:300ms]" />
      </div>
    </div>
  )
}