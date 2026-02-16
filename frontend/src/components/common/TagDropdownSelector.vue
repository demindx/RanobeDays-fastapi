<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

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
const isOpen = ref(false)
const localId = `rd-tag-select-${++instanceId}`

const normalizedModelValue = computed(() => Array.from(new Set(props.modelValue.map(String))))

const selectedSet = computed(() => new Set(normalizedModelValue.value))

const selectedOptions = computed(() =>
  props.options.filter((option) => selectedSet.value.has(String(option.value))),
)

const visibleTags = computed(() => selectedOptions.value.slice(0, props.maxVisibleTags))
const hiddenCount = computed(() => Math.max(0, selectedOptions.value.length - props.maxVisibleTags))

const baseId = computed(() => props.id || localId)
const listboxId = computed(() => `${baseId.value}-listbox`)

const closeDropdown = () => {
  isOpen.value = false
}

const toggleDropdown = () => {
  if (props.disabled) return
  isOpen.value = !isOpen.value
}

const toggleTag = (optionValue) => {
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

const handleOutsidePointer = (event) => {
  if (rootRef.value && !rootRef.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('pointerdown', handleOutsidePointer)
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', handleOutsidePointer)
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
    >
      <div class="rd-tag-select__chips">
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

    <transition name="rd-tag-select-fade">
      <ul
        v-if="isOpen"
        :id="listboxId"
        class="rd-tag-select__menu"
        role="listbox"
        :aria-label="ariaLabel"
        aria-multiselectable="true"
      >
        <li
          v-for="option in options"
          :key="String(option.value)"
          class="rd-tag-select__option"
          :class="{ 'rd-tag-select__option--active': selectedSet.has(String(option.value)) }"
          role="option"
          :aria-selected="selectedSet.has(String(option.value)) ? 'true' : 'false'"
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
  align-items: center;
  gap: 5px;
  min-width: 0;
  overflow: hidden;
}

.rd-tag-select__chip {
  display: inline-flex;
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
  max-width: 88px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rd-tag-select__chip--more {
  width: 16px;
  padding: 0;
  color: #383838;
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

.rd-tag-select__option--active {
  background: var(--first-color-soft);
  color: var(--first-color);
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
