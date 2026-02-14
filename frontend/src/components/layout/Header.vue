<template>
  <header class="w-full relative md:relative">
    <!-- Mobile sticky header -->
    <div
      class="md:hidden fixed top-0 left-0 right-0 z-50 bg-rd-surface shadow-md transition-transform duration-300"
      :class="{ '-translate-y-full': hideOnScroll && isScrollingDown }"
    >
      <div class="flex items-center justify-between h-[60px] px-4">
        <div class="flex-1">
          <SearchBar
            v-model="searchQuery"
            placeholder="Поиск"
            @search="handleSearch"
          />
        </div>
      </div>
    </div>

    <!-- Full-width background -->
    <div class="absolute inset-0 bg-rd-surface hidden md:block" />

    <!-- Main header content -->
    <div class="w-full h-[60px] flex items-center justify-between relative z-10">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-[1250px] w-full">
        <div class="flex items-center justify-between h-[60px]">
          <!-- Logo section - visible on desktop -->
          <div class="hidden md:flex items-center">
            <router-link
              to="/"
              aria-label="Открыть главную"
            >
              <Icon class="h-8 cursor-pointer" />
            </router-link>
          </div>

          <HeaderDesktopNav :nav-items="desktopNavItems" />

          <!-- Search bar - visible on desktop -->
          <div class="hidden md:flex flex-grow max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl mx-4">
            <SearchBar
              v-model="searchQuery"
              placeholder="Поиск"
              @search="handleSearch"
            />
          </div>

          <HeaderUserControls
            :is-logged-in="isLoggedIn"
            :has-notifications="hasNotifications"
            :user-initials="userInitials"
            :user-has-image="userProfile.hasImage"
            @login="handleLogin"
            @book-click="handleBookClick"
            @notifications-click="handleNotificationClick"
          />
        </div>
      </div>
    </div>

    <HeaderMobileNav
      :is-logged-in="isLoggedIn"
      :has-notifications="hasNotifications"
      :user-initials="userInitials"
      @notifications-click="handleNotificationClick"
    />
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import Icon from '@/components/icons/Icon.vue'
import SearchBar from '@/components/common/SearchBar.vue'
import HeaderDesktopNav from '@/components/layout/HeaderDesktopNav.vue'
import HeaderUserControls from '@/components/layout/HeaderUserControls.vue'
import HeaderMobileNav from '@/components/layout/HeaderMobileNav.vue'
import { useSearch } from '@/composables/useSearch'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
const router = useRouter()
const { isLoggedIn, hasNotifications, userProfile, userInitials } = storeToRefs(appStore)
const { login, markNotificationsRead } = appStore
const { query: searchQuery, search } = useSearch()

const lastScrollY = ref(0)
const isScrollingDown = ref(false)
const hideOnScroll = ref(true)

const handleScroll = () => {
  const currentScrollY = window.scrollY

  if (currentScrollY > lastScrollY.value && currentScrollY > 60) {
    isScrollingDown.value = true
  } else {
    isScrollingDown.value = false
  }

  lastScrollY.value = currentScrollY
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const navItems = [
  { name: 'Главная', to: '/' },
  { name: 'Каталог', to: '/catalog' },
  { name: 'Уведомления', to: '/notifications' },
  { name: 'Топ', to: '/top' },
  { name: 'Профиль', to: '/profile' },
]
const desktopNavItems = [navItems[0], navItems[1], navItems[3]]

const handleSearch = (value) => {
  void search(value)
}

const handleLogin = () => {
  login()
}

const handleBookClick = () => {
  void router.push('/favorites')
}

const handleNotificationClick = () => {
  markNotificationsRead()
}
</script>
