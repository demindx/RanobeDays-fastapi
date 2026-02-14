<script setup>
import { computed } from 'vue'

const props = defineProps({
  callback: {
    type: Function,
    default: null,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline', 'ghost'].includes(value),
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  loading: {
    type: Boolean,
    default: false,
  },
  type: {
    type: String,
    default: 'button',
  },
  fullWidth: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

const buttonClass = computed(() => {
  const base = 'btn'
  const variantClass = `btn--${props.variant}`
  const sizeClass = `btn--${props.size}`
  const loadingClass = props.loading ? 'btn--loading' : ''
  const widthClass = props.fullWidth ? 'btn--full' : ''
  const disabledClass = props.disabled ? 'btn--disabled' : ''

  return [base, variantClass, sizeClass, loadingClass, widthClass, disabledClass]
    .filter(Boolean)
    .join(' ')
})

const handleClick = async (event) => {
  if (props.disabled || props.loading) {
    event.preventDefault()
    return
  }

  emit('click', event)

  if (props.callback) {
    await props.callback()
  }
}
</script>

<template>
  <button
    :type="type"
    :class="buttonClass"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span
      v-if="loading"
      class="btn__spinner"
    />
    <span
      class="btn__content"
      :class="{ 'btn__content--hidden': loading }"
    >
      <slot />
    </span>
  </button>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-weight: 500;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px var(--focus-ring-color);
}

.btn:active:not(:disabled) {
  transform: scale(0.98);
}

.btn--primary {
  background: var(--first-color);
  color: var(--foreground-color);
  border: none;
}

.btn--primary:hover:not(:disabled) {
  background: var(--first-color-hover);
}

.btn--secondary {
  background: var(--foreground-color);
  color: var(--foreground-third-color);
  border: none;
}

.btn--secondary:hover:not(:disabled) {
  background: var(--surface-hover-color);
}

.btn--outline {
  background: transparent;
  color: var(--first-color);
  border: 2px solid var(--first-color);
}

.btn--outline:hover:not(:disabled) {
  background: var(--first-color-soft);
}

.btn--ghost {
  background: transparent;
  color: var(--foreground-third-color);
  border: none;
}

.btn--ghost:hover:not(:disabled) {
  background: var(--surface-muted-overlay-color);
}

.btn--sm {
  padding: 0.375rem 1rem;
  font-size: 0.75rem;
}

.btn--md {
  padding: 0.5rem 1.5rem;
  font-size: 0.875rem;
}

.btn--lg {
  padding: 0.75rem 2rem;
  font-size: 1rem;
}

.btn--full {
  width: 100%;
}

.btn--disabled,
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--loading {
  cursor: wait;
}

.btn__spinner {
  position: absolute;
  width: 1rem;
  height: 1rem;
  border: 2px solid transparent;
  border-top-color: var(--foreground-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.btn__content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn__content--hidden {
  visibility: hidden;
}
</style>
