<script setup>
import Icon from '@/components/icons/Icon.vue'
import NotificationIcon from '@/components/icons/Notification.vue'
import BookIcon from '@/components/icons/Book.vue'

defineProps({
  isLoggedIn: {
    type: Boolean,
    required: true,
  },
  hasNotifications: {
    type: Boolean,
    required: true,
  },
  userInitials: {
    type: String,
    required: true,
  },
})

defineEmits(['notifications-click'])
</script>

<template>
  <div
    class="fixed bottom-0 left-0 right-0 bg-rd-surface border-t border-gray-700 py-2 md:hidden z-50"
  >
    <div class="flex items-center justify-around">
      <router-link
        to="/catalog"
        class="flex flex-col items-center text-white"
      >
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
          />
        </svg>
        <span class="text-xs mt-1">Каталог</span>
      </router-link>

      <router-link
        to="/notifications"
        class="flex flex-col items-center text-white"
        @click="$emit('notifications-click')"
      >
        <div class="relative">
          <NotificationIcon class="w-6 h-6" />
          <div
            v-if="hasNotifications"
            class="absolute -top-1 -right-1 w-3 h-3 bg-rd-accent rounded-full"
          />
        </div>
        <span class="text-xs mt-1">Уведомления</span>
      </router-link>

      <router-link
        to="/"
        class="flex flex-col items-center"
      >
        <Icon class="h-8 cursor-pointer" />
      </router-link>

      <router-link
        to="/favorites"
        class="flex flex-col items-center text-white"
      >
        <BookIcon class="w-6 h-6" />
        <span class="text-xs mt-1">Закладки</span>
      </router-link>

      <div
        v-if="isLoggedIn"
        class="flex flex-col items-center text-white"
      >
        <router-link
          to="/profile"
          class="flex flex-col items-center"
        >
          <div class="w-6 h-6 rounded-full bg-rd-accent flex items-center justify-center">
            <span class="text-rd-text-strong font-bold text-xs">{{ userInitials }}</span>
          </div>
          <span class="text-xs mt-1">Профиль</span>
        </router-link>
      </div>
      <div
        v-else
        class="flex flex-col items-center text-white"
      >
        <router-link
          to="/login"
          class="flex flex-col items-center"
        >
          <div class="w-6 h-6 rounded-full bg-rd-accent flex items-center justify-center">
            <span class="text-rd-text-strong font-bold text-xs">В</span>
          </div>
          <span class="text-xs mt-1">Войти</span>
        </router-link>
      </div>
    </div>
  </div>
</template>
