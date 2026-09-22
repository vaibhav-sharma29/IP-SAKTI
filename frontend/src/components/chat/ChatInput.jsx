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
import { useState } from 'react'
import { Send } from 'lucide-react'

const PLACEHOLDERS = {
  en: 'Ask about patents, trademarks, GI tags, biodiversity compliance...',
  hi: 'पेटेंट, ट्रेडमार्क, GI टैग के बारे में पूछें...'
}

export default function ChatInput({ onSend, loading, language }) {
  const [value, setValue] = useState('')

  const handleSubmit = () => {
    if (!value.trim() || loading) return
    onSend(value.trim())
    setValue('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="flex gap-2 mt-auto">
      <textarea
        rows={2}
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
        placeholder={PLACEHOLDERS[language] || PLACEHOLDERS.en}
        className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3
                   text-gray-100 placeholder-gray-500 resize-none
                   focus:outline-none focus:border-purple-500 transition
                   disabled:opacity-50"
      />
      <button
        onClick={handleSubmit}
        disabled={loading || !value.trim()}
        className="px-4 bg-purple-600 hover:bg-purple-700 disabled:opacity-40
                   rounded-xl transition flex items-center justify-center"
      >
        <Send size={20} />
      </button>
    </div>
  )
}
