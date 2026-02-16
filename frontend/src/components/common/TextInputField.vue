<script setup>
defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  name: {
    type: String,
    default: '',
  },
  id: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  ariaLabel: {
    type: String,
    default: 'Текстовое поле',
  },
  autocomplete: {
    type: String,
    default: 'off',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  width: {
    type: [String, Number],
    default: 229,
  },
})

const emit = defineEmits(['update:modelValue', 'focus', 'blur', 'enter'])

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleKeydown = (event) => {
  if (event.key === 'Enter') {
    emit('enter', event.target.value)
  }
}
</script>

<template>
  <div
    class="rd-field"
    :style="{ '--rd-field-width': typeof width === 'number' ? `${width}px` : width }"
  >
    <input
      :id="id || undefined"
      :name="name || undefined"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :aria-label="ariaLabel"
      :autocomplete="autocomplete"
      :disabled="disabled"
      class="rd-field__input"
      @input="handleInput"
      @focus="$emit('focus', $event)"
      @blur="$emit('blur', $event)"
      @keydown="handleKeydown"
    >
  </div>
</template>

<style scoped>
.rd-field {
  display: inline-flex;
  width: min(100%, var(--rd-field-width));
  max-width: 100%;
  align-items: center;
  height: 34px;
  border-radius: 4px;
  background: var(--third-color);
  border: 1px solid var(--border-soft-color);
  box-shadow: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.rd-field:hover {
  border-color: color-mix(in srgb, white 24%, var(--border-soft-color));
}

.rd-field:focus-within {
  box-shadow: 0 0 0 1px var(--first-color);
}

.rd-field__input {
  width: 100%;
  height: 100%;
  border: none;
  background: transparent;
  padding: 0 12px 0 20px;
  color: var(--foreground-third-color);
  font-size: 12px;
  font-weight: 500;
  line-height: 1;
}

.rd-field__input::placeholder {
  color: var(--foreground-secondary-color);
  opacity: 1;
}

.rd-field__input:focus {
  outline: none;
}

.rd-field__input:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

@media (max-width: 767px) {
  .rd-field {
    width: 100%;
  }
}
</style>
