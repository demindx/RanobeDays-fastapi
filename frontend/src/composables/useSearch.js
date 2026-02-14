import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useSearch = (initialValue = '') => {
  const router = useRouter()
  const query = ref(initialValue)

  const search = async (value = query.value) => {
    const normalized = String(value || '').trim()
    query.value = normalized

    const targetQuery = normalized ? { q: normalized } : {}
    const current = router.currentRoute.value
    const currentQuery = current.query?.q ? String(current.query.q) : ''

    if (current.path === '/catalog' && currentQuery === normalized) {
      return
    }

    await router.push({
      path: '/catalog',
      query: targetQuery,
    })
  }

  return {
    query,
    search,
  }
}
