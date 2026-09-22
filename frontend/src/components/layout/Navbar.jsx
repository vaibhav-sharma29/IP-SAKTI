/**
 * NAVBAR
 *
 * Dikhana hai:
 * - Left: "IP-SAKTI" logo/text
 * - Right: Nav links → Home | Chat | Classify
 * - Backend health status dot (green = online, red = offline)
 *   Call GET /api/health on mount to check
 */
import { NavLink, Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../../api/axiosInstance'

export default function Navbar() {
  const [online, setOnline] = useState(false)

  // Check backend health on mount and periodically every 30 seconds
  useEffect(() => {
    let isMounted = true

    const checkHealth = async () => {
      try {
        const res = await api.get('/api/health')
        if (isMounted) {
          setOnline(res.status === 200)
        }
      } catch (error) {
        if (isMounted) {
          setOnline(false)
        }
      }
    }

    checkHealth()
    const intervalId = setInterval(checkHealth, 30000)

    return () => {
      isMounted = false
      clearInterval(intervalId)
    }
  }, [])

  const navLinkClass = ({ isActive }) =>
    `px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
      isActive
        ? 'text-purple-400 bg-purple-500/10'
        : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
    }`

  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-gray-950/80 border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Left: Brand / Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center font-bold text-white shadow-lg shadow-purple-500/20 group-hover:opacity-90 transition">
            IP
          </div>
          <span className="text-xl font-bold tracking-tight text-white">
            IP-<span className="text-purple-400">SAKTI</span>
          </span>
        </Link>

        {/* Right: Navigation Links & Health Status */}
        <div className="flex items-center gap-2 sm:gap-6">
          <nav className="flex items-center gap-1 sm:gap-2">
            <NavLink to="/" className={navLinkClass}>
              Home
            </NavLink>
            <NavLink to="/chat" className={navLinkClass}>
              Chat
            </NavLink>
            <NavLink to="/classify" className={navLinkClass}>
              Classify
            </NavLink>
          </nav>

          <div className="h-4 w-px bg-gray-800 hidden sm:block" />

          {/* Backend health status dot */}
          <div
            className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-gray-900/90 border border-gray-800 text-xs text-gray-400"
            title={online ? 'Backend is reachable and healthy' : 'Backend is unreachable'}
          >
            <span className="relative flex h-2 w-2">
              {online && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              )}
              <span
                className={`relative inline-flex rounded-full h-2 w-2 ${
                  online ? 'bg-emerald-500' : 'bg-rose-500'
                }`}
              />
            </span>
            <span className="text-[11px] font-medium hidden sm:inline">
              {online ? 'Online' : 'Offline'}
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}
