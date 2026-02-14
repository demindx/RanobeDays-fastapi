<script setup>
import Button from '@/components/common/Button.vue'
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
  userHasImage: {
    type: Boolean,
    required: true,
  },
})

defineEmits(['login', 'book-click', 'notifications-click'])
</script>

<template>
  <div
    v-if="isLoggedIn"
    class="hidden md:flex items-center space-x-3"
  >
    <div class="relative">
      <button
        type="button"
        class="cursor-pointer rounded-full p-1 text-white transition hover:text-rd-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rd-accent"
        aria-label="Открыть закладки"
        @click="$emit('book-click')"
      >
        <BookIcon class="w-6 h-6" />
      </button>
    </div>
    <div class="relative">
      <button
        type="button"
        class="cursor-pointer rounded-full p-1 text-white transition hover:text-rd-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rd-accent"
        aria-label="Открыть уведомления"
        @click="$emit('notifications-click')"
      >
        <NotificationIcon class="w-6 h-6" />
      </button>
      <div
        v-if="hasNotifications"
        class="absolute -top-1 -right-1 w-3 h-3 bg-rd-accent rounded-full"
        aria-hidden="true"
      />
    </div>
    <router-link
      to="/profile"
      class="w-8 h-8 rounded-full bg-rd-accent flex items-center justify-center focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rd-accent"
      :class="{ 'shadow-inner': !userHasImage }"
      aria-label="Открыть профиль"
    >
      <span class="text-rd-text-strong font-bold text-sm">{{ userInitials }}</span>
    </router-link>
  </div>
  <div
    v-else
    class="hidden md:block"
  >
    <Button @click="$emit('login')">
      Войти
    </Button>
  </div>
</template>
