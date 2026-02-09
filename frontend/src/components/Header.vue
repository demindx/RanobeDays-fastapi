<template>
  <header class="w-full relative">
    <!-- Full-width background -->
    <div class="absolute inset-0 bg-[#232323]"></div>

    <!-- Main header content -->
    <div class="w-full h-[60px] flex items-center justify-between relative z-10">
      <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-[1250px] w-full">
        <div class="flex items-center justify-between h-[60px]">
          <!-- Logo section -->
          <div class="flex items-center">
            <router-link to="/">
              <Icon class="h-8 cursor-pointer" />
            </router-link>
          </div>

          <!-- Desktop navigation -->
          <nav class="hidden md:flex items-center space-x-6 ml-8">
            <NavItem v-for="item in navItems" :key="item.name" :to="item.to" :name="item.name" />
          </nav>

          <!-- Search bar -->
          <div class="hidden md:block mx-8 flex-grow max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl">
            <SearchBar placeholder="Поиск" @on-search="handleSearch" />
          </div>

          <!-- User Profile or Login Button - hidden on mobile -->
          <div class="hidden md:flex items-center space-x-3" v-if="isLoggedIn">
            <div class="relative">
              <BookIcon class="w-6 h-6 text-white cursor-pointer" @click="handleBookClick" />
            </div>
            <div class="relative">
              <NotificationIcon class="w-6 h-6 text-white cursor-pointer" @click="handleNotificationClick" />
              <div v-if="hasNotifications" class="absolute -top-1 -right-1 w-3 h-3 bg-[#C4FF61] rounded-full"></div>
            </div>
            <div class="w-8 h-8 rounded-full bg-[#C4FF61] flex items-center justify-center" :class="{'shadow-inner': !userProfile.hasImage}">
              <span class="text-[#494949] font-bold text-sm">{{ userProfile.initials }}</span>
            </div>
          </div>
          <div class="hidden md:block" v-else>
            <Button @click="handleLogin">Войти</Button>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden text-white focus:outline-none z-50"
            aria-label="Toggle menu"
          >
            <svg
              v-if="!mobileMenuOpen"
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
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
            </svg>
            <svg
              v-else
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
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div
      v-if="mobileMenuOpen"
      class="md:hidden fixed inset-0 bg-transparent z-40 transition-opacity"
      @click="closeMobileMenu"
    ></div>

    <div
      v-if="mobileMenuOpen"
      class="md:hidden fixed top-0 left-0 h-full w-full bg-[#232323] z-40"
    >
      <div class="flex flex-col h-full">
        <!-- Header section with logo and search -->
        <div class="p-4 border-b border-gray-700">
          <div class="flex items-center justify-between mb-4">
            <router-link to="/" @click="closeMobileMenu">
              <Icon class="h-8 cursor-pointer" />
            </router-link>
            <button
              @click="closeMobileMenu"
              class="text-white focus:outline-none"
              aria-label="Close menu"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <SearchBar placeholder="Поиск" @on-search="handleSearch" />
        </div>

        <!-- Main content area -->
        <div class="flex-grow p-4 overflow-y-auto">
          <nav class="grid grid-cols-2 gap-4 mb-6">
            <NavItem
              v-for="item in navItems"
              :key="item.name"
              :to="item.to"
              :name="item.name"
              @click="closeMobileMenu"
              class="py-3 text-center bg-[#2C2C2C] rounded-lg"
            />
          </nav>

          <div class="mt-auto" v-if="isLoggedIn">
            <div class="flex justify-center space-x-6 mb-4">
              <div class="relative">
                <BookIcon class="w-6 h-6 text-white cursor-pointer" @click="handleBookClick" />
              </div>
              <div class="relative">
                <NotificationIcon class="w-6 h-6 text-white cursor-pointer" @click="handleNotificationClick" />
                <div v-if="hasNotifications" class="absolute -top-1 -right-1 w-3 h-3 bg-[#C4FF61] rounded-full"></div>
              </div>
              <div class="w-8 h-8 rounded-full bg-[#C4FF61] flex items-center justify-center" :class="{'shadow-inner': !userProfile.hasImage}">
                <span class="text-[#494949] font-bold text-sm">{{ userProfile.initials }}</span>
              </div>
            </div>
            <Button @click="handleLogout" class="w-full">Выйти</Button>
          </div>
          <div class="mt-auto" v-else>
            <Button @click="handleLogin" class="w-full">Войти</Button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue';
import Icon from '@/components/icons/Icon.vue';
import NavItem from '@/components/NavItem.vue';
import SearchBar from '@/components/SearchBar.vue';
import Button from '@/components/Button.vue';
import NotificationIcon from '@/components/icons/Notification.vue';
import BookIcon from '@/components/icons/Book.vue';

const mobileMenuOpen = ref(false);
const isLoggedIn = ref(true); // This would typically come from your auth store/state
const hasNotifications = ref(true); // This would typically come from your notification store/state

const navItems = [
  { name: 'Главная', to: '/' },
  { name: 'Каталог', to: '/catalog' },
  { name: 'Случайный тайтл', to: '/random' },
];

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const closeMobileMenu = () => {
  mobileMenuOpen.value = false;
};

const handleSearch = () => {
  // Handle search functionality here
  console.log('Search clicked');
};

const handleLogin = () => {
  isLoggedIn.value = true;
};

const handleLogout = () => {
  isLoggedIn.value = false;
  closeMobileMenu();
};

const handleBookClick = () => {
  console.log('Book icon clicked');
  // Add functionality for book icon here
};

const handleNotificationClick = () => {
  console.log('Notification icon clicked');
  // Add functionality for notification icon here
  hasNotifications.value = false; // Clear notifications when clicked
};

const userProfile = computed(() => {
  return {
    name: 'Александр',
    initials: 'А',
    hasImage: false // Set to true if user has uploaded an avatar image
  };
});
</script>
