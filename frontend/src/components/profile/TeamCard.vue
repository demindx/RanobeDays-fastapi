<script setup>
const props = defineProps({
  name: { type: String, required: true },
  avatarColorClass: { type: String, default: 'bg-zinc-600' },
})
</script>

<template>
  <div class="flex flex-col items-center gap-2">
    <div
      class="flex h-14 w-14 items-center justify-center rounded-full text-lg font-bold text-white shadow-md transition hover:opacity-80"
      :class="props.avatarColorClass"
    >
      {{ props.name.slice(0, 1).toUpperCase() }}
    </div>
    <span class="text-center text-xs leading-tight text-zinc-300">{{ props.name }}</span>
  </div>
</template>
