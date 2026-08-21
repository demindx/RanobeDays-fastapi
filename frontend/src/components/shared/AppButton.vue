<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'neutral',
  },
  size: {
    type: String,
    default: 'md',
  },
  type: {
    type: String,
    default: 'button',
  },
  block: {
    type: Boolean,
    default: false,
  },
  href: {
    type: String,
    default: '',
  },
})

const tagName = computed(() => (props.href ? 'a' : 'button'))

const variantClass = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'bg-lime-300 text-zinc-900 hover:bg-lime-200'
    case 'primary-gradient':
      return 'bg-gradient-to-r from-lime-300 via-emerald-300 to-green-300 text-zinc-900 hover:from-lime-200 hover:via-emerald-200 hover:to-green-200'
    case 'success':
      return 'border border-emerald-300 bg-emerald-300/20 text-emerald-300 hover:bg-emerald-300/30'
    case 'danger':
      return 'border border-rose-300 bg-rose-300/15 text-rose-300 hover:bg-rose-300/25'
    default:
      return 'border border-zinc-700 bg-zinc-800 text-zinc-200 hover:bg-zinc-700'
  }
})

const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-2.5 py-1 text-xs'
    case 'lg':
      return 'px-4 py-2.5 text-sm'
    default:
      return 'px-3 py-2 text-sm'
  }
})
</script>

<template>
  <component
    :is="tagName"
    :type="tagName === 'button' ? props.type : undefined"
    :href="tagName === 'a' ? props.href : undefined"
    :class="[
      'inline-flex cursor-pointer items-center justify-center rounded-lg font-medium transition active:scale-95',
      variantClass,
      sizeClass,
      props.block ? 'w-full' : '',
    ]"
  >
    <slot />
  </component>
</template>
