<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import AppTabs from '../components/shared/AppTabs.vue'
import AppEmptyState from '../components/shared/AppEmptyState.vue'
import {
  freeChapters as freeData,
  paidChapters as paidData,
  systemNotifications as systemData,
} from '../mocks/notificationsData'

const activeTab = ref('free')

const freeChapters = ref(freeData.map((n) => ({ ...n })))
const paidChapters = ref(paidData.map((n) => ({ ...n })))
const systemNotifications = ref(systemData.map((n) => ({ ...n })))

const unreadFree = computed(() => freeChapters.value.filter((n) => !n.isRead))
const unreadPaid = computed(() => paidChapters.value.filter((n) => !n.isRead))
const unreadSystem = computed(() => systemNotifications.value.filter((n) => !n.isRead))

const tabs = computed(() => [
  { key: 'free', label: 'Бесплатные главы', count: unreadFree.value.length },
  { key: 'paid', label: 'Платные', count: unreadPaid.value.length },
  { key: 'system', label: 'Системные', count: unreadSystem.value.length },
])

const markAsRead = (event, list, id) => {
  event.preventDefault()
  event.stopPropagation()
  const item = list.value.find((n) => n.id === id)
  if (item) item.isRead = true
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-bold text-white sm:text-2xl">Уведомления</h1>
    </div>

    <div class="rounded-2xl border border-zinc-700/70 bg-zinc-900/80">
      <AppTabs v-model:model-value="activeTab" :tabs="tabs" />

      <div class="p-4 sm:p-6">
        <template v-if="activeTab === 'free'">
          <AppEmptyState v-if="!unreadFree.length" compact>
            Нет новых уведомлений о бесплатных главах.
          </AppEmptyState>
          <div v-else class="space-y-2">
            <div
              v-for="notif in unreadFree"
              :key="notif.id"
              class="group flex items-center gap-3 rounded-lg border border-zinc-700 bg-zinc-900/60 px-3 py-2.5 transition hover:border-lime-300/40"
            >
              <span class="h-2 w-2 shrink-0 rounded-full bg-lime-400" />
              <RouterLink
                :to="`/novel/${notif.novelId}/chapter/${notif.novelId}-c1`"
                class="min-w-0 flex-1"
              >
                <p class="truncate text-sm text-zinc-200">{{ notif.novelTitle }}</p>
                <p class="text-xs text-zinc-500">{{ notif.chapter }}</p>
              </RouterLink>
              <span class="shrink-0 text-xs text-zinc-500">{{ notif.timeAgo }}</span>
              <button
                type="button"
                class="flex h-7 w-7 shrink-0 cursor-pointer items-center justify-center rounded-md border border-zinc-700 text-zinc-500 opacity-0 transition hover:border-lime-300/50 hover:text-lime-300 group-hover:opacity-100"
                title="Отметить прочитанным"
                @click="markAsRead($event, freeChapters, notif.id)"
              >
                <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M5 13l4 4L19 7"
                    stroke="currentColor"
                    stroke-width="2.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
            </div>
          </div>
        </template>

        <template v-if="activeTab === 'paid'">
          <AppEmptyState v-if="!unreadPaid.length" compact>
            Нет новых уведомлений о платных главах.
          </AppEmptyState>
          <div v-else class="space-y-2">
            <div
              v-for="notif in unreadPaid"
              :key="notif.id"
              class="group flex items-center gap-3 rounded-lg border border-zinc-700 bg-zinc-900/60 px-3 py-2.5 transition hover:border-amber-300/40"
            >
              <span class="h-2 w-2 shrink-0 rounded-full bg-amber-400" />
              <RouterLink
                :to="`/novel/${notif.novelId}/chapter/${notif.novelId}-c1`"
                class="min-w-0 flex-1"
              >
                <p class="truncate text-sm text-zinc-200">{{ notif.novelTitle }}</p>
                <p class="text-xs text-zinc-500">{{ notif.chapter }}</p>
              </RouterLink>
              <span class="shrink-0 rounded bg-amber-500/15 px-1.5 py-0.5 text-xs text-amber-300">
                {{ notif.price }}
              </span>
              <span class="shrink-0 text-xs text-zinc-500">{{ notif.timeAgo }}</span>
              <button
                type="button"
                class="flex h-7 w-7 shrink-0 cursor-pointer items-center justify-center rounded-md border border-zinc-700 text-zinc-500 opacity-0 transition hover:border-lime-300/50 hover:text-lime-300 group-hover:opacity-100"
                title="Отметить прочитанным"
                @click="markAsRead($event, paidChapters, notif.id)"
              >
                <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M5 13l4 4L19 7"
                    stroke="currentColor"
                    stroke-width="2.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
            </div>
          </div>
        </template>

        <template v-if="activeTab === 'system'">
          <AppEmptyState v-if="!unreadSystem.length" compact>
            Нет системных уведомлений.
          </AppEmptyState>
          <div v-else class="space-y-2">
            <div
              v-for="notif in unreadSystem"
              :key="notif.id"
              class="group rounded-lg border border-zinc-700 bg-zinc-900/60 px-4 py-3 transition"
            >
              <div class="flex items-start gap-3">
                <span class="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-blue-400" />
                <div class="min-w-0 flex-1">
                  <p class="text-sm font-medium text-zinc-200">{{ notif.title }}</p>
                  <p class="mt-0.5 text-sm text-zinc-400">{{ notif.text }}</p>
                </div>
                <span class="shrink-0 text-xs text-zinc-500">{{ notif.timeAgo }}</span>
                <button
                  type="button"
                  class="flex h-7 w-7 shrink-0 cursor-pointer items-center justify-center rounded-md border border-zinc-700 text-zinc-500 opacity-0 transition hover:border-lime-300/50 hover:text-lime-300 group-hover:opacity-100"
                  title="Отметить прочитанным"
                  @click="markAsRead($event, systemNotifications, notif.id)"
                >
                  <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
                    <path
                      d="M5 13l4 4L19 7"
                      stroke="currentColor"
                      stroke-width="2.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
