/**
 * CHAT WINDOW — Scrollable message list
 *
 * Props:
 * - messages: Array of message objects
 *   Each message: { role: "user"|"assistant", content: string,
 *                   sources?: [], confidence?: string, disclaimer?: string }
 * - loading: boolean — show typing animation when true
 *
 * Render:
 * - User messages: right-aligned, purple background
 * - Assistant messages: left-aligned, gray background
 *   Below assistant message show:
 *   1. SourceCards (list of cited sources)
 *   2. ConfidenceBadge
 *   3. Disclaimer in tiny text
 * - Loading: show TypingIndicator component
 * - Empty state: show "Ask anything about Ayurveda IP..."
 */
import { useEffect, useRef } from 'react'
import SourceCards from './SourceCards'
import ConfidenceBadge from './ConfidenceBadge'
import TypingIndicator from './TypingIndicator'

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null)

  // Auto-scroll to bottom on new message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-1">

      {/* Empty state */}
      {messages.length === 0 && !loading && (
        <div className="text-center text-gray-600 mt-20">
          <p className="text-4xl mb-3">⚖️</p>
          <p>Ask anything about Ayurveda IP &amp; regulations</p>
          <p className="text-sm mt-1 font-hindi">आयुर्वेद IP के बारे में कुछ भी पूछें</p>
        </div>
      )}

      {/* Messages */}
      {messages.map((msg, i) => (
        <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
          <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
            msg.role === 'user'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-100'
          }`}>
            <p className="whitespace-pre-wrap">{msg.content}</p>

            {/* Assistant extras */}
            {msg.role === 'assistant' && (
              <div className="mt-3 space-y-2">
                {msg.sources?.length > 0 && <SourceCards sources={msg.sources} />}
                {msg.confidence && <ConfidenceBadge level={msg.confidence} />}
                {msg.disclaimer && (
                  <p className="text-xs text-gray-500 mt-1">⚠️ {msg.disclaimer}</p>
                )}
              </div>
            )}
          </div>
        </div>
      ))}

      {/* Typing indicator */}
      {loading && <TypingIndicator />}

      <div ref={bottomRef} />
    </div>
  )
}
