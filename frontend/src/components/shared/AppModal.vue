<script setup>
import { onBeforeUnmount, onMounted } from 'vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  containerClass: {
    type: String,
    default: 'flex items-center justify-center px-3 py-4 sm:px-4 sm:py-6',
  },
  panelClass: {
    type: String,
    default: 'w-full max-w-md rounded-2xl border border-zinc-700 bg-zinc-900 p-4 shadow-2xl sm:p-5',
  },
})

const emit = defineEmits(['close'])

const handleKeydown = (event) => {
  if (props.open && event.key === 'Escape') emit('close')
}

onMounted(() => window.addEventListener('keydown', handleKeydown))
onBeforeUnmount(() => window.removeEventListener('keydown', handleKeydown))
</script>

<template>
  <div
    v-if="props.open"
    class="fixed inset-0 z-50 bg-black/65"
    :class="props.containerClass"
    @click.self="emit('close')"
  >
    <div role="dialog" aria-modal="true" :class="props.panelClass">
      <slot />
    </div>
  </div>
</template>
