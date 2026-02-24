import { ref } from 'vue'
import { fetchHomeContinueReading } from '@/services/home'

export const useHomeContinueReading = () => {
  const items = ref([])
  const isLoading = ref(false)
  const error = ref('')

  const load = async (isLoggedIn) => {
    isLoading.value = true
    error.value = ''

    try {
      items.value = await fetchHomeContinueReading(isLoggedIn)
    } catch {
      items.value = []
      error.value = 'Не удалось загрузить прогресс чтения.'
    } finally {
      isLoading.value = false
    }
  }

  return {
    items,
    isLoading,
    error,
    load,
  }
}
