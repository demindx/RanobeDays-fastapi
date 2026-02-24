import { ref } from 'vue'
import { fetchHomeNewChaptersToday } from '@/services/home'

export const useHomeNewChapters = () => {
  const items = ref([])
  const isLoading = ref(false)
  const error = ref('')

  const load = async () => {
    isLoading.value = true
    error.value = ''

    try {
      items.value = await fetchHomeNewChaptersToday()
    } catch {
      items.value = []
      error.value = 'Не удалось загрузить новые главы.'
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
