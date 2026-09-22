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

export default function ChatWindow({ messages = [], loading = false }) {
  const bottomRef = useRef(null)

  // Auto-scroll to bottom on new message or typing state change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="flex-1 overflow-y-auto space-y-6 p-4 rounded-2xl bg-gray-950/50 border border-gray-800/60 backdrop-blur-md min-h-[400px] max-h-[calc(100vh-220px)] scrollbar-thin scrollbar-thumb-gray-800">

      {/* Empty State */}
      {messages.length === 0 && !loading && (
        <div className="h-full min-h-[300px] flex flex-col items-center justify-center text-center p-6 space-y-3 my-auto animate-fadeIn">
          <div className="w-16 h-16 rounded-2xl bg-purple-950/50 border border-purple-800/40 flex items-center justify-center text-3xl shadow-xl shadow-purple-900/20">
            ⚖️
          </div>
          <h3 className="text-xl font-bold text-gray-200">
            Ask anything about Ayurveda IP &amp; Regulations
          </h3>
          <p className="text-sm text-purple-400 font-medium italic">
            आयुर्वेद IP, पेटेंट और नियमों के बारे में कुछ भी पूछें
          </p>
          <div className="flex flex-wrap justify-center gap-2 mt-4 text-xs text-gray-400">
            <span className="px-3 py-1.5 bg-gray-900 border border-gray-800 rounded-full">
              💡 Patenting Traditional Knowledge
            </span>
            <span className="px-3 py-1.5 bg-gray-900 border border-gray-800 rounded-full">
              📜 TKDL Compliance
            </span>
            <span className="px-3 py-1.5 bg-gray-900 border border-gray-800 rounded-full">
              🌿 Biodiversity Clearance
            </span>
          </div>
        </div>
      )}

      {/* Message List */}
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`flex flex-col ${
            msg.role === 'user' ? 'items-end' : 'items-start'
          } animate-fadeIn`}
        >
          {/* Main Bubble */}
          <div
            className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-3.5 shadow-lg leading-relaxed text-sm sm:text-base ${
              msg.role === 'user'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-br-none font-medium'
                : 'bg-gray-800/90 border border-gray-700/70 text-gray-100 rounded-bl-none shadow-black/20'
            }`}
          >
            <p className="whitespace-pre-wrap">{msg.content}</p>

            {/* Assistant Specific Extra Widgets */}
            {msg.role === 'assistant' && (
              <div className="mt-4 pt-3 border-t border-gray-700/60 space-y-3">
                
                {/* Confidence Badge */}
                {msg.confidence && (
                  <div className="flex items-center gap-2">
                    <ConfidenceBadge level={msg.confidence} />
                  </div>
                )}

                {/* Source Cards */}
                {msg.sources && msg.sources.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
                      Cited References
                    </p>
                    <SourceCards sources={msg.sources} />
                  </div>
                )}

                {/* Disclaimer */}
                {msg.disclaimer && (
                  <p className="text-[11px] text-amber-400/80 bg-amber-950/20 border border-amber-800/30 rounded-lg p-2 leading-tight">
                    ⚠️ <span className="font-medium">Disclaimer:</span> {msg.disclaimer}
                  </p>
                )}

              </div>
            )}
          </div>
        </div>
      ))}

      {/* Typing Indicator While Waiting for Response */}
      {loading && (
        <div className="flex justify-start animate-fadeIn">
          <TypingIndicator />
        </div>
      )}

      {/* Dummy div to anchor auto-scrolling */}
      <div ref={bottomRef} />
    </div>
  )
}