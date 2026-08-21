<script setup>
import { RouterLink } from 'vue-router'

const props = defineProps({
  id: { type: [String, Number], required: true },
  name: { type: String, required: true },
  avatarColorClass: { type: String, default: 'bg-zinc-600' },
})
</script>

<template>
  <RouterLink
    :to="'/team/' + props.id"
    class="flex flex-col items-center gap-2 transition hover:opacity-80"
  >
    <div
      class="flex h-14 w-14 items-center justify-center rounded-full text-lg font-bold text-white shadow-md"
      :class="props.avatarColorClass"
    >
      {{ props.name.slice(0, 1).toUpperCase() }}
    </div>
    <span class="text-center text-xs leading-tight text-zinc-300">{{ props.name }}</span>
  </RouterLink>
</template>
