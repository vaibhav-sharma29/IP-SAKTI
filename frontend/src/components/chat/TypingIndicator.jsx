/**
 * TYPING INDICATOR — shown while backend is processing
 * 3 animated dots — like WhatsApp typing animation
 */
export default function TypingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="bg-gray-800 rounded-2xl px-4 py-3 flex gap-1 items-center">
        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0ms]" />
        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:150ms]" />
        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:300ms]" />
      </div>
    </div>
  )
}
