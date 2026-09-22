/**
 * CLASSIFY PAGE — Formulation Classifier
 *
 * Layout: Step-by-step form (wizard style)
 *
 * STEP 1: Product description text input
 * STEP 2: 4 Yes/No questions:
 *   Q1: "Is your formula mentioned in any classical Ayurvedic text?
 *        (Charaka Samhita, Sushruta, Ashtanga Hridayam?)"
 *   Q2: "Does your product involve a novel extraction or manufacturing process?"
 *   Q3: "Does your product make any health or nutrition claims?"
 *   Q4: "Is your product applied on skin or hair? (topical use)"
 * STEP 3: Show result card
 *
 * API CONTRACT — POST /api/classify
 *
 * REQUEST body (send this to backend):
 * {
 *   "description":       string,   ← product description
 *   "has_classical_ref": boolean,  ← Q1 answer
 *   "has_novel_process": boolean,  ← Q2 answer
 *   "has_health_claim":  boolean,  ← Q3 answer
 *   "is_topical":        boolean,  ← Q4 answer
 *   "language":          "en"|"hi"
 * }
 *
 * RESPONSE from backend:
 * {
 *   "category":         string,   ← e.g. "Classical Medicine"
 *   "ip_posture":       string,   ← what IP protection is possible
 *   "regulatory_track": string,   ← which act/ministry governs it
 *   "patent_possible":  boolean,  ← show green tick or red cross
 *   "key_actions":      string[], ← numbered action list
 *   "warning":          string    ← show in yellow warning box if not empty
 * }
 *
 * RESULT CARD should show:
 * - Category badge (colored)
 * - Patent possible: ✅ Yes / ❌ No
 * - IP Posture text
 * - Regulatory track
 * - Key Actions as numbered list
 * - Warning box (yellow) if warning exists
 */

import { useState } from 'react'
import ClassifyForm from '../components/classify/ClassifyForm'
import ClassifyResult from '../components/classify/ClassifyResult'
import { classifyProduct } from '../api/classifyApi'

export default function ClassifyPage() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]   = useState(null)

  const handleClassify = async (formData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await classifyProduct(formData)
      setResult(response)
    } catch (err) {
      setError('Classification failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      <h2 className="text-3xl font-bold mb-2">Classify Your Product</h2>
      <p className="text-gray-400 mb-8">
        Answer 4 quick questions to understand your IP position.
      </p>

      {!result ? (
        <ClassifyForm onSubmit={handleClassify} loading={loading} error={error} />
      ) : (
        <ClassifyResult result={result} onReset={() => setResult(null)} />
      )}
    </div>
  )
}
