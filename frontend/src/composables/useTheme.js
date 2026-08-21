import { computed, ref } from 'vue'

const THEME_KEY = 'ranobe-theme'
const theme = ref('dark')
let initialized = false

const applyTheme = (nextTheme) => {
  theme.value = nextTheme
  if (typeof document !== 'undefined') {
    document.documentElement.setAttribute('data-theme', nextTheme)
  }
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(THEME_KEY, nextTheme)
  }
}

const initTheme = () => {
  if (initialized || typeof window === 'undefined') return
  const savedTheme = window.localStorage.getItem(THEME_KEY)
  if (savedTheme === 'light' || savedTheme === 'dark') {
    applyTheme(savedTheme)
  } else {
    applyTheme('dark')
  }
  initialized = true
}

export const useTheme = () => {
  initTheme()
  const isDark = computed(() => theme.value === 'dark')
  const toggleTheme = () => applyTheme(isDark.value ? 'light' : 'dark')
  return { theme, isDark, toggleTheme, setTheme: applyTheme }
}
