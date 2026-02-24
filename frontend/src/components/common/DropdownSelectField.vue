<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

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
const activeIndex = ref(-1)
const optionRefs = ref([])

const listboxId = computed(() => `${props.id || 'rd-select'}-listbox`)

const selectedOption = computed(() =>
  props.options.find((option) => String(option.value) === String(props.modelValue)),
)

const buttonLabel = computed(() => selectedOption.value?.label || props.placeholder)
const enabledOptionIndexes = computed(() =>
  props.options
    .map((option, index) => ({ option, index }))
    .filter(({ option }) => !option.disabled)
    .map(({ index }) => index),
)

const getInitialActiveIndex = () => {
  const selectedIndex = props.options.findIndex(
    (option) => !option.disabled && String(option.value) === String(props.modelValue),
  )
  if (selectedIndex >= 0) {
    return selectedIndex
  }
  return enabledOptionIndexes.value[0] ?? -1
}

const focusActiveOption = async () => {
  await nextTick()
  optionRefs.value[activeIndex.value]?.focus()
}

const setOptionRef = (index, element) => {
  optionRefs.value[index] = element
}

const openDropdown = async ({ focusOption = true } = {}) => {
  if (props.disabled) return
  isOpen.value = true
  activeIndex.value = getInitialActiveIndex()
  if (focusOption && activeIndex.value >= 0) {
    await focusActiveOption()
  }
}

const closeDropdown = ({ focusTrigger = false } = {}) => {
  isOpen.value = false
  activeIndex.value = -1
  optionRefs.value = []
  if (focusTrigger) {
    triggerRef.value?.focus()
  }
}

const toggleDropdown = () => {
  if (props.disabled) return
  if (isOpen.value) {
    closeDropdown()
    return
  }
  void openDropdown()
}

const selectOption = (option) => {
  if (option.disabled) return
  emit('update:modelValue', option.value)
  emit('change', option.value)
  closeDropdown({ focusTrigger: true })
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
    void openDropdown()
    return
  }

  if (!isOpen.value && event.key === 'ArrowUp') {
    event.preventDefault()
    void openDropdown()
    nextTick(() => {
      const lastIndex = enabledOptionIndexes.value.at(-1) ?? -1
      if (lastIndex >= 0) {
        activeIndex.value = lastIndex
        void focusActiveOption()
      }
    })
  }
}

const moveActive = (step) => {
  const enabledIndexes = enabledOptionIndexes.value
  if (!enabledIndexes.length) return

  const currentPos = enabledIndexes.indexOf(activeIndex.value)
  const basePos = currentPos >= 0 ? currentPos : 0
  const nextPos = (basePos + step + enabledIndexes.length) % enabledIndexes.length
  activeIndex.value = enabledIndexes[nextPos]
  void focusActiveOption()
}

const moveToBoundary = (direction) => {
  const enabledIndexes = enabledOptionIndexes.value
  if (!enabledIndexes.length) return

  activeIndex.value = direction === 'start' ? enabledIndexes[0] : enabledIndexes.at(-1)
  void focusActiveOption()
}

const selectActiveOption = () => {
  if (activeIndex.value < 0) return
  const option = props.options[activeIndex.value]
  if (!option || option.disabled) return
  selectOption(option)
}

const handleOptionMouseMove = (index) => {
  if (props.options[index]?.disabled) return
  activeIndex.value = index
}

const handleOptionKeydown = (event) => {
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    moveActive(1)
    return
  }

  if (event.key === 'ArrowUp') {
    event.preventDefault()
    moveActive(-1)
    return
  }

  if (event.key === 'Home') {
    event.preventDefault()
    moveToBoundary('start')
    return
  }

  if (event.key === 'End') {
    event.preventDefault()
    moveToBoundary('end')
    return
  }

  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault()
    selectActiveOption()
    return
  }

  if (event.key === 'Escape') {
    event.preventDefault()
    closeDropdown({ focusTrigger: true })
    return
  }

  if (event.key === 'Tab') {
    closeDropdown()
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

watch(
  [() => props.options, () => props.modelValue],
  () => {
    if (!isOpen.value) return
    activeIndex.value = getInitialActiveIndex()
  },
  { deep: true },
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
    :style="{ '--rd-select-width': typeof width === 'number' ? `${width}px` : width }"
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
        @keydown="handleOptionKeydown"
      >
        <li
          v-for="(option, index) in options"
          :key="String(option.value)"
          :ref="(element) => setOptionRef(index, element)"
          class="rd-select__option"
          :class="{
            'rd-select__option--focused': activeIndex === index,
            'rd-select__option--active': String(modelValue) === String(option.value),
            'rd-select__option--disabled': Boolean(option.disabled),
          }"
          role="option"
          :tabindex="activeIndex === index ? 0 : -1"
          :aria-selected="String(modelValue) === String(option.value) ? 'true' : 'false'"
          :aria-disabled="option.disabled ? 'true' : undefined"
          @mousemove="handleOptionMouseMove(index)"
          @focus="activeIndex = index"
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
  width: min(100%, var(--rd-select-width));
  max-width: 100%;
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
  min-width: 0;
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
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rd-select__option:hover {
  background: var(--surface-strong-overlay-color);
  transform: translateX(2px);
}

.rd-select__option--focused,
.rd-select__option:focus-visible {
  outline: none;
  background: var(--surface-strong-overlay-color);
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

@media (max-width: 767px) {
  .rd-select {
    width: 100%;
  }
}
</style>
