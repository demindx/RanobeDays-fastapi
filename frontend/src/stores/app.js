import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  const isLoggedIn = ref(false)
  const hasNotifications = ref(true)
  const userProfile = ref({
    name: 'Александр',
    initials: 'А',
    hasImage: false,
  })

  const userInitials = computed(() => userProfile.value.initials || 'U')

  const login = () => {
    isLoggedIn.value = true
  }

  const logout = () => {
    isLoggedIn.value = false
  }

  const markNotificationsRead = () => {
    hasNotifications.value = false
  }

  return {
    isLoggedIn,
    hasNotifications,
    userProfile,
    userInitials,
    login,
    logout,
    markNotificationsRead,
  }
})
