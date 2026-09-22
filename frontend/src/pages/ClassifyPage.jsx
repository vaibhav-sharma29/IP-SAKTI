/**
 * CLASSIFY PAGE — Formulation Classifier
 *
 * API CONTRACT MATCHED — POST /api/classify
 * Request payload: { description, has_classical_ref, has_novel_process, has_health_claim, is_topical, language }
 * Response mapped: { category, ip_posture, regulatory_track, patent_possible, key_actions, warning }
 */

import { useState } from 'react'
import ClassifyForm from '../components/classify/ClassifyForm'
import ClassifyResult from '../components/classify/ClassifyResult'
import { classifyProduct } from '../api/classifyApi'

export default function ClassifyPage() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleClassify = async (formData) => {
    setLoading(true)
    setError(null)
    try {
      const response = await classifyProduct(formData)
      setResult(response)
    } catch (err) {
      setError(err?.message || 'Classification failed. Please check your network or try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 animate-fadeIn">
      
      {/* Header Banner */}
      <div className="text-center mb-8 space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-950/60 border border-purple-800/40 text-purple-300 text-xs font-semibold uppercase tracking-wider">
          🧪 Ayurvedic IP Formulation Classifier
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-100 tracking-tight">
          Classify Your Product
        </h1>
        <p className="text-gray-400 text-sm sm:text-base max-w-xl mx-auto">
          Answer 4 quick questions to evaluate patentability, regulatory tracks, and key legal steps.
        </p>
      </div>

      {/* Main Container Card */}
      <div className="bg-gray-900/80 border border-gray-800 rounded-2xl p-6 sm:p-8 backdrop-blur-md shadow-2xl">
        {!result ? (
          <ClassifyForm onSubmit={handleClassify} loading={loading} error={error} />
        ) : (
          <ClassifyResult result={result} onReset={() => setResult(null)} />
        )}
      </div>

    </div>
  )
}