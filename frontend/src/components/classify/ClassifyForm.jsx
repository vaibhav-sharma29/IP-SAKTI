import { useState } from 'react'

const QUESTIONS = [
  {
    key: 'has_classical_ref',
    question: 'Is your formula mentioned in any classical Ayurvedic text?',
    hint: 'e.g. Charaka Samhita, Sushruta Samhita, Ashtanga Hridayam',
    hindi: 'क्या आपका फॉर्मूला किसी शास्त्रीय आयुर्वेदिक ग्रंथ में है?'
  },
  {
    key: 'has_novel_process',
    question: 'Does your product involve a novel extraction or manufacturing process?',
    hint: 'A new method not previously documented',
    hindi: 'क्या इसमें कोई नई निष्कर्षण या निर्माण प्रक्रिया है?'
  },
  {
    key: 'has_health_claim',
    question: 'Does your product make any health or nutrition claims?',
    hint: 'e.g. "boosts immunity", "supports digestion"',
    hindi: 'क्या यह उत्पाद स्वास्थ्य या पोषण संबंधी दावे करता है?'
  },
  {
    key: 'is_topical',
    question: 'Is your product applied on skin or hair?',
    hint: 'Creams, oils, face packs, shampoos etc.',
    hindi: 'क्या यह उत्पाद त्वचा या बालों पर लगाया जाता है?'
  },
]

export default function ClassifyForm({ onSubmit, loading, error }) {
  const [step, setStep] = useState(0)  // 0 = description, 1-4 = questions
  const [description, setDescription] = useState('')
  const [answers, setAnswers] = useState({})

  const totalSteps = QUESTIONS.length + 1  // 5 total steps
  const progressPercent = Math.min(((step + 1) / totalSteps) * 100, 100)

  const handleAnswer = (key, val) => {
    const updated = { ...answers, [key]: val }
    setAnswers(updated)

    if (step < totalSteps - 1) {
      setStep(step + 1)
    } else {
      // Final submission when all questions are answered
      onSubmit({
        description,
        language: 'en',
        ...updated
      })
    }
  }

  const handleBack = () => {
    if (step > 0 && !loading) {
      setStep(step - 1)
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto bg-gray-900/90 border border-gray-800 backdrop-blur-xl rounded-2xl p-6 md:p-8 shadow-2xl transition-all">
      
      {/* Header & Step Counter */}
      <div className="flex items-center justify-between mb-3 text-sm">
        <span className="font-semibold text-purple-400 uppercase tracking-wider text-xs">
          Classification Wizard
        </span>
        <span className="text-gray-400 font-medium">
          Step <span className="text-purple-400 font-bold">{step + 1}</span> of {totalSteps}
        </span>
      </div>

      {/* Modern Progress Bar */}
      <div className="w-full bg-gray-800/80 rounded-full h-2.5 mb-8 overflow-hidden p-0.5 border border-gray-700/50">
        <div
          className="bg-gradient-to-r from-purple-600 via-indigo-500 to-amber-500 h-1.5 rounded-full transition-all duration-500 ease-out shadow-sm"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {/* Step 0: Product Description */}
      {step === 0 && (
        <div className="space-y-5 animate-fadeIn">
          <div>
            <h2 className="text-xl font-bold text-gray-100 mb-1">
              Describe your Ayurvedic Product
            </h2>
            <p className="text-gray-400 text-sm">
              Provide a clear overview of ingredients, purpose, or preparation details.
            </p>
          </div>

          <textarea
            rows={5}
            value={description}
            onChange={e => setDescription(e.target.value)}
            placeholder="e.g. An Ashwagandha + Brahmi oral syrup intended for stress relief and cognitive enhancement..."
            className="w-full bg-gray-800/80 border border-gray-700 focus:border-purple-500 rounded-xl p-4 text-gray-100 placeholder-gray-500 focus:ring-2 focus:ring-purple-500/20 focus:outline-none resize-none transition-all duration-200 text-base"
          />

          <div className="flex justify-end pt-2">
            <button
              onClick={() => description.trim() && setStep(1)}
              disabled={!description.trim() || loading}
              className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-200 shadow-lg shadow-purple-600/25 flex items-center gap-2 cursor-pointer"
            >
              Continue <span>→</span>
            </button>
          </div>
        </div>
      )}

      {/* Steps 1-4: Questions Wizard */}
      {step >= 1 && step <= QUESTIONS.length && (() => {
        const q = QUESTIONS[step - 1]
        return (
          <div className="space-y-6 animate-fadeIn">
            <div>
              <span className="inline-block px-3 py-1 bg-purple-950/60 border border-purple-800/50 text-purple-300 text-xs font-semibold rounded-full mb-3">
                Question {step}
              </span>
              <h3 className="text-xl font-bold text-gray-100 mb-2 leading-snug">
                {q.question}
              </h3>
              <p className="text-gray-400 text-sm mb-1">{q.hint}</p>
              <p className="text-amber-400/90 text-sm italic font-sans">{q.hindi}</p>
            </div>

            {/* Answer Options */}
            <div className="grid grid-cols-2 gap-4 pt-2">
              <button
                type="button"
                onClick={() => handleAnswer(q.key, true)}
                disabled={loading}
                className="group py-4 px-6 bg-gray-800/80 hover:bg-emerald-950/40 border border-gray-700/80 hover:border-emerald-500/60 rounded-xl font-semibold text-gray-200 hover:text-emerald-300 transition-all duration-200 flex flex-col items-center justify-center gap-1 cursor-pointer shadow-md active:scale-[0.98]"
              >
                <span className="text-2xl group-hover:scale-110 transition-transform">✅</span>
                <span>Yes</span>
              </button>

              <button
                type="button"
                onClick={() => handleAnswer(q.key, false)}
                disabled={loading}
                className="group py-4 px-6 bg-gray-800/80 hover:bg-rose-950/40 border border-gray-700/80 hover:border-rose-500/60 rounded-xl font-semibold text-gray-200 hover:text-rose-300 transition-all duration-200 flex flex-col items-center justify-center gap-1 cursor-pointer shadow-md active:scale-[0.98]"
              >
                <span className="text-2xl group-hover:scale-110 transition-transform">❌</span>
                <span>No</span>
              </button>
            </div>

            {/* Back Navigation */}
            <div className="pt-4 border-t border-gray-800 flex justify-between items-center">
              <button
                type="button"
                onClick={handleBack}
                disabled={loading}
                className="text-gray-400 hover:text-gray-200 text-sm font-medium transition flex items-center gap-1 cursor-pointer disabled:opacity-30"
              >
                ← Back
              </button>
            </div>
          </div>
        )
      })()}

      {/* Loading Indicator */}
      {loading && (
        <div className="mt-6 p-4 bg-purple-950/30 border border-purple-800/40 rounded-xl flex items-center justify-center gap-3">
          <div className="w-5 h-5 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
          <p className="text-purple-300 text-sm font-medium animate-pulse">
            Analyzing regulatory rules and classifying product...
          </p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="mt-6 p-4 bg-red-950/40 border border-red-800/60 rounded-xl text-red-300 text-sm text-center">
          ⚠️ {error}
        </div>
      )}
    </div>
  )
}