<script setup>
import { computed, ref } from 'vue'
import { useClickOutside } from '../../composables/useClickOutside'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  options: {
    type: Array,
    default: () => [],
  },
  placeholder: {
    type: String,
    default: 'Выберите значение',
  },
  variant: {
    type: String,
    default: 'green',
  },
  actionLabel: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue', 'change', 'action'])

const rootRef = ref(null)
const isOpen = ref(false)
const normalizedValue = computed(() => (props.modelValue == null ? '' : String(props.modelValue)))
const selectedOption = computed(
  () => props.options.find((option) => String(option.value) === normalizedValue.value) || null,
)
const displayLabel = computed(() => selectedOption.value?.label || props.placeholder)

const triggerClass = computed(() => {
  if (props.variant === 'green') {
    return 'border-emerald-300/60 bg-emerald-500/15 text-emerald-100 hover:border-lime-300/70 hover:bg-emerald-400/20'
  }
  return 'border-zinc-700 bg-zinc-800 text-zinc-100 hover:border-zinc-600 hover:bg-zinc-700/80'
})

const menuClass = computed(() => {
  if (props.variant === 'green') {
    return 'border-emerald-300/45 bg-zinc-900/95'
  }
  return 'border-zinc-700 bg-zinc-900/95'
})

const itemClass = computed(() => {
  if (props.variant === 'green') {
    return 'text-zinc-100 hover:bg-emerald-400/20 hover:text-emerald-100'
  }
  return 'text-zinc-100 hover:bg-zinc-800 hover:text-white'
})

const selectedItemClass = computed(() => {
  if (props.variant === 'green') {
    return 'border-emerald-300/50 bg-emerald-400/20 text-emerald-100'
  }
  return 'border-zinc-500/70 bg-zinc-700/80 text-white'
})

const toggleOpen = () => {
  if (!props.options.length && !props.actionLabel) return
  isOpen.value = !isOpen.value
}

const close = () => {
  isOpen.value = false
}

const selectOption = (option) => {
  const value = String(option.value)
  emit('update:modelValue', value)
  emit('change', value)
  close()
}

const handleAction = () => {
  emit('action')
  close()
}

useClickOutside(rootRef, isOpen, close)
</script>

<template>
  <div ref="rootRef" class="relative">
    <button
      type="button"
      :class="[
        'flex w-full cursor-pointer items-center justify-between gap-2 rounded-lg border px-3 py-2 text-sm outline-none transition focus-visible:ring-2 focus-visible:ring-lime-300/60',
        triggerClass,
      ]"
      :aria-expanded="isOpen"
      @click="toggleOpen"
    >
      <span :class="selectedOption ? '' : 'text-zinc-400'">{{ displayLabel }}</span>
      <svg
        class="h-4 w-4 shrink-0 transition duration-200"
        :class="isOpen ? 'rotate-180 text-lime-300' : 'text-zinc-400'"
        viewBox="0 0 20 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M5 7.5L10 12.5L15 7.5"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>

    <div
      v-if="isOpen"
      :class="[
        'absolute z-20 mt-2 w-full overflow-hidden rounded-xl border p-1 shadow-xl shadow-black/30 backdrop-blur',
        menuClass,
      ]"
    >
      <button
        v-for="option in props.options"
        :key="String(option.value)"
        type="button"
        :class="[
          'flex w-full cursor-pointer items-center justify-between rounded-lg border border-transparent px-3 py-2 text-left text-sm transition',
          itemClass,
          String(option.value) === normalizedValue ? selectedItemClass : '',
        ]"
        @click="selectOption(option)"
      >
        <span class="truncate">{{ option.label }}</span>
        <span
          v-if="String(option.value) === normalizedValue"
          class="ml-2 text-xs font-semibold text-lime-300"
        >
          Выбрано
        </span>
      </button>

      <button
        v-if="props.actionLabel"
        type="button"
        class="mt-1 flex w-full cursor-pointer items-center justify-center rounded-lg border border-rose-300/45 bg-rose-400/15 px-3 py-2 text-sm font-medium text-rose-200 transition hover:bg-rose-400/25"
        @click="handleAction"
      >
        {{ props.actionLabel }}
      </button>
    </div>
  </div>
</template>
