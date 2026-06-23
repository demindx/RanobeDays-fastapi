<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import Icon from '../icons/Icon.vue'
import NavHomeIcon from '../icons/NavHomeIcon.vue'
import NavCatalogIcon from '../icons/NavCatalogIcon.vue'
import NavBookmarkIcon from '../icons/NavBookmarkIcon.vue'
import NotificationBellIcon from '../icons/NotificationBellIcon.vue'
import NavMenuIcon from '../icons/NavMenuIcon.vue'
import CloseIcon from '../icons/CloseIcon.vue'
import SettingsIcon from '../icons/SettingsIcon.vue'
import LogoutIcon from '../icons/LogoutIcon.vue'
import AppButton from '../shared/AppButton.vue'
import { useTheme } from '../../composables/useTheme'
import { useAuth } from '../../composables/useAuth'
import { useProfile } from '../../composables/useProfile'
import { navLinks as routeLinks } from '../../constants/navigation'

const router = useRouter()
const route = useRoute()
const isMenuOpen = ref(false)
const { isDark, toggleTheme } = useTheme()
const { isAuthenticated, isAuthModalOpen, user, logout } = useAuth()
const { openSettings } = useProfile()

const visible = computed(() => route.name !== 'chapter')

const iconByRoute = {
  '/': NavHomeIcon,
  '/catalog': NavCatalogIcon,
  '/bookmarks': NavBookmarkIcon,
}

const mainLinks = routeLinks.map((link) => ({
  ...link,
  icon: iconByRoute[link.to],
}))

const openAuthFromMenu = () => {
  isMenuOpen.value = false
  isAuthModalOpen.value = true
}

const handleLogout = () => {
  logout()
  isMenuOpen.value = false
}

const handleSettings = () => {
  isMenuOpen.value = false
  router.push('/profile')
  openSettings()
}
</script>

<template>
  <template v-if="visible">
    <nav
      class="fixed inset-x-0 bottom-0 z-40 border-t border-zinc-700/80 bg-zinc-900 md:hidden transform-gpu"
    >
      <div class="mx-auto w-full max-w-6xl px-2 pb-[calc(env(safe-area-inset-bottom)+8px)] pt-2">
        <div class="grid grid-cols-5 items-end gap-1 text-zinc-300">
          <component
            v-for="(link, idx) in mainLinks"
            :key="link.label"
            :is="link.to ? RouterLink : 'a'"
            :to="link.to"
            :href="link.href"
            :class="[
              'flex cursor-pointer select-none flex-col items-center gap-1 rounded-md px-1 py-2 text-[11px] hover:bg-zinc-800',
              idx === 0 ? 'col-start-1 row-start-1' : '',
              idx === 1 ? 'col-start-2 row-start-1' : '',
              idx === 2 ? 'col-start-4 row-start-1' : '',
            ]"
          >
            <component :is="link.icon" />
            <span>{{ link.label }}</span>
          </component>

          <RouterLink
            to="/"
            class="col-start-3 row-start-1 mx-auto -mt-6 rounded-full border border-zinc-700/80 bg-zinc-950 p-2.5 shadow-lg hover:opacity-90"
          >
            <Icon class="h-7 w-auto" />
          </RouterLink>

          <button
            type="button"
            class="col-start-5 row-start-1 flex cursor-pointer flex-col items-center gap-1 rounded-md px-1 py-2 text-[11px] hover:bg-zinc-800"
            @click="isMenuOpen = true"
          >
            <NavMenuIcon />
            <span>Меню</span>
          </button>
        </div>
      </div>
    </nav>

    <div
      :class="[
        'fixed inset-0 z-50 md:hidden',
        isMenuOpen ? 'pointer-events-auto' : 'pointer-events-none',
      ]"
    >
      <div
        :class="[
          'absolute inset-0 bg-black/50 transition-opacity duration-200',
          isMenuOpen ? 'opacity-100' : 'opacity-0',
        ]"
        @click="isMenuOpen = false"
      />

      <aside
        :class="[
          'absolute right-0 top-0 h-full w-[86%] max-w-sm border-l border-zinc-700 bg-zinc-900/98 p-4 shadow-2xl transition-transform duration-200',
          isMenuOpen ? 'translate-x-0' : 'translate-x-full',
        ]"
      >
        <div class="flex h-full flex-col">
          <div class="mb-4 flex items-center justify-end">
            <button
              type="button"
              class="cursor-pointer rounded-md p-2 text-zinc-300 transition hover:bg-zinc-800 active:scale-95"
              @click="isMenuOpen = false"
            >
              <CloseIcon />
            </button>
          </div>

          <div v-if="isAuthenticated" class="mb-4">
            <RouterLink
              to="/profile"
              class="flex items-center gap-3 rounded-lg border border-zinc-800 bg-zinc-900 p-3 transition hover:bg-zinc-800"
              @click="isMenuOpen = false"
            >
              <div
                class="flex h-10 w-10 items-center justify-center rounded-full text-sm font-semibold text-white"
                :class="user?.avatarColorClass || 'bg-zinc-700'"
              >
                {{ (user?.login || 'U').slice(0, 1).toUpperCase() }}
              </div>
              <div>
                <p class="text-sm font-medium text-zinc-200">{{ user?.login || 'Профиль' }}</p>
                <p class="text-xs text-zinc-500">Профиль</p>
              </div>
            </RouterLink>
          </div>
          <AppButton
            v-else
            variant="primary-gradient"
            block
            class="mb-4 font-semibold"
            @click="openAuthFromMenu"
          >
            Войти
          </AppButton>

          <div v-if="isAuthenticated" class="p-1.5">
            <RouterLink
              to="/notifications"
              class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
              @click="isMenuOpen = false"
            >
              <NotificationBellIcon class="text-zinc-400" />
              <span>Уведомления</span>
            </RouterLink>

            <RouterLink
              to="/bookmarks"
              class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
              @click="isMenuOpen = false"
            >
              <NavBookmarkIcon class="text-zinc-400" />
              <span>Закладки</span>
            </RouterLink>

            <button
              type="button"
              class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
              @click="handleSettings"
            >
              <SettingsIcon class="text-zinc-400" />
              <span>Настройки</span>
            </button>
          </div>

          <div class="mt-auto border-t border-zinc-800 p-1.5">
            <button
              type="button"
              class="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-200 transition hover:bg-zinc-800 hover:text-white"
              @click="toggleTheme"
            >
              <SettingsIcon class="text-zinc-400" />
              <span>{{ isDark ? 'Тёмная' : 'Светлая' }} тема</span>
            </button>

            <button
              v-if="isAuthenticated"
              type="button"
              class="mt-1 flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-rose-300 transition hover:bg-rose-500/15"
              @click="handleLogout"
            >
              <LogoutIcon class="text-rose-400" />
              <span>Выйти</span>
            </button>
          </div>
        </div>
      </aside>
    </div>
  </template>
</template>
