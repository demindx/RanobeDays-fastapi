<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  id: {
    type: [String, Number],
    required: true,
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  clickable: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['click'])

const tagClass = computed(() => {
  const base = 'tag'
  const sizeClass = `tag--${props.size}`
  return `${base} ${sizeClass}`
})

const handleClick = (event) => {
  if (!props.clickable) {
    event.preventDefault()
    return
  }
  emit('click', { id: props.id, name: props.name })
}
</script>

<template>
  <component
    :is="clickable ? 'router-link' : 'span'"
    :to="clickable ? `/catalog?tag=${id}` : undefined"
    :class="tagClass"
    :aria-label="`Тег: ${name}`"
    @click="handleClick"
  >
    {{ name }}
  </component>
</template>

<style scoped>
.tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  background: var(--secondary-color);
  color: var(--foreground-color);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.tag:hover {
  background: var(--first-color-hover);
  transform: scale(1.02);
}

.tag:active {
  transform: scale(0.98);
}

.tag--sm {
  padding: 0.125rem 0.5rem;
  font-size: 0.7rem;
}

.tag--md {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
}

.tag--lg {
  padding: 0.375rem 1rem;
  font-size: 0.875rem;
}
</style>
