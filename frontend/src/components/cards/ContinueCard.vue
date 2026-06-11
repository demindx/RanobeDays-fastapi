<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { getNovelById } from '../../mocks/novelPageData'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

const readHref = computed(() => {
  const novelId = props.item.novelId || props.item.id
  const novel = getNovelById(novelId)
  const firstChapter = novel?.chapters?.[0]
  if (firstChapter) {
    return `/novel/${novelId}/chapter/${firstChapter.id}`
  }
  return `/novel/${novelId}`
})
</script>

<template>
  <article class="rounded-2xl border border-zinc-700/70 bg-zinc-900/70 p-3 sm:p-4">
    <h3 class="line-clamp-2 text-sm font-semibold text-white">{{ props.item.title }}</h3>
    <p class="mt-1 text-xs text-zinc-400">
      Глава {{ props.item.currentChapter }} из {{ props.item.totalChapters }}
    </p>

    <div class="mt-4 h-2 overflow-hidden rounded-full bg-zinc-700">
      <div
        class="h-full rounded-full bg-gradient-to-r from-lime-400 via-emerald-400 to-green-500"
        :style="{ width: `${props.item.progress}%` }"
      />
    </div>

    <div class="mt-3 flex items-center justify-between gap-2">
      <span class="text-xs text-zinc-400">{{ props.item.progress }}%</span>
      <RouterLink
        :to="readHref"
        class="cursor-pointer rounded-lg bg-gradient-to-r from-lime-400 to-emerald-400 px-3 py-1 text-xs font-semibold text-zinc-900 transition hover:from-lime-300 hover:to-emerald-300 active:scale-95"
      >
        Читать
      </RouterLink>
    </div>
  </article>
</template>
