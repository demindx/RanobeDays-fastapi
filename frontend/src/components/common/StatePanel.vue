<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    default: '',
  },
  variant: {
    type: String,
    default: 'info',
    validator: (value) => ['info', 'empty', 'error', 'loading'].includes(value),
  },
  actionLabel: {
    type: String,
    default: '',
  },
  busy: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['action'])

const role = computed(() => (props.variant === 'error' ? 'alert' : 'status'))

const panelClass = computed(() => {
  const map = {
    info: 'state-panel--info',
    empty: 'state-panel--empty',
    error: 'state-panel--error',
    loading: 'state-panel--loading',
  }
  return ['state-panel', map[props.variant]].join(' ')
})

const handleAction = () => {
  emit('action')
}
</script>

<template>
  <section
    :class="panelClass"
    :role="role"
    aria-live="polite"
    :aria-busy="busy ? 'true' : undefined"
  >
    <h2 class="state-panel__title">
      {{ title }}
    </h2>
    <p
      v-if="description"
      class="state-panel__description"
    >
      {{ description }}
    </p>

    <slot />

    <button
      v-if="actionLabel"
      type="button"
      class="state-panel__action"
      @click="handleAction"
    >
      {{ actionLabel }}
    </button>
  </section>
</template>

<style scoped>
.state-panel {
  border-radius: 0.75rem;
  border: 1px solid var(--border-soft-color);
  background: var(--surface-elevated-color);
  padding: 1rem;
}

.state-panel--loading {
  opacity: 0.9;
}

.state-panel--error {
  border-color: color-mix(in srgb, var(--danger-color) 50%, transparent);
  background: color-mix(in srgb, var(--danger-color) 10%, var(--surface-elevated-color));
}

.state-panel__title {
  color: var(--foreground-third-color);
  font-size: 1rem;
  font-weight: 700;
  margin: 0;
}

.state-panel__description {
  color: var(--foreground-secondary-color);
  margin-top: 0.5rem;
  margin-bottom: 0;
}

.state-panel__action {
  margin-top: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--first-color);
  color: var(--foreground-color);
  font-weight: 600;
  cursor: pointer;
}

.state-panel__action:focus-visible {
  outline: 2px solid var(--first-color);
  outline-offset: 2px;
}
</style>
