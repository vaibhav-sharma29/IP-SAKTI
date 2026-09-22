/**
 * HOME PAGE
 *
 * Kya dikhana hai:
 * - IP-SAKTI ka hero section (logo + tagline)
 * - 2 main CTA buttons:
 *     1. "Ask IP Question" → /chat
 *     2. "Classify My Product" → /classify
 * - 3 feature cards:
 *     - Source-cited answers
 *     - Hindi + English
 *     - India & International laws
 * - "How it works" — 3 steps
 * - Footer with disclaimer
 *
 * NO API CALLS on this page — pure UI
 */

import { useNavigate } from 'react-router-dom'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="max-w-4xl mx-auto px-4 py-16 text-center">

      {/* Hero */}
      <h1 className="text-5xl font-bold mb-4">
        IP-<span className="text-purple-400">SAKTI</span>
      </h1>
      <p className="text-xl text-gray-400 mb-2">
        Intelligent IP & Regulatory Assistant for Ayurveda
      </p>
      <p className="text-gray-500 mb-10">
        आयुर्वेद के लिए IP मार्गदर्शन — हिंदी और अंग्रेजी में, स्रोत के साथ
      </p>

      {/* CTA Buttons */}
      <div className="flex gap-4 justify-center mb-16">
        <button
          onClick={() => navigate('/chat')}
          className="px-8 py-3 bg-purple-600 hover:bg-purple-700 rounded-xl font-semibold transition"
        >
          Ask IP Question
        </button>
        <button
          onClick={() => navigate('/classify')}
          className="px-8 py-3 border border-purple-600 hover:bg-purple-600/10 rounded-xl font-semibold transition"
        >
          Classify My Product
        </button>
      </div>

      {/* Feature Cards — 3 cards */}
      {/* TODO: Build FeatureCard component */}

      {/* How it works — 3 steps */}
      {/* TODO: Build StepsSection component */}

      {/* Disclaimer */}
      <p className="text-xs text-gray-600 mt-16">
        IP-SAKTI provides information only, not legal advice.
        Consult a qualified IP attorney for specific cases.
      </p>
    </div>
  )
}
