<script setup>
import { RouterLink } from 'vue-router'
import NovelTags from '../shared/NovelTags.vue'

const props = defineProps({
  genres: {
    type: Array,
    default: () => [],
  },
  tags: {
    type: Array,
    default: () => [],
  },
  translators: {
    type: Array,
    default: () => [],
  },
})

const toTeamEntry = (t) => {
  if (t && typeof t === 'object' && t.id) return t
  return { id: null, name: String(t) }
}
</script>

<template>
  <div class="space-y-2">
    <NovelTags :genres="props.genres" :tags="props.tags" :show-labels="true" />

    <div v-if="props.translators.length" class="flex flex-wrap items-center gap-1.5">
      <span class="text-xs font-semibold text-zinc-400">Переводчики:</span>
      <template v-for="t in props.translators" :key="`translator-${t?.id || t}`">
        <RouterLink
          v-if="t?.id"
          :to="'/team/' + t.id"
          class="rounded-full border border-zinc-600 bg-zinc-800 px-2 py-0.5 text-xs text-zinc-200 transition hover:border-zinc-500 hover:text-zinc-100 active:scale-95"
        >
          {{ t.name }}
        </RouterLink>
        <span
          v-else
          class="rounded-full border border-zinc-600 bg-zinc-800 px-2 py-0.5 text-xs text-zinc-200"
        >
          {{ t }}
        </span>
      </template>
    </div>
  </div>
</template>
