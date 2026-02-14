<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  options: {
    type: Array,
    default: () => [],
  },
  id: {
    type: String,
    default: '',
  },
  name: {
    type: String,
    default: '',
  },
  ariaLabel: {
    type: String,
    default: 'Выпадающий список',
  },
  placeholder: {
    type: String,
    default: 'Выберите значение',
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

const emit = defineEmits(['update:modelValue', 'change', 'focus', 'blur'])

const rootRef = ref(null)
const triggerRef = ref(null)
const isOpen = ref(false)

const listboxId = computed(() => `${props.id || 'rd-select'}-listbox`)

const selectedOption = computed(() =>
  props.options.find((option) => String(option.value) === String(props.modelValue)),
)

const buttonLabel = computed(() => selectedOption.value?.label || props.placeholder)

const openDropdown = () => {
  if (props.disabled) return
  isOpen.value = true
}

const closeDropdown = () => {
  isOpen.value = false
}

const toggleDropdown = () => {
  if (props.disabled) return
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  if (option.disabled) return
  emit('update:modelValue', option.value)
  emit('change', option.value)
  closeDropdown()
  triggerRef.value?.focus()
}

const handleDocumentPointerDown = (event) => {
  if (!rootRef.value) return
  if (!rootRef.value.contains(event.target)) {
    closeDropdown()
  }
}

const handleTriggerKeydown = (event) => {
  if (event.key === 'Escape') {
    closeDropdown()
    return
  }

  if (!isOpen.value && (event.key === 'Enter' || event.key === ' ' || event.key === 'ArrowDown')) {
    event.preventDefault()
    openDropdown()
  }
}

watch(
  () => props.disabled,
  (nextDisabled) => {
    if (nextDisabled) {
      closeDropdown()
    }
  },
)

onMounted(() => {
  document.addEventListener('pointerdown', handleDocumentPointerDown)
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', handleDocumentPointerDown)
})
</script>

<template>
  <div
    ref="rootRef"
    class="rd-select"
    :class="{ 'rd-select--open': isOpen }"
    :style="{ width: typeof width === 'number' ? `${width}px` : width }"
  >
    <input
      v-if="name"
      type="hidden"
      :name="name"
      :value="modelValue"
    >

    <button
      :id="id || undefined"
      ref="triggerRef"
      type="button"
      class="rd-select__trigger"
      :aria-label="ariaLabel"
      aria-haspopup="listbox"
      :aria-expanded="isOpen ? 'true' : 'false'"
      :aria-controls="listboxId"
      :disabled="disabled"
      @click="toggleDropdown"
      @focus="$emit('focus', $event)"
      @blur="$emit('blur', $event)"
      @keydown="handleTriggerKeydown"
    >
      <span class="rd-select__label">{{ buttonLabel }}</span>

      <svg
        class="rd-select__icon"
        :class="{ 'rd-select__icon--open': isOpen }"
        width="16"
        height="10"
        viewBox="0 0 16 10"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
        focusable="false"
      >
        <path
          d="M1 1.5L8 8L15 1.5"
          stroke="white"
          stroke-width="1.5"
          stroke-linecap="round"
        />
      </svg>
    </button>

    <transition name="rd-select-fade">
      <ul
        v-if="isOpen"
        :id="listboxId"
        class="rd-select__menu"
        role="listbox"
        :aria-label="ariaLabel"
      >
        <li
          v-for="option in options"
          :key="String(option.value)"
          class="rd-select__option"
          :class="{
            'rd-select__option--active': String(modelValue) === String(option.value),
            'rd-select__option--disabled': Boolean(option.disabled),
          }"
          role="option"
          :aria-selected="String(modelValue) === String(option.value) ? 'true' : 'false'"
          :aria-disabled="option.disabled ? 'true' : undefined"
          @click="selectOption(option)"
        >
          {{ option.label }}
        </li>
      </ul>
    </transition>
  </div>
</template>

<style scoped>
.rd-select {
  position: relative;
  display: inline-flex;
  align-items: center;
  height: 34px;
  border-radius: 4px;
  background: var(--third-color);
  border: 1px solid var(--border-soft-color);
  box-shadow: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.rd-select:hover {
  border-color: color-mix(in srgb, white 24%, var(--border-soft-color));
}

.rd-select:focus-within,
.rd-select--open {
  box-shadow: 0 0 0 1px var(--first-color);
}

.rd-select__trigger {
  width: 100%;
  height: 100%;
  border: none;
  background: transparent;
  color: var(--foreground-third-color);
  font-size: 12px;
  font-weight: 500;
  line-height: 1;
  padding: 0 34px 0 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  text-align: left;
}

.rd-select__trigger:focus {
  outline: none;
}

.rd-select__trigger:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.rd-select__label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--foreground-third-color);
}

.rd-select__icon {
  position: absolute;
  right: 11px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  transition: transform 0.2s ease;
}

.rd-select__icon--open {
  transform: translateY(-50%) rotate(180deg);
}

.rd-select__menu {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  width: 100%;
  max-height: 220px;
  overflow-y: auto;
  margin: 0;
  padding: 6px;
  list-style: none;
  border-radius: 10px;
  border: 1px solid var(--border-soft-color);
  background: color-mix(in srgb, var(--third-color) 94%, black);
  box-shadow:
    var(--shadow-lg),
    inset 0 1px 0 color-mix(in srgb, white 7%, transparent);
  z-index: 40;
}

.rd-select__menu::-webkit-scrollbar {
  width: 8px;
}

.rd-select__menu::-webkit-scrollbar-thumb {
  background: color-mix(in srgb, var(--first-color) 28%, transparent);
  border-radius: 999px;
}

.rd-select__option {
  min-height: 34px;
  border-radius: 6px;
  padding: 8px 10px;
  color: var(--foreground-third-color);
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
}

.rd-select__option:hover {
  background: var(--surface-strong-overlay-color);
  transform: translateX(2px);
}

.rd-select__option--active {
  background: var(--first-color-soft);
  color: var(--first-color);
}

.rd-select__option--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.rd-select-fade-enter-active,
.rd-select-fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.rd-select-fade-enter-from,
.rd-select-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
