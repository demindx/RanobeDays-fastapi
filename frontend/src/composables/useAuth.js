import { computed, reactive, ref } from 'vue'

const AUTH_KEY = 'ranobe-auth'

const state = reactive({
  isAuthenticated: false,
  user: null,
  hasUnreadNotifications: false,
})

const isAuthModalOpen = ref(false)

const mockCredentials = {
  login: 'demo',
  password: 'demo123',
}

const saveState = () => {
  if (typeof window === 'undefined') return
  window.localStorage.setItem(
    AUTH_KEY,
    JSON.stringify({
      isAuthenticated: state.isAuthenticated,
      user: state.user,
      hasUnreadNotifications: state.hasUnreadNotifications,
    }),
  )
}

const restoreState = () => {
  if (typeof window === 'undefined') return
  const saved = window.localStorage.getItem(AUTH_KEY)
  if (!saved) return
  try {
    const parsed = JSON.parse(saved)
    state.isAuthenticated = !!parsed?.isAuthenticated
    state.hasUnreadNotifications = !!parsed?.hasUnreadNotifications
    if (parsed?.user) {
      state.user = {
        ...parsed.user,
        avatarUrl: parsed.user.avatarUrl || null,
        email: parsed.user.email || 'demo@example.com',
        settings: {
          blacklistedGenres: parsed.user.settings?.blacklistedGenres || [],
          blacklistedTags: parsed.user.settings?.blacklistedTags || [],
          hideAdultContent: parsed.user.settings?.hideAdultContent || false,
        },
      }
    } else {
      state.user = null
    }
  } catch {
    state.isAuthenticated = false
    state.user = null
    state.hasUnreadNotifications = false
  }
}

restoreState()

const login = (loginValue, passwordValue) => {
  const loginNormalized = loginValue.trim()
  if (loginNormalized !== mockCredentials.login || passwordValue !== mockCredentials.password) {
    return {
      ok: false,
      error: `Неверный логин или пароль. Тестовые данные: ${mockCredentials.login} / ${mockCredentials.password}`,
    }
  }

  state.isAuthenticated = true
  state.user = {
    login: state.user?.login || 'DemoReader',
    avatarUrl: state.user?.avatarUrl || null,
    email: state.user?.email || 'demo@example.com',
    settings: state.user?.settings || {
      blacklistedGenres: [],
      blacklistedTags: [],
      hideAdultContent: false,
    },
  }
  state.hasUnreadNotifications = true
  saveState()

  return { ok: true }
}

const logout = () => {
  state.isAuthenticated = false
  state.user = null
  state.hasUnreadNotifications = false
  saveState()
}

const updateUser = (partial) => {
  if (!state.user) return
  Object.assign(state.user, partial)
  saveState()
}

export const useAuth = () => ({
  isAuthenticated: computed(() => state.isAuthenticated),
  user: computed(() => state.user),
  hasUnreadNotifications: computed(() => state.hasUnreadNotifications),
  isAuthModalOpen,
  mockCredentials,
  login,
  logout,
  updateUser,
})
