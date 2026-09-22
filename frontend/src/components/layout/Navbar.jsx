/**
 * NAVBAR
 *
 * Dikhana hai:
 * - Left: "IP-SAKTI" logo/text
 * - Right: Nav links → Home | Chat | Classify
 * - Backend health status dot (green = online, red = offline)
 *   Call GET /api/health on mount to check
 */
import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../../api/axiosInstance'

export default function Navbar() {
  const [online, setOnline] = useState(false)

  useEffect(() => {
    api.get('/api/health')
      .then(() => setOnline(true))
      .catch(() => setOnline(false))
  }, [])

  return (
    <nav className="border-b border-gray-800 px-6 py-4 flex justify-between items-center">
      <Link to="/" className="text-xl font-bold">
        IP-<span className="text-purple-400">SAKTI</span>
      </Link>

      <div className="flex items-center gap-6">
        <Link to="/"         className="text-gray-400 hover:text-white transition">Home</Link>
        <Link to="/chat"     className="text-gray-400 hover:text-white transition">Chat</Link>
        <Link to="/classify" className="text-gray-400 hover:text-white transition">Classify</Link>

        {/* Health dot */}
        <span className="flex items-center gap-1 text-xs text-gray-500">
          <span className={`w-2 h-2 rounded-full ${online ? 'bg-green-400' : 'bg-red-500'}`} />
          {online ? 'Backend Online' : 'Backend Offline'}
        </span>
      </div>
    </nav>
  )
}
