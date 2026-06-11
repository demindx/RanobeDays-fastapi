<script setup>
import { RouterLink } from 'vue-router'
import AppEmptyState from '../shared/AppEmptyState.vue'
import AppPanel from '../shared/AppPanel.vue'

const props = defineProps({
  chapters: {
    type: Array,
    default: () => [],
  },
  novelId: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <AppPanel as="section" class="rounded-2xl space-y-3">
    <h3 class="text-base font-semibold text-white">Главы</h3>

    <AppEmptyState v-if="!props.chapters.length" compact> Глав пока нет. </AppEmptyState>

    <div v-else class="space-y-2">
      <RouterLink
        v-for="chapter in props.chapters"
        :key="chapter.id"
        :to="`/novel/${props.novelId}/chapter/${chapter.id}`"
        :class="[
          'flex cursor-pointer items-center justify-between rounded-xl border px-3 py-2 text-left transition card-interactive',
          chapter.isRead
            ? 'border-emerald-300/35 bg-emerald-400/10 hover:bg-emerald-400/15'
            : 'border-zinc-700 bg-zinc-800/60 hover:bg-zinc-800',
        ]"
      >
        <div class="min-w-0">
          <p class="truncate text-sm font-medium text-zinc-200">
            Глава {{ chapter.number }} — {{ chapter.title }}
          </p>
          <p class="text-xs text-zinc-500">{{ chapter.publishedAt }}</p>
        </div>
        <span
          class="ml-2 shrink-0 text-xs"
          :class="chapter.isRead ? 'text-emerald-300' : 'text-zinc-400'"
        >
          {{ chapter.isRead ? 'Прочитано' : 'Новая' }}
        </span>
      </RouterLink>
    </div>
  </AppPanel>
</template>
