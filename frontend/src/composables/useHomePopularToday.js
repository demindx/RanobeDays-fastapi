import { ref } from 'vue'
import { fetchHomePopularToday } from '@/services/home'

export const useHomePopularToday = () => {
  const items = ref([])
  const isLoading = ref(false)
  const error = ref('')

  const load = async () => {
    isLoading.value = true
    error.value = ''

    try {
      items.value = await fetchHomePopularToday()
    } catch {
      items.value = []
      error.value = 'Не удалось загрузить популярные новелы.'
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
