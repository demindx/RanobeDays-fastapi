import { computed, reactive, ref } from 'vue'
import { loginUser, registerUser, logoutUser, fetchProfile } from '../api/auth'
import { hasAuthToken } from '../api/client'

const AUTH_KEY = 'ranobe-auth'

const state = reactive({
  isAuthenticated: false,
  user: null,
  hasUnreadNotifications: false,
})

const isAuthModalOpen = ref(false)

const clearState = () => {
  state.isAuthenticated = false
  state.user = null
  state.hasUnreadNotifications = false
}

const saveState = () => {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(
      AUTH_KEY,
      JSON.stringify({
        isAuthenticated: state.isAuthenticated,
        user: state.user,
        hasUnreadNotifications: state.hasUnreadNotifications,
      }),
    )
  } catch {
    // Authentication must still work when storage is unavailable.
  }
}

const restoreState = () => {
  if (typeof window === 'undefined') return
  try {
    const saved = window.localStorage.getItem(AUTH_KEY)
    if (!saved) return
    const parsed = JSON.parse(saved)
    if (!hasAuthToken()) {
      clearState()
      return
    }
    state.isAuthenticated = !!parsed?.isAuthenticated
    state.hasUnreadNotifications = !!parsed?.hasUnreadNotifications
    if (parsed?.user) {
      state.user = {
        ...parsed.user,
        avatarUrl: parsed.user.avatarUrl || null,
        email: parsed.user.email || '',
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
    clearState()
  }
}

restoreState()

const toUser = (profile) => {
  if (!profile) return null
  return {
    login: profile.user_profile?.nickname || profile.login || '',
    avatarUrl: profile.avatar_url || null,
    email: profile.email || '',
    settings: {
      blacklistedGenres: profile.settings?.blacklisted_genres || [],
      blacklistedTags: profile.settings?.blacklisted_tags || [],
      hideAdultContent: profile.settings?.hide_adult_content || false,
    },
  }
}

const login = async (loginValue, passwordValue) => {
  const loginNormalized = loginValue.trim()
  if (!loginNormalized || !passwordValue) {
    return { ok: false, error: 'Введите логин и пароль.' }
  }

  let sessionCreated = false
  try {
    await loginUser(loginNormalized, passwordValue)
    sessionCreated = true
    const profile = await fetchProfile()
    state.user = toUser(profile)
    state.isAuthenticated = true
    saveState()
    return { ok: true }
  } catch (err) {
    if (sessionCreated) {
      try {
        await logoutUser()
      } catch {
        // The local token is cleared by the API logout helper even if the request fails.
      }
    }
    clearState()
    saveState()
    if (err?.status === 0) return { ok: false, error: 'Не удалось подключиться к серверу.' }
    if (err?.status === 401 || err?.status === 404)
      return { ok: false, error: 'Неверный логин или пароль.' }
    return { ok: false, error: err?.message || 'Ошибка входа.' }
  }
}

const register = async (loginValue, emailValue, passwordValue) => {
  const loginNormalized = loginValue.trim()
  if (!loginNormalized || !emailValue || !passwordValue) {
    return { ok: false, error: 'Заполните все поля.' }
  }

  let sessionCreated = false
  try {
    await registerUser(loginNormalized, emailValue, passwordValue)
    sessionCreated = true
    const profile = await fetchProfile()
    state.user = toUser(profile)
    state.isAuthenticated = true
    saveState()
    return { ok: true }
  } catch (err) {
    if (sessionCreated) {
      try {
        await logoutUser()
      } catch {
        // The local token is cleared by the API logout helper even if the request fails.
      }
    }
    clearState()
    saveState()
    if (err?.status === 0) return { ok: false, error: 'Не удалось подключиться к серверу.' }
    return { ok: false, error: err?.message || 'Ошибка регистрации.' }
  }
}

const logout = async () => {
  try {
    await logoutUser()
  } catch {
    // Logging out locally must not depend on network availability.
  } finally {
    clearState()
    saveState()
  }
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
  login,
  register,
  logout,
  updateUser,
})
