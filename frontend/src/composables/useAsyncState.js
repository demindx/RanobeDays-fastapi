import { ref } from 'vue'

export function useAsyncState() {
  const loading = ref(false)
  const error = ref(null)

  const run = async (fn) => {
    loading.value = true
    error.value = null
    try {
      return await fn()
    } catch (err) {
      error.value = err?.message || 'Произошла ошибка'
      return null
    } finally {
      loading.value = false
    }
  }

  return { loading, error, run }
}
