<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

let instanceId = 0

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [],
  },
  options: {
    type: Array,
    default: () => [],
  },
  id: {
    type: String,
    default: '',
  },
  ariaLabel: {
    type: String,
    default: 'Выбор тегов',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  width: {
    type: [String, Number],
    default: 229,
  },
  maxVisibleTags: {
    type: Number,
    default: 4,
  },
})

const emit = defineEmits(['update:modelValue', 'change', 'focus', 'blur'])

const rootRef = ref(null)
const triggerRef = ref(null)
const chipsViewportRef = ref(null)
const measureOverflowRef = ref(null)
const isOpen = ref(false)
const activeIndex = ref(-1)
const optionRefs = ref([])
const measureTagRefs = ref([])
const visibleCount = ref(props.maxVisibleTags)
let chipsResizeObserver = null
const localId = `rd-tag-select-${++instanceId}`

const normalizedModelValue = computed(() => Array.from(new Set(props.modelValue.map(String))))

const selectedSet = computed(() => new Set(normalizedModelValue.value))

const selectedOptions = computed(() =>
  props.options.filter((option) => selectedSet.value.has(String(option.value))),
)

const visibleTags = computed(() => selectedOptions.value.slice(0, visibleCount.value))
const hiddenCount = computed(() => Math.max(0, selectedOptions.value.length - visibleCount.value))

const baseId = computed(() => props.id || localId)
const listboxId = computed(() => `${baseId.value}-listbox`)

const enabledOptionIndexes = computed(() =>
  props.options
    .map((option, index) => ({ option, index }))
    .filter(({ option }) => !option.disabled)
    .map(({ index }) => index),
)

const setMeasureTagRef = (index, element) => {
  measureTagRefs.value[index] = element
}

const recalculateVisibleTags = () => {
  const selectedLength = selectedOptions.value.length
  if (selectedLength === 0) {
    visibleCount.value = 0
    return
  }

  const availableWidth = chipsViewportRef.value?.clientWidth ?? 0
  // In tests/SSR-like environments layout metrics are often 0.
  if (availableWidth <= 0) {
    visibleCount.value = Math.min(selectedLength, props.maxVisibleTags)
    return
  }

  const gap = 5
  const overflowWidth = measureOverflowRef.value?.offsetWidth ?? 16
  const tagWidths = selectedOptions.value.map(
    (_, index) => measureTagRefs.value[index]?.offsetWidth ?? 0,
  )

  if (tagWidths.every((width) => width <= 0) || availableWidth <= overflowWidth) {
    visibleCount.value = Math.min(selectedLength, props.maxVisibleTags)
    return
  }

  let count = 0
  let usedWidth = 0

  for (let index = 0; index < tagWidths.length; index += 1) {
    const nextWidth = count === 0 ? tagWidths[index] : usedWidth + gap + tagWidths[index]
    const hasRemaining = index < tagWidths.length - 1
    const requiredWidth = hasRemaining ? nextWidth + gap + overflowWidth : nextWidth

    if (requiredWidth <= availableWidth + 0.5) {
      usedWidth = nextWidth
      count += 1
      continue
    }

    break
  }

  if (count === 0) {
    visibleCount.value = 0
    return
  }

  visibleCount.value = count
}

const scheduleVisibleTagRecalc = () => {
  void nextTick(() => {
    recalculateVisibleTags()
  })
}

const getInitialActiveIndex = () => {
  const selectedIndex = props.options.findIndex(
    (option) => !option.disabled && selectedSet.value.has(String(option.value)),
  )
  if (selectedIndex >= 0) {
    return selectedIndex
  }
  return enabledOptionIndexes.value[0] ?? -1
}

const setOptionRef = (index, element) => {
  optionRefs.value[index] = element
}

const focusActiveOption = async () => {
  await nextTick()
  optionRefs.value[activeIndex.value]?.focus()
}

const closeDropdown = ({ focusTrigger = false } = {}) => {
  isOpen.value = false
  activeIndex.value = -1
  optionRefs.value = []
  if (focusTrigger) {
    triggerRef.value?.focus()
  }
}

const openDropdown = async ({ focusOption = true } = {}) => {
  if (props.disabled) return
  isOpen.value = true
  activeIndex.value = getInitialActiveIndex()
  if (focusOption && activeIndex.value >= 0) {
    await focusActiveOption()
  }
}

const toggleDropdown = async () => {
  if (props.disabled) return
  if (isOpen.value) {
    closeDropdown()
    return
  }
  await openDropdown()
}

const toggleTag = (optionValue) => {
  const option = props.options.find((item) => String(item.value) === String(optionValue))
  if (option?.disabled) return

  const value = String(optionValue)
  const next = [...normalizedModelValue.value]
  const index = next.indexOf(value)

  if (index >= 0) {
    next.splice(index, 1)
  } else {
    next.push(value)
  }

  emit('update:modelValue', next)
  emit('change', next)
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

const toggleActiveTag = () => {
  if (activeIndex.value < 0) return
  const option = props.options[activeIndex.value]
  if (!option || option.disabled) return
  toggleTag(option.value)
}

const handleOutsidePointer = (event) => {
  if (rootRef.value && !rootRef.value.contains(event.target)) {
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
    toggleActiveTag()
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
  [() => props.options, () => props.modelValue],
  () => {
    if (!isOpen.value) return
    activeIndex.value = getInitialActiveIndex()
  },
  { deep: true },
)

watch(
  () => selectedOptions.value.map((option) => String(option.value)),
  () => {
    measureTagRefs.value = []
    scheduleVisibleTagRecalc()
  },
  { deep: true, immediate: true },
)

watch(
  () => props.width,
  () => {
    scheduleVisibleTagRecalc()
  },
)

onMounted(() => {
  document.addEventListener('pointerdown', handleOutsidePointer)
  if (typeof ResizeObserver !== 'undefined' && chipsViewportRef.value) {
    chipsResizeObserver = new ResizeObserver(() => {
      recalculateVisibleTags()
    })
    chipsResizeObserver.observe(chipsViewportRef.value)
  }
  scheduleVisibleTagRecalc()
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', handleOutsidePointer)
  if (chipsResizeObserver) {
    chipsResizeObserver.disconnect()
  }
})
</script>

<template>
  <div
    ref="rootRef"
    class="rd-tag-select"
    :class="{ 'rd-tag-select--open': isOpen }"
    :style="{ '--rd-tag-select-width': typeof width === 'number' ? `${width}px` : width }"
  >
    <button
      :id="baseId"
      ref="triggerRef"
      type="button"
      class="rd-tag-select__trigger"
      :disabled="disabled"
      :aria-label="ariaLabel"
      aria-haspopup="listbox"
      :aria-expanded="isOpen ? 'true' : 'false'"
      :aria-controls="listboxId"
      @click="toggleDropdown"
      @focus="$emit('focus', $event)"
      @blur="$emit('blur', $event)"
      @keydown="handleTriggerKeydown"
    >
      <div
        ref="chipsViewportRef"
        class="rd-tag-select__chips"
      >
        <template v-if="visibleTags.length">
          <span
            v-for="tag in visibleTags"
            :key="String(tag.value)"
            class="rd-tag-select__chip"
          >
            {{ tag.label }}
          </span>
          <span
            v-if="hiddenCount > 0"
            class="rd-tag-select__chip rd-tag-select__chip--more"
          >
            ...
          </span>
        </template>
        <span
          v-else
          class="rd-tag-select__placeholder"
        >
          Выберите теги
        </span>
      </div>

      <svg
        class="rd-tag-select__icon"
        :class="{ 'rd-tag-select__icon--open': isOpen }"
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
          stroke-linecap="round"
          stroke-width="1.5"
        />
      </svg>
    </button>

    <div
      class="rd-tag-select__measure"
      aria-hidden="true"
    >
      <span
        v-for="(tag, index) in selectedOptions"
        :key="`measure-${String(tag.value)}`"
        :ref="(element) => setMeasureTagRef(index, element)"
        class="rd-tag-select__chip rd-tag-select__chip--measure"
      >
        {{ tag.label }}
      </span>
      <span
        ref="measureOverflowRef"
        class="rd-tag-select__chip rd-tag-select__chip--measure rd-tag-select__chip--more"
      >
        ...
      </span>
    </div>

    <transition name="rd-tag-select-fade">
      <ul
        v-if="isOpen"
        :id="listboxId"
        class="rd-tag-select__menu"
        role="listbox"
        :aria-label="ariaLabel"
        aria-multiselectable="true"
        @keydown="handleOptionKeydown"
      >
        <li
          v-for="(option, index) in options"
          :key="String(option.value)"
          :ref="(element) => setOptionRef(index, element)"
          class="rd-tag-select__option"
          :class="{
            'rd-tag-select__option--focused': activeIndex === index,
            'rd-tag-select__option--active': selectedSet.has(String(option.value)),
            'rd-tag-select__option--disabled': Boolean(option.disabled),
          }"
          role="option"
          :tabindex="activeIndex === index ? 0 : -1"
          :aria-selected="selectedSet.has(String(option.value)) ? 'true' : 'false'"
          :aria-disabled="option.disabled ? 'true' : undefined"
          @mousemove="handleOptionMouseMove(index)"
          @focus="activeIndex = index"
          @click="toggleTag(option.value)"
        >
          <span>{{ option.label }}</span>
          <span
            v-if="selectedSet.has(String(option.value))"
            class="rd-tag-select__check"
            aria-hidden="true"
          >
            ✓
          </span>
        </li>
      </ul>
    </transition>
  </div>
</template>

<style scoped>
.rd-tag-select {
  position: relative;
  display: inline-flex;
  width: min(100%, var(--rd-tag-select-width));
  max-width: 100%;
  align-items: center;
  height: 34px;
  border-radius: 4px;
  background: var(--third-color);
  border: 1px solid var(--border-soft-color);
  box-shadow: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.rd-tag-select:hover {
  border-color: color-mix(in srgb, white 24%, var(--border-soft-color));
}

.rd-tag-select:focus-within,
.rd-tag-select--open {
  box-shadow: 0 0 0 1px var(--first-color);
}

.rd-tag-select__trigger {
  width: 100%;
  min-width: 0;
  height: 100%;
  border: none;
  background: transparent;
  padding: 0 30px 0 4px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  cursor: pointer;
  overflow: hidden;
}

.rd-tag-select__trigger:focus {
  outline: none;
}

.rd-tag-select__trigger:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.rd-tag-select__chips {
  display: flex;
  flex: 1 1 auto;
  align-items: center;
  gap: 5px;
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
}

.rd-tag-select__chip {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  height: 14px;
  padding: 0 7px;
  border-radius: 7px;
  background: #c3e57e;
  color: #494949;
  font-size: 9px;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
}

.rd-tag-select__chip--more {
  flex: 0 0 auto;
  min-width: 16px;
  width: auto;
  padding: 0 5px;
  color: #383838;
}

.rd-tag-select__measure {
  position: absolute;
  inset: auto auto 0 0;
  display: flex;
  align-items: center;
  gap: 5px;
  visibility: hidden;
  pointer-events: none;
  white-space: nowrap;
}

.rd-tag-select__chip--measure {
  width: auto;
  max-width: none;
}

.rd-tag-select__placeholder {
  color: var(--foreground-secondary-color);
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rd-tag-select__icon {
  position: absolute;
  right: 11px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s ease;
  pointer-events: none;
}

.rd-tag-select__icon--open {
  transform: translateY(-50%) rotate(180deg);
}

.rd-tag-select__menu {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  width: 100%;
  margin: 0;
  padding: 6px;
  list-style: none;
  border-radius: 10px;
  border: 1px solid var(--border-soft-color);
  background: color-mix(in srgb, var(--third-color) 94%, black);
  box-shadow:
    var(--shadow-lg),
    inset 0 1px 0 color-mix(in srgb, white 7%, transparent);
  max-height: 220px;
  overflow-y: auto;
  z-index: 40;
}

.rd-tag-select__menu::-webkit-scrollbar {
  width: 8px;
}

.rd-tag-select__menu::-webkit-scrollbar-thumb {
  background: color-mix(in srgb, var(--first-color) 28%, transparent);
  border-radius: 999px;
}

.rd-tag-select__option {
  min-height: 30px;
  border-radius: 6px;
  padding: 6px 8px;
  color: var(--foreground-third-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.15s ease;
  overflow: hidden;
}

.rd-tag-select__option > span:first-child {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rd-tag-select__option:hover {
  background: var(--surface-strong-overlay-color);
  transform: translateX(2px);
}

.rd-tag-select__option--focused,
.rd-tag-select__option:focus-visible {
  outline: none;
  background: var(--surface-strong-overlay-color);
}

.rd-tag-select__option--active {
  background: var(--first-color-soft);
  color: var(--first-color);
}

.rd-tag-select__option--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.rd-tag-select__check {
  margin-left: 8px;
}

.rd-tag-select-fade-enter-active,
.rd-tag-select-fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.rd-tag-select-fade-enter-from,
.rd-tag-select-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (max-width: 767px) {
  .rd-tag-select {
    width: 100%;
  }
}
</style>
