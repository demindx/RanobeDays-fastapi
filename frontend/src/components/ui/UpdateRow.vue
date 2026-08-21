<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  update: {
    type: Object,
    required: true,
  },
})

const updateHref = computed(() =>
  props.update.href && props.update.href !== '#'
    ? props.update.href
    : `/novel/${props.update.novelId || props.update.id}`,
)

const isInternalLink = computed(() => updateHref.value.startsWith('/'))
</script>

<template>
  <component
    :is="isInternalLink ? RouterLink : 'a'"
    :to="isInternalLink ? updateHref : undefined"
    :href="isInternalLink ? undefined : updateHref"
    class="flex flex-col gap-2 rounded-xl border border-zinc-700/70 bg-zinc-900/70 px-3 py-3 transition odd:hover:border-emerald-300/60 even:hover:border-lime-300/60 card-interactive sm:flex-row sm:items-center sm:justify-between sm:gap-3 sm:px-4"
  >
    <div class="min-w-0">
      <p class="truncate text-sm font-medium text-white">{{ props.update.novelTitle }}</p>
      <p class="text-xs text-zinc-400">{{ props.update.chapter }}</p>
    </div>
    <span class="shrink-0 text-xs text-zinc-500">{{ props.update.timeAgo }}</span>
  </component>
</template>
