/**
 * Chat API — POST /api/chat
 *
 * Used by: ChatPage.jsx
 */
import api from './axiosInstance'

/**
 * Send a message to IP-SAKTI backend
 *
 * @param {Object} payload
 * @param {string} payload.query        - User ka sawaal
 * @param {string} payload.language     - "en" or "hi"
 * @param {string} payload.jurisdiction - "india" | "international" | "both"
 * @param {string} payload.session_id   - use "default"
 *
 * @returns {Promise<{
 *   answer: string,
 *   sources: Array<{title: string, section: string, url: string}>,
 *   confidence: "high"|"medium"|"low",
 *   disclaimer: string,
 *   jurisdiction: string
 * }>}
 */
export async function sendChatMessage(payload) {
  const response = await api.post('/api/chat', payload)
  return response.data
}
