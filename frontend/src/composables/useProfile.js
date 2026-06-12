import { computed, ref } from 'vue'
import { useAuth } from './useAuth'
import { profileUser, calendarData, userBookmarks, userComments } from '../mocks/profileData'

const calendar = ref(calendarData)
const bookmarks = ref(userBookmarks)
const comments = ref(userComments)
const isSettingsOpen = ref(false)

export function useProfile() {
  const { user: authUser, updateUser } = useAuth()

  const user = computed(() => {
    const auth = authUser.value
    if (!auth) return null
    return {
      ...auth,
      joinDate: profileUser.joinDate,
      stats: profileUser.stats,
      teams: profileUser.teams,
    }
  })

  const updateNickname = (nextName) => {
    const trimmed = nextName.trim()
    if (!trimmed) return { ok: false, error: 'Никнейм не может быть пустым.' }
    if (trimmed.length < 2) return { ok: false, error: 'Никнейм должен быть не короче 2 символов.' }
    if (trimmed.length > 24)
      return { ok: false, error: 'Никнейм должен быть не длиннее 24 символов.' }
    updateUser({ login: trimmed })
    return { ok: true }
  }

  const updateAvatar = (file) => {
    if (!file) {
      updateUser({ avatarUrl: null })
      return
    }
    const reader = new FileReader()
    reader.onload = () => {
      updateUser({ avatarUrl: reader.result })
    }
    reader.readAsDataURL(file)
  }

  const updateEmail = (newEmail) => {
    const trimmed = newEmail.trim()
    if (!trimmed) return { ok: false, error: 'Email не может быть пустым.' }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed))
      return { ok: false, error: 'Некорректный формат email.' }
    updateUser({ email: trimmed })
    return { ok: true }
  }

  const updatePassword = (currentPassword, newPassword) => {
    if (!currentPassword) return { ok: false, error: 'Введите текущий пароль.' }
    if (currentPassword !== 'demo123') return { ok: false, error: 'Неверный текущий пароль.' }
    if (!newPassword || newPassword.length < 6)
      return { ok: false, error: 'Новый пароль должен быть не короче 6 символов.' }
    return { ok: true }
  }

  const toggleGenreBlacklist = (genre) => {
    const settings = authUser.value.settings
    const list = settings.blacklistedGenres
    const idx = list.indexOf(genre)
    const next = idx === -1 ? [...list, genre] : list.filter((g) => g !== genre)
    updateUser({ settings: { ...settings, blacklistedGenres: next } })
  }

  const toggleTagBlacklist = (tag) => {
    const settings = authUser.value.settings
    const list = settings.blacklistedTags
    const idx = list.indexOf(tag)
    const next = idx === -1 ? [...list, tag] : list.filter((t) => t !== tag)
    updateUser({ settings: { ...settings, blacklistedTags: next } })
  }

  const toggleAdultContent = () => {
    const settings = authUser.value.settings
    updateUser({ settings: { ...settings, hideAdultContent: !settings.hideAdultContent } })
  }

  const openSettings = () => {
    isSettingsOpen.value = true
  }

  const closeSettings = () => {
    isSettingsOpen.value = false
  }

  return {
    user,
    calendar,
    bookmarks,
    comments,
    isSettingsOpen,
    updateNickname,
    updateAvatar,
    updateEmail,
    updatePassword,
    toggleGenreBlacklist,
    toggleTagBlacklist,
    toggleAdultContent,
    openSettings,
    closeSettings,
  }
}
