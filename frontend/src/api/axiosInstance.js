/**
 * Axios base instance
 * Sab API calls yahan se jaati hain
 * Base URL .env.local se aati hai
 */
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
  timeout: 120000, // 2 minutes — RAG + Gemini needs time
})

export default api
