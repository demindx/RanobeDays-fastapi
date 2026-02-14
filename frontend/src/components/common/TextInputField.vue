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
    :style="{ width: typeof width === 'number' ? `${width}px` : width }"
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
  align-items: center;
  height: 34px;
  border-radius: 3px;
  background: var(--third-color);
  border: 1px solid transparent;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.rd-field:focus-within {
  border-color: var(--first-color);
  box-shadow: 0 0 0 2px var(--focus-ring-color);
}

.rd-field__input {
  width: 100%;
  height: 100%;
  border: none;
  background: transparent;
  padding: 0 12px 0 20px;
  color: #dbdbdb;
  font-size: 12px;
  line-height: 1;
}

.rd-field__input::placeholder {
  color: #dbdbdb;
  opacity: 0.85;
}

.rd-field__input:focus {
  outline: none;
}

.rd-field__input:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
