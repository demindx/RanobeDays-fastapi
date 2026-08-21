<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  options: {
    type: Array,
    default: () => [],
  },
  includeState: {
    type: Array,
    default: () => [],
  },
  excludeState: {
    type: Array,
    default: () => [],
  },
  searchable: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle'])

const open = ref(false)
const query = ref('')

const toggleOpen = () => {
  open.value = !open.value
}

const totalActive = computed(() => props.includeState.length + props.excludeState.length)

const filteredOptions = computed(() => {
  if (!props.searchable || !query.value.trim()) return props.options
  const q = query.value.toLowerCase()
  return props.options.filter((o) => String(o).toLowerCase().includes(q))
})

const pillState = (option) => {
  if (props.includeState.includes(option)) return 'include'
  if (props.excludeState.includes(option)) return 'exclude'
  return 'off'
}

const handleClick = (option) => {
  const state = pillState(option)
  if (state === 'off') {
    emit('toggle', 'include', option)
  } else if (state === 'include') {
    emit('toggle', 'exclude', option)
  } else {
    emit('toggle', 'exclude', option)
  }
}
</script>

<template>
  <div class="px-3 py-2">
    <button
      type="button"
      class="flex w-full cursor-pointer items-center justify-between gap-2 py-1 text-left"
      @click="toggleOpen"
    >
      <span class="text-sm text-zinc-300">{{ props.title }}</span>
      <div class="flex items-center gap-2">
        <span v-if="totalActive" class="text-[11px] text-zinc-500">{{ totalActive }}</span>
        <svg
          :class="['h-3 w-3 text-zinc-600 transition-transform', open ? 'rotate-90' : '']"
          viewBox="0 0 12 12"
          fill="none"
        >
          <path
            d="M4.5 2.5L7.5 6L4.5 9.5"
            stroke="currentColor"
            stroke-width="1.2"
            stroke-linecap="round"
          />
        </svg>
      </div>
    </button>

    <div v-if="open" class="mt-2 space-y-2">
      <input
        v-if="props.searchable"
        v-model="query"
        type="text"
        placeholder="Поиск..."
        class="w-full rounded-lg border border-zinc-700 bg-zinc-800/50 px-2.5 py-1.5 text-xs text-zinc-200 outline-none transition placeholder:text-zinc-600 focus:border-zinc-600"
      />

      <div class="flex max-h-48 flex-wrap gap-1.5 overflow-y-auto">
        <button
          v-for="option in filteredOptions"
          :key="String(option)"
          type="button"
          :class="[
            'rounded-md border px-2.5 py-1 text-xs transition active:scale-95',
            pillState(option) === 'include'
              ? 'border-emerald-500/40 bg-emerald-500/15 text-emerald-300'
              : pillState(option) === 'exclude'
                ? 'border-rose-500/40 bg-rose-500/15 text-rose-300'
                : 'border-zinc-700 bg-zinc-800/50 text-zinc-400 hover:border-zinc-600 hover:text-zinc-300',
          ]"
          @click="handleClick(option)"
        >
          <span v-if="pillState(option) === 'include'" class="mr-0.5">+</span>
          <span v-else-if="pillState(option) === 'exclude'" class="mr-0.5">−</span>
          {{ option }}
        </button>
      </div>
    </div>
  </div>
</template>
