/**
 * CHAT PAGE — Main feature page
 *
 * Layout:
 * ┌─────────────────────────────────────────┐
 * │  Jurisdiction Toggle  [🇮🇳 India] [🌍 Intl] │
 * │  Language Toggle      [EN] [HI]          │
 * ├─────────────────────────────────────────┤
 * │                                         │
 * │   Chat messages area (scrollable)       │
 * │   - User messages (right aligned)       │
 * │   - AI messages (left aligned)          │
 * │     with source citation cards below    │
 * │     and confidence badge                │
 * │                                         │
 * ├─────────────────────────────────────────┤
 * │  [ Type your question here...      ] 📤 │
 * └─────────────────────────────────────────┘
 *
 * API CONTRACT — POST /api/chat
 *
 * REQUEST body (send this to backend):
 * {
 *   "query":        string,   ← user ka message
 *   "language":     "en"|"hi",
 *   "jurisdiction": "india"|"international"|"both",
 *   "session_id":   string    ← use "default" for now
 * }
 *
 * RESPONSE from backend:
 * {
 *   "answer":       string,   ← AI ka jawab (show in chat bubble)
 *   "sources": [              ← Show as cards below the answer
 *     {
 *       "title":   string,    ← e.g. "Patents Act 1970"
 *       "section": string,    ← e.g. "Section 3(p)"
 *       "url":     string     ← link to official doc
 *     }
 *   ],
 *   "confidence":  "high"|"medium"|"low",  ← show as colored badge
 *   "disclaimer":  string,    ← show in small text below answer
 *   "jurisdiction": string
 * }
 *
 * LOADING STATE:
 * Show a typing animation while waiting for API response.
 *
 * ERROR STATE:
 * Show "Something went wrong. Please try again." in red.
 */

import { useState } from 'react'
import ChatWindow from '../components/chat/ChatWindow'
import ChatInput from '../components/chat/ChatInput'
import JurisdictionToggle from '../components/ui/JurisdictionToggle'
import LanguageToggle from '../components/ui/LanguageToggle'
import { sendChatMessage } from '../api/chatApi'

export default function ChatPage() {
  const [messages, setMessages]       = useState([])
  const [language, setLanguage]       = useState('en')
  const [jurisdiction, setJurisdiction] = useState('india')
  const [loading, setLoading]         = useState(false)

  const handleSend = async (query) => {
    if (!query.trim()) return

    // Add user message to chat
    const userMsg = { role: 'user', content: query }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)

    try {
      // Call backend API
      const response = await sendChatMessage({
        query,
        language,
        jurisdiction,
        session_id: 'default'
      })

      // Add AI response to chat
      const aiMsg = {
        role: 'assistant',
        content:    response.answer,
        sources:    response.sources,
        confidence: response.confidence,
        disclaimer: response.disclaimer
      }
      setMessages(prev => [...prev, aiMsg])

    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Something went wrong. Please try again.',
        sources: [],
        confidence: 'low',
        disclaimer: ''
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-6 flex flex-col h-[90vh]">

      {/* Top Controls */}
      <div className="flex justify-between items-center mb-4">
        <JurisdictionToggle value={jurisdiction} onChange={setJurisdiction} />
        <LanguageToggle value={language} onChange={setLanguage} />
      </div>

      {/* Chat messages */}
      <ChatWindow messages={messages} loading={loading} />

      {/* Input box */}
      <ChatInput onSend={handleSend} loading={loading} language={language} />
    </div>
  )
}
