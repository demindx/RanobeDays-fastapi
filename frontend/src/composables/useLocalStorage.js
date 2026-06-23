import { ref, watch } from 'vue'

export function useLocalStorage(key, defaultValue) {
  let initial = defaultValue
  if (typeof window !== 'undefined') {
    try {
      const stored = window.localStorage.getItem(key)
      if (stored !== null) initial = JSON.parse(stored)
    } catch {}
  }

  const data = ref(initial)

  watch(
    data,
    (val) => {
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(val))
      }
    },
    { deep: true },
  )

  return data
}
