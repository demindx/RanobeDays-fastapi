<script setup>
defineProps({
  item: { type: Object, required: true },
})
</script>

<template>
  <div
    class="flex items-center gap-3 bg-zinc-900/50 px-4 py-3 transition hover:bg-zinc-800/50 sm:px-5 sm:py-3.5"
  >
    <div class="h-12 w-9 shrink-0 rounded-md bg-gradient-to-br" :class="item.coverStyle" />
    <div class="min-w-0 flex-1">
      <p class="truncate text-sm font-medium text-zinc-200">{{ item.title }}</p>
      <p class="truncate text-xs text-zinc-500">{{ item.author }} · {{ item.chapterLabel }}</p>
    </div>
    <span class="shrink-0 rounded-full bg-zinc-800/70 px-2 py-1 text-xs text-zinc-400">
      ★ {{ item.rating }}
    </span>
  </div>
</template>
