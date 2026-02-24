<script setup>
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import SearchIcon from '../icons/SearchIcon.vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Поиск...',
  },
  ariaLabel: {
    type: String,
    default: 'Поиск по ранобэ',
  },
  debounce: {
    type: Number,
    default: 300,
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  clearable: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue', 'search', 'clear'])

const inputValue = ref(props.modelValue)
const isFocused = ref(false)
let debounceTimer = null

watch(
  () => props.modelValue,
  (newVal) => {
    inputValue.value = newVal
  },
)

const sizeClass = computed(() => `search-bar--${props.size}`)

const handleInput = (event) => {
  const value = event.target.value
  inputValue.value = value
  emit('update:modelValue', value)

  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }

  if (props.debounce > 0) {
    debounceTimer = setTimeout(() => {
      emit('search', value)
    }, props.debounce)
  }
}

const handleSearch = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  emit('search', inputValue.value)
}

const handleClear = () => {
  inputValue.value = ''
  emit('update:modelValue', '')
  emit('clear')
}

const handleKeydown = (event) => {
  if (event.key === 'Enter') {
    handleSearch()
  } else if (event.key === 'Escape') {
    handleClear()
  }
}

onBeforeUnmount(() => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
})
</script>

<template>
  <div
    class="search-bar"
    :class="[sizeClass, { 'search-bar--focused': isFocused }]"
  >
    <input
      type="text"
      :value="inputValue"
      :placeholder="placeholder"
      :aria-label="ariaLabel"
      class="search-bar__input"
      @input="handleInput"
      @focus="isFocused = true"
      @blur="isFocused = false"
      @keydown="handleKeydown"
    >

    <div class="search-bar__actions">
      <button
        v-if="clearable && inputValue"
        class="search-bar__clear"
        type="button"
        aria-label="Очистить"
        @click="handleClear"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clip-rule="evenodd"
          />
        </svg>
      </button>

      <button
        class="search-bar__submit"
        type="button"
        aria-label="Поиск"
        @click="handleSearch"
      >
        <SearchIcon />
      </button>
    </div>
  </div>
</template>

<style scoped>
.search-bar {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
}

.search-bar__input {
  width: 100%;
  border: none;
  border-radius: 9999px;
  background: var(--secondary-color);
  color: var(--foreground-color);
  transition: all 0.2s ease;
}

.search-bar__input::placeholder {
  color: var(--foreground-placeholder-color);
}

.search-bar__input:focus {
  outline: none;
}

.search-bar--sm .search-bar__input {
  padding: 0.375rem 2.5rem 0.375rem 1rem;
  font-size: 0.75rem;
}

.search-bar--md .search-bar__input {
  padding: 0.5rem 3rem 0.5rem 1.25rem;
  font-size: 0.875rem;
}

.search-bar--lg .search-bar__input {
  padding: 0.75rem 3.5rem 0.75rem 1.5rem;
  font-size: 1rem;
}

.search-bar--focused .search-bar__input {
  box-shadow: 0 0 0 3px var(--focus-ring-color);
}

.search-bar__actions {
  position: absolute;
  right: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.search-bar__submit,
.search-bar__clear {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--foreground-color);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.search-bar__submit:hover {
  background: var(--surface-strong-overlay-color);
}

.search-bar__clear:hover {
  color: var(--danger-color);
  background: var(--danger-soft-color);
}

.search-bar__input:focus-visible,
.search-bar__submit:focus-visible,
.search-bar__clear:focus-visible {
  outline: 2px solid var(--first-color);
  outline-offset: 2px;
}
</style>
