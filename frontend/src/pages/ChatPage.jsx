/**
 * CHAT PAGE — Main feature page
 *
 * API CONTRACT MATCHED — POST /api/chat
 * Payload sent: { query, language, jurisdiction, session_id: 'default' }
 * Response mapped: response.answer, response.sources, response.confidence, response.disclaimer
 */

import { useState } from 'react'
import ChatWindow from '../components/chat/ChatWindow'
import ChatInput from '../components/chat/ChatInput'
import JurisdictionToggle from '../components/ui/JurisdictionToggle'
import LanguageToggle from '../components/ui/LanguageToggle'
import { sendChatMessage } from '../api/chatApi'

export default function ChatPage() {
  const [messages, setMessages] = useState([])
  const [language, setLanguage] = useState('en')
  const [jurisdiction, setJurisdiction] = useState('india')
  const [loading, setLoading] = useState(false)

  const handleSend = async (query) => {
    if (!query.trim()) return

    // 1. Add user message
    const userMsg = { role: 'user', content: query }
    setMessages(prev => [...prev, userMsg])
    setLoading(true)

    try {
      // 2. Call backend API with precise contract payload
      const response = await sendChatMessage({
        query,
        language,
        jurisdiction,
        session_id: 'default'
      })

      // 3. Map backend response values to chat assistant bubble
      const aiMsg = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources || [],
        confidence: response.confidence || 'medium',
        disclaimer: response.disclaimer || ''
      }
      setMessages(prev => [...prev, aiMsg])

    } catch (err) {
      // Error state fallback
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Something went wrong. Please try again.',
        sources: [],
        confidence: 'low',
        disclaimer: err?.message || 'Server response failed.'
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-4 flex flex-col h-[calc(100vh-80px)] space-y-4">

      {/* Top Header Controls Bar */}
      <div className="flex flex-wrap justify-between items-center gap-3 bg-gray-900/80 border border-gray-800 rounded-2xl p-3 shadow-md backdrop-blur-md">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-xs font-semibold uppercase tracking-wider text-purple-300">
            IP Assistant Chat
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <JurisdictionToggle value={jurisdiction} onChange={setJurisdiction} />
          <LanguageToggle value={language} onChange={setLanguage} />
        </div>
      </div>

      {/* Main Chat Stream Container */}
      <div className="flex-1 min-h-0 flex flex-col">
        <ChatWindow messages={messages} loading={loading} />
      </div>

      {/* Bottom Sticky Input */}
      <div className="pt-1">
        <ChatInput onSend={handleSend} loading={loading} language={language} />
      </div>

    </div>
  )
}