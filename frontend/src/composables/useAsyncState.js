import { ref } from 'vue'

export function useAsyncState() {
  const loading = ref(false)
  const error = ref(null)
  let latestRunId = 0

  const run = async (fn) => {
    const runId = ++latestRunId
    loading.value = true
    error.value = null
    try {
      const result = await fn()
      return runId === latestRunId ? result : null
    } catch (err) {
      if (runId === latestRunId) {
        error.value = err?.message || 'Произошла ошибка'
      }
      return null
    } finally {
      if (runId === latestRunId) {
        loading.value = false
      }
    }
  }

  return { loading, error, run }
}
