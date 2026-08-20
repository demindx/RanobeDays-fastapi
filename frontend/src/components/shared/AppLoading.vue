<script setup>
defineProps({
  label: {
    type: String,
    default: 'Загрузка...',
  },
})
</script>

<template>
  <div class="flex items-center justify-center gap-2 py-10 text-sm text-zinc-500">
    <span class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-600 border-t-lime-400" />
    <span>{{ label }}</span>
  </div>
</template>
