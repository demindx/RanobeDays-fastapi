<template>
  <header class="w-full relative md:relative">
    <!-- Mobile sticky header -->
    <div
      class="md:hidden fixed top-0 left-0 right-0 z-50 bg-[#161616] shadow-md transition-transform duration-300"
      :class="{ '-translate-y-full': hideOnScroll && isScrollingDown }"
    >
      <div class="flex items-center justify-between h-[60px] px-4">
        <div class="flex-1">
          <SearchBar placeholder="Поиск" @on-search="handleSearch" />
        </div>
      </div>
    </div>

    <!-- Full-width background -->
    <div class="absolute inset-0 bg-[#161616] hidden md:block"></div>

    <!-- Main header content -->
    <div class="w-full h-[60px] flex items-center justify-between relative z-10">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-[1250px] w-full">
        <div class="flex items-center justify-between h-[60px]">
          <!-- Logo section - visible on desktop -->
          <div class="hidden md:flex items-center">
            <router-link to="/">
              <Icon class="h-8 cursor-pointer" />
            </router-link>
          </div>

          <!-- Mobile: Logo + Search bar sticky at top -->
          <div class="flex md:hidden items-center gap-2 w-full">
            <router-link to="/" class="flex-shrink-0">
              <Icon class="h-8 cursor-pointer" />
            </router-link>
            <div class="flex-1">
              <SearchBar placeholder="Поиск" @on-search="handleSearch" />
            </div>
          </div>

          <!-- Desktop navigation -->
          <nav class="hidden md:flex items-center space-x-6 ml-8">
            <NavItem :to="navItems[0].to" :name="navItems[0].name" />
            <NavItem :to="navItems[1].to" :name="navItems[1].name" />
            <NavItem :to="navItems[4].to" :name="navItems[4].name" />
          </nav>

          <!-- Search bar - visible on desktop -->
          <div class="hidden md:flex flex-grow max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl mx-4">
            <SearchBar placeholder="Поиск" @on-search="handleSearch" />
          </div>

          <!-- User Profile or Login Button - hidden on mobile -->
          <div class="hidden md:flex items-center space-x-3" v-if="isLoggedIn">
            <div class="relative">
              <BookIcon class="w-6 h-6 text-white cursor-pointer" @click="handleBookClick" />
            </div>
            <div class="relative">
              <NotificationIcon
                class="w-6 h-6 text-white cursor-pointer"
                @click="handleNotificationClick"
              />
              <div
                v-if="hasNotifications"
                class="absolute -top-1 -right-1 w-3 h-3 bg-[#C4FF61] rounded-full"
              ></div>
            </div>
            <div
              class="w-8 h-8 rounded-full bg-[#C4FF61] flex items-center justify-center"
              :class="{ 'shadow-inner': !userProfile.hasImage }"
            >
              <span class="text-[#494949] font-bold text-sm">{{ userProfile.initials }}</span>
            </div>
          </div>
          <div class="hidden md:block" v-else>
            <Button @click="handleLogin">Войти</Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom navigation for mobile -->
    <div
      class="fixed bottom-0 left-0 right-0 bg-[#161616] border-t border-gray-700 py-2 md:hidden z-50"
    >
      <div class="flex items-center justify-around">
        <!-- Left menu item: Catalog -->
        <router-link to="/catalog" class="flex flex-col items-center text-white">
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
            ></path>
          </svg>
          <span class="text-xs mt-1">Каталог</span>
        </router-link>

        <!-- Left menu item: Notifications -->
        <router-link to="/notifications" class="flex flex-col items-center text-white">
          <div class="relative">
            <NotificationIcon class="w-6 h-6" />
            <div
              v-if="hasNotifications"
              class="absolute -top-1 -right-1 w-3 h-3 bg-[#C4FF61] rounded-full"
            ></div>
          </div>
          <span class="text-xs mt-1">Уведомления</span>
        </router-link>

        <!-- Center: Logo -->
        <router-link to="/" class="flex flex-col items-center">
          <Icon class="h-8 cursor-pointer" />
        </router-link>

        <!-- Right menu item: Favorites -->
        <router-link to="/favorites" class="flex flex-col items-center text-white">
          <BookIcon class="w-6 h-6" />
          <span class="text-xs mt-1">Закладки</span>
        </router-link>

        <!-- Right menu item: Profile -->
        <div class="flex flex-col items-center text-white" v-if="isLoggedIn">
          <router-link to="/profile" class="flex flex-col items-center">
            <div class="w-6 h-6 rounded-full bg-[#C4FF61] flex items-center justify-center">
              <span class="text-[#494949] font-bold text-xs">А</span>
            </div>
            <span class="text-xs mt-1">Профиль</span>
          </router-link>
        </div>
        <div class="flex flex-col items-center text-white" v-else>
          <router-link to="/login" class="flex flex-col items-center">
            <div class="w-6 h-6 rounded-full bg-[#C4FF61] flex items-center justify-center">
              <span class="text-[#494949] font-bold text-xs">В</span>
            </div>
            <span class="text-xs mt-1">Войти</span>
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Icon from '@/components/icons/Icon.vue'
import NavItem from '@/components/layout/NavItem.vue'
import SearchBar from '@/components/common/SearchBar.vue'
import Button from '@/components/common/Button.vue'
import NotificationIcon from '@/components/icons/Notification.vue'
import BookIcon from '@/components/icons/Book.vue'

const isLoggedIn = ref(true) // This would typically come from your auth store/state
const hasNotifications = ref(true) // This would typically come from your notification store/state

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
  { name: 'Закладки', to: '/favorites' },
  { name: 'Профиль', to: '/profile' },
]

// Mobile menu functionality removed as we're using a bottom navigation bar

const handleSearch = () => {
  // Handle search functionality here
  console.log('Search clicked')
}

const handleLogin = () => {
  isLoggedIn.value = true
}

const handleLogout = () => {
  isLoggedIn.value = false
  closeMobileMenu()
}

const handleBookClick = () => {
  console.log('Book icon clicked')
  // Add functionality for book icon here
}

const handleNotificationClick = () => {
  console.log('Notification icon clicked')
  // Add functionality for notification icon here
  hasNotifications.value = false // Clear notifications when clicked
}

const userProfile = computed(() => {
  return {
    name: 'Александр',
    initials: 'А',
    hasImage: false, // Set to true if user has uploaded an avatar image
  }
})
</script>
