<script setup>
const props = defineProps({
  compact: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <div
    :class="[
      'rounded-xl border border-dashed border-zinc-700 bg-zinc-900/50 px-4 text-sm text-zinc-400',
      props.compact ? 'py-6' : 'py-8',
    ]"
  >
    <slot />
  </div>
</template>
