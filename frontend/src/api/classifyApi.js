/**
 * Classify API — POST /api/classify
 *
 * Used by: ClassifyPage.jsx
 */
import api from './axiosInstance'

/**
 * Classify an Ayurvedic product
 *
 * @param {Object} payload
 * @param {string}  payload.description       - Product description
 * @param {boolean} payload.has_classical_ref - From classical text?
 * @param {boolean} payload.has_novel_process - Novel process?
 * @param {boolean} payload.has_health_claim  - Health claims?
 * @param {boolean} payload.is_topical        - Topical/cosmetic?
 * @param {string}  payload.language          - "en" | "hi"
 *
 * @returns {Promise<{
 *   category: string,
 *   ip_posture: string,
 *   regulatory_track: string,
 *   patent_possible: boolean,
 *   key_actions: string[],
 *   warning: string
 * }>}
 */
export async function classifyProduct(payload) {
  const response = await api.post('/api/classify', payload)
  return response.data
}

/**
 * AI Auto-detect — POST /api/classify/auto-detect
 * Reads product description and pre-fills the 4 questions.
 *
 * @param {string} description - Product description
 * @returns {Promise<{
 *   has_classical_ref: boolean,
 *   has_novel_process: boolean,
 *   has_health_claim: boolean,
 *   is_topical: boolean,
 *   reasoning: string
 * }>}
 */
export async function autoDetectClassification(description) {
  const response = await api.post('/api/classify/auto-detect', { description })
  return response.data
}
