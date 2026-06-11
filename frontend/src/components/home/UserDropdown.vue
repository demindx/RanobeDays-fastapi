<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import NavHomeIcon from '../icons/NavHomeIcon.vue'
import NavBookmarkIcon from '../icons/NavBookmarkIcon.vue'
import NavCollectionIcon from '../icons/NavCollectionIcon.vue'
import SettingsIcon from '../icons/SettingsIcon.vue'
import LogoutIcon from '../icons/LogoutIcon.vue'
import { useTheme } from '../../composables/useTheme'
import { useAuth } from '../../composables/useAuth'
import { useClickOutside } from '../../composables/useClickOutside'

const props = defineProps({
  user: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['open-settings', 'open-profile', 'open-history', 'open-achievements'])

const isOpen = ref(false)
const rootRef = ref(null)
const { isDark, toggleTheme } = useTheme()
const { logout } = useAuth()

const toggle = () => {
  isOpen.value = !isOpen.value
}

const close = () => {
  isOpen.value = false
}

const handleLogout = () => {
  logout()
  close()
}

const handleAction = (action) => {
  emit(action)
  close()
}

useClickOutside(rootRef, isOpen, close)
</script>

<template>
  <div ref="rootRef" class="relative">
    <button
      type="button"
      class="flex h-10 w-10 items-center justify-center rounded-full border transition"
      :class="[
        props.user?.avatarColorClass || 'bg-zinc-700',
        isOpen
          ? 'border-lime-300/60 ring-2 ring-lime-300/30'
          : 'border-zinc-700 hover:opacity-90 active:scale-95',
      ]"
      :aria-label="`Профиль ${props.user?.login || ''}`"
      @click="toggle"
    >
      <span class="text-sm font-semibold text-white">
        {{ (props.user?.login || 'U').slice(0, 1).toUpperCase() }}
      </span>
    </button>

    <Transition
      enter-active-class="transition duration-150 ease-out"
      enter-from-class="opacity-0 -translate-y-1 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-100 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 -translate-y-1 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 z-50 mt-2 w-64 origin-top-right overflow-hidden rounded-xl border border-zinc-700/70 bg-zinc-900/98 shadow-xl shadow-black/40 backdrop-blur"
      >
        <div class="border-b border-zinc-800 px-4 py-3">
          <p class="text-sm font-semibold text-white">
            {{ props.user?.login || 'Пользователь' }}
          </p>
          <p class="text-xs text-zinc-500">Профиль</p>
        </div>

        <div class="p-1.5">
          <RouterLink
            to="/profile"
            class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
            @click="close"
          >
            <NavHomeIcon class="text-zinc-400" />
            <span>Профиль</span>
          </RouterLink>

          <RouterLink
            to="/bookmarks"
            class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
            @click="close"
          >
            <NavBookmarkIcon class="text-zinc-400" />
            <span>Закладки</span>
          </RouterLink>

          <button
            type="button"
            class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
            @click="handleAction('open-history')"
          >
            <NavCollectionIcon class="text-zinc-400" />
            <span>История чтения</span>
          </button>

          <button
            type="button"
            class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
            @click="handleAction('open-settings')"
          >
            <SettingsIcon class="text-zinc-400" />
            <span>Настройки</span>
          </button>
        </div>

        <div class="border-t border-zinc-800 p-1.5">
          <button
            type="button"
            class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
            @click="toggleTheme"
          >
            <SettingsIcon class="text-zinc-400" />
            <span>Тема: {{ isDark ? 'Тёмная' : 'Светлая' }}</span>
          </button>

          <button
            type="button"
            class="mt-1 flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-rose-300 transition hover:bg-rose-500/15"
            @click="handleLogout"
          >
            <LogoutIcon class="text-rose-400" />
            <span>Выйти</span>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>
