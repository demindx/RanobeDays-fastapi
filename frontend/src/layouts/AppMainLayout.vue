<script setup>
import DefaultFooter from '../components/home/DefaultFooter.vue'
import HomeHeader from '../components/home/HomeHeader.vue'
import AppSectionSwitchTransition from '../components/shared/AppSectionSwitchTransition.vue'
import AppErrorBoundary from '../components/shared/AppErrorBoundary.vue'
import { useAuth } from '../composables/useAuth'

const { isAuthenticated, user, hasUnreadNotifications } = useAuth()

const animatedRouteNames = new Set(['home', 'catalog', 'bookmarks', 'novel', 'profile'])

const shouldAnimateRoute = (route) => animatedRouteNames.has(String(route?.name || ''))
const routeViewKey = (route) => String(route?.name || route?.path || 'route')
</script>

<template>
  <main class="min-h-screen bg-zinc-950 text-white flex flex-col">
    <div
      class="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-4 px-3 py-4 pb-24 sm:px-4 sm:py-6 md:gap-6 md:px-6 md:py-8 md:pb-8"
    >
      <HomeHeader
        v-memo="[isAuthenticated, user, hasUnreadNotifications]"
        :is-authenticated="isAuthenticated"
        :user="user"
        :has-unread-notifications="hasUnreadNotifications"
      />

      <div class="flex-1">
        <AppErrorBoundary>
          <RouterView v-slot="{ Component, route }">
            <AppSectionSwitchTransition v-if="shouldAnimateRoute(route)">
              <component :is="Component" :key="routeViewKey(route)" />
            </AppSectionSwitchTransition>
            <component :is="Component" v-else />
          </RouterView>
        </AppErrorBoundary>
      </div>

      <div class="mt-auto">
        <DefaultFooter />
      </div>
    </div>
  </main>
</template>
