/**
 * CLASSIFY FORM — Step-by-step wizard
 *
 * Props:
 * - onSubmit: function(formData) — called with final form data
 * - loading: boolean
 * - error: string | null
 *
 * Steps:
 * 1. Product description (textarea)
 * 2. Q1: Classical text reference? (Yes/No buttons)
 * 3. Q2: Novel process? (Yes/No buttons)
 * 4. Q3: Health claims? (Yes/No buttons)
 * 5. Q4: Topical/cosmetic? (Yes/No buttons)
 * 6. Submit → calls onSubmit with all answers
 *
 * Show progress bar at top (step 1/5, 2/5 etc.)
 */
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
  const [step, setStep]             = useState(0)  // 0 = description, 1-4 = questions
  const [description, setDescription] = useState('')
  const [answers, setAnswers]       = useState({})

  const totalSteps = QUESTIONS.length + 1  // +1 for description step

  const handleAnswer = (key, val) => {
    const updated = { ...answers, [key]: val }
    setAnswers(updated)

    if (step < totalSteps - 1) {
      setStep(step + 1)
    } else {
      // All questions answered — submit
      onSubmit({
        description,
        language: 'en',
        ...updated
      })
    }
  }

  return (
    <div>
      {/* Progress bar */}
      <div className="w-full bg-gray-800 rounded-full h-2 mb-8">
        <div
          className="bg-purple-600 h-2 rounded-full transition-all"
          style={{ width: `${((step) / totalSteps) * 100}%` }}
        />
      </div>

      {/* Step 0: Description */}
      {step === 0 && (
        <div>
          <label className="block text-lg font-medium mb-3">
            Describe your Ayurvedic product
          </label>
          <textarea
            rows={4}
            value={description}
            onChange={e => setDescription(e.target.value)}
            placeholder="e.g. An Ashwagandha + Brahmi formulation for cognitive support..."
            className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3
                       text-gray-100 placeholder-gray-500 resize-none
                       focus:outline-none focus:border-purple-500"
          />
          <button
            onClick={() => description.trim() && setStep(1)}
            disabled={!description.trim()}
            className="mt-4 px-6 py-2 bg-purple-600 hover:bg-purple-700
                       disabled:opacity-40 rounded-xl transition"
          >
            Next →
          </button>
        </div>
      )}

      {/* Steps 1-4: Yes/No questions */}
      {step >= 1 && step <= QUESTIONS.length && (() => {
        const q = QUESTIONS[step - 1]
        return (
          <div>
            <p className="text-lg font-medium mb-1">{q.question}</p>
            <p className="text-gray-500 text-sm mb-1">{q.hint}</p>
            <p className="text-gray-600 text-sm font-hindi mb-6">{q.hindi}</p>
            <div className="flex gap-4">
              <button
                onClick={() => handleAnswer(q.key, true)}
                className="flex-1 py-3 bg-green-700 hover:bg-green-600 rounded-xl font-semibold transition"
              >
                ✅ Yes
              </button>
              <button
                onClick={() => handleAnswer(q.key, false)}
                className="flex-1 py-3 bg-gray-700 hover:bg-gray-600 rounded-xl font-semibold transition"
              >
                ❌ No
              </button>
            </div>
          </div>
        )
      })()}

      {/* Loading */}
      {loading && (
        <p className="text-gray-400 mt-6 text-center animate-pulse">
          Analyzing your product...
        </p>
      )}

      {/* Error */}
      {error && (
        <p className="text-red-400 mt-4 text-center">{error}</p>
      )}
    </div>
  )
}
