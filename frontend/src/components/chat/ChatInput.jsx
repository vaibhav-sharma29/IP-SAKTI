/**
 * CHAT INPUT — Bottom input bar
 *
 * Props:
 * - onSend: function(query: string) — called when user submits
 * - loading: boolean — disable input when true
 * - language: "en"|"hi" — show placeholder in correct language
 *
 * Behavior:
 * - Enter key = submit (Shift+Enter = new line)
 * - Send button click = submit
 * - Clear input after submit
 */
import { useState, useRef, useEffect } from 'react'
import { Send, Sparkles } from 'lucide-react'

const PLACEHOLDERS = {
  en: 'Ask about patents, trademarks, GI tags, biodiversity compliance...',
  hi: 'पेटेंट, ट्रेडमार्क, GI टैग के बारे में पूछें...'
}

export default function ChatInput({ onSend, loading, language = 'en' }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)

  const handleSubmit = () => {
    if (!value.trim() || loading) return
    onSend(value.trim())
    setValue('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  // Auto-grow textarea height dynamically up to a limit
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`
    }
  }, [value])

  return (
    <div className="w-full max-w-4xl mx-auto mt-auto pt-2 pb-4 px-2">
      <div className="relative flex items-end gap-2 bg-gray-900/90 border border-gray-700/80 focus-within:border-purple-500/80 focus-within:ring-2 focus-within:ring-purple-500/20 backdrop-blur-xl rounded-2xl p-2 shadow-2xl transition-all duration-200">
        
        {/* Left Accent Icon */}
        <div className="pl-3 pb-3 hidden sm:flex items-center text-purple-400/80">
          <Sparkles className="w-5 h-5 animate-pulse" />
        </div>

        {/* Text Area */}
        <textarea
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          placeholder={PLACEHOLDERS[language] || PLACEHOLDERS.en}
          className="flex-1 bg-transparent text-gray-100 placeholder-gray-500 resize-none py-2 px-2 focus:outline-none text-sm md:text-base leading-relaxed max-h-32 disabled:opacity-50"
        />

        {/* Submit Button */}
        <button
          type="button"
          onClick={handleSubmit}
          disabled={loading || !value.trim()}
          className="p-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 active:scale-95 text-white disabled:opacity-30 disabled:hover:from-purple-600 disabled:hover:to-indigo-600 disabled:cursor-not-allowed rounded-xl transition-all duration-200 flex items-center justify-center shadow-md shadow-purple-600/30 cursor-pointer flex-shrink-0"
          title="Send message"
        >
          <Send className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Helper Footer Tip */}
      <div className="flex justify-between items-center px-4 mt-2 text-[11px] text-gray-500">
        <span>Press <kbd className="px-1.5 py-0.5 bg-gray-800 border border-gray-700 rounded text-gray-400 font-mono">Enter</kbd> to send</span>
        <span>Use <kbd className="px-1.5 py-0.5 bg-gray-800 border border-gray-700 rounded text-gray-400 font-mono">Shift + Enter</kbd> for new line</span>
      </div>
    </div>
  )
}