<script setup>
const props = defineProps({
  as: {
    type: String,
    default: 'div',
  },
})
</script>

<template>
  <component
    :is="props.as"
    class="rounded-xl border border-zinc-700/70 bg-zinc-900/70 p-3"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>
