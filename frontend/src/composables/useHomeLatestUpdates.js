import { ref } from 'vue'
import { fetchHomeLatestUpdates } from '@/services/home'

export const useHomeLatestUpdates = () => {
  const items = ref([])
  const isLoading = ref(false)
  const error = ref('')

  const load = async () => {
    isLoading.value = true
    error.value = ''

    try {
      items.value = await fetchHomeLatestUpdates()
    } catch {
      items.value = []
      error.value = 'Не удалось загрузить последние обновления.'
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
