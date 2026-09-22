/**
 * HOME PAGE
 *
 * Requirements met:
 * - IP-SAKTI hero section (logo + tagline + Hindi subtitle)
 * - 2 main CTA buttons: "Ask IP Question" -> /chat, "Classify My Product" -> /classify
 * - 3 feature cards: Source-cited answers, Hindi + English, India & International laws
 * - "How it works" — 3 steps
 * - Footer with legal disclaimer
 *
 * Pure UI Component (No API calls)
 */

import { useNavigate } from 'react-router-dom'
import { MessageSquare, FileText, Globe2, BookOpenCheck, ShieldAlert, ChevronRight } from 'lucide-react'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 md:py-16 text-center space-y-16 animate-fadeIn">

      {/* Hero Section */}
      <div className="space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-purple-950/60 border border-purple-800/50 text-purple-300 text-xs font-semibold uppercase tracking-widest mb-2">
          ✨ AI-Powered Ayurveda IP Intelligence
        </div>

        <h1 className="text-5xl md:text-6xl font-black tracking-tight text-gray-100">
          IP-<span className="bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent">SAKTI</span>
        </h1>

        <p className="text-xl md:text-2xl font-medium text-gray-300">
          Intelligent IP &amp; Regulatory Assistant for Ayurveda
        </p>

        <p className="text-gray-400 text-sm md:text-base font-medium">
          आयुर्वेद के लिए IP मार्गदर्शन — हिंदी और अंग्रेजी में, स्रोत के साथ
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-6">
          <button
            onClick={() => navigate('/chat')}
            className="w-full sm:w-auto px-8 py-3.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-semibold rounded-xl shadow-lg shadow-purple-600/30 transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer active:scale-95"
          >
            <MessageSquare className="w-5 h-5" />
            <span>Ask IP Question</span>
            <ChevronRight className="w-4 h-4 ml-1" />
          </button>

          <button
            onClick={() => navigate('/classify')}
            className="w-full sm:w-auto px-8 py-3.5 bg-gray-900 hover:bg-gray-800 border border-purple-600/60 hover:border-purple-500 text-gray-200 hover:text-white font-semibold rounded-xl transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer active:scale-95 shadow-md"
          >
            <FileText className="w-5 h-5 text-purple-400" />
            <span>Classify My Product</span>
          </button>
        </div>
      </div>

      {/* Feature Cards — 3 Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4 text-left">
        {/* Card 1 */}
        <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-6 backdrop-blur-md shadow-xl hover:border-purple-600/40 transition-all duration-200 group">
          <div className="w-12 h-12 rounded-xl bg-purple-950/80 border border-purple-800/50 flex items-center justify-center text-purple-400 mb-4 group-hover:scale-105 transition-transform">
            <BookOpenCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-gray-100 mb-2">Source-Cited Answers</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Every response cites official legal databases, Indian Patent Act clauses, and classical Ayurveda references.
          </p>
        </div>

        {/* Card 2 */}
        <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-6 backdrop-blur-md shadow-xl hover:border-purple-600/40 transition-all duration-200 group">
          <div className="w-12 h-12 rounded-xl bg-purple-950/80 border border-purple-800/50 flex items-center justify-center text-purple-400 mb-4 group-hover:scale-105 transition-transform">
            <span className="text-xl font-bold">अ/A</span>
          </div>
          <h3 className="text-lg font-bold text-gray-100 mb-2">Bilingual Support</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Seamlessly toggle between English and Hindi for prompts, explanations, and regulatory terminology.
          </p>
        </div>

        {/* Card 3 */}
        <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-6 backdrop-blur-md shadow-xl hover:border-purple-600/40 transition-all duration-200 group">
          <div className="w-12 h-12 rounded-xl bg-purple-950/80 border border-purple-800/50 flex items-center justify-center text-purple-400 mb-4 group-hover:scale-105 transition-transform">
            <Globe2 className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-gray-100 mb-2">India &amp; Global Laws</h3>
          <p className="text-sm text-gray-400 leading-relaxed">
            Covers Indian Patents Act, TKDL guidelines, NBA regulations, as well as US &amp; EU international IP norms.
          </p>
        </div>
      </div>

      {/* How It Works — 3 Steps */}
      <div className="bg-gray-900/50 border border-gray-800/80 rounded-2xl p-8 backdrop-blur-sm text-left space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-2xl font-bold text-gray-100">How IP-SAKTI Works</h2>
          <p className="text-sm text-gray-400">3 simple steps to get legal clarity for your Ayurvedic formulation</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* Step 1 */}
          <div className="flex flex-col items-center text-center space-y-3">
            <div className="w-10 h-10 rounded-full bg-purple-600 text-white font-bold flex items-center justify-center text-lg shadow-lg shadow-purple-600/30">
              1
            </div>
            <h4 className="font-semibold text-gray-200">Select Mode</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Choose between interactive Q&amp;A chat or step-by-step product classification wizard.
            </p>
          </div>

          {/* Step 2 */}
          <div className="flex flex-col items-center text-center space-y-3">
            <div className="w-10 h-10 rounded-full bg-purple-600 text-white font-bold flex items-center justify-center text-lg shadow-lg shadow-purple-600/30">
              2
            </div>
            <h4 className="font-semibold text-gray-200">Provide Details</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Describe your ingredients, novel processes, classical references, or legal queries.
            </p>
          </div>

          {/* Step 3 */}
          <div className="flex flex-col items-center text-center space-y-3">
            <div className="w-10 h-10 rounded-full bg-purple-600 text-white font-bold flex items-center justify-center text-lg shadow-lg shadow-purple-600/30">
              3
            </div>
            <h4 className="font-semibold text-gray-200">Get Actionable IP Insights</h4>
            <p className="text-xs text-gray-400 leading-relaxed">
              Receive clear guidance on patentability, regulatory tracks, and source citations.
            </p>
          </div>
        </div>
      </div>

      {/* Footer Disclaimer */}
      <div className="pt-8 border-t border-gray-800/60 text-center">
        <p className="text-xs text-gray-500 max-w-2xl mx-auto flex items-center justify-center gap-1.5 leading-relaxed">
          <ShieldAlert className="w-4 h-4 text-amber-500 flex-shrink-0" />
          <span>
            IP-SAKTI provides informational guidance based on public regulations, not legal advice. Consult a qualified IP attorney for official patent filings.
          </span>
        </p>
      </div>

    </div>
  )
}