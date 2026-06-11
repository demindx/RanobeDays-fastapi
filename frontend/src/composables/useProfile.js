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

  const updateAvatarColor = (colorClass) => {
    updateUser({ avatarColorClass: colorClass })
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
    updateAvatarColor,
    openSettings,
    closeSettings,
  }
}
