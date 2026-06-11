<script setup>
import { computed, ref } from 'vue'
import ChevronRightIcon from '../icons/ChevronRightIcon.vue'
import AppInput from '../shared/AppInput.vue'
import AppPanel from '../shared/AppPanel.vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  mode: {
    type: String,
    default: 'include',
    validator: (value) => ['include', 'exclude'].includes(value),
  },
  options: {
    type: Array,
    default: () => [],
  },
  filterState: {
    type: Object,
    required: true,
  },
  searchable: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle'])
const query = ref('')
const isOpen = ref(false)

const activeCount = computed(() => props.filterState[props.mode].length)

const filteredOptions = computed(() => {
  if (!props.searchable || !query.value.trim()) return props.options
  const lower = query.value.toLowerCase()
  return props.options.filter((item) => String(item).toLowerCase().includes(lower))
})

const isSelected = (option) => props.filterState[props.mode].includes(option)

const toggleOption = (option) => {
  emit('toggle', props.mode, option)
}
</script>

<template>
  <AppPanel as="section">
    <button
      type="button"
      class="flex w-full cursor-pointer items-center justify-between gap-2 rounded-lg px-1 py-1 text-left transition hover:bg-zinc-800/50 active:scale-[0.99]"
      @click="isOpen = !isOpen"
    >
      <div class="min-w-0">
        <h3 class="text-sm font-semibold text-white">{{ props.title }}</h3>
      </div>
      <div class="flex items-center gap-2">
        <span
          v-if="activeCount"
          :class="[
            'rounded-full px-2 py-0.5 text-[11px] font-semibold',
            props.mode === 'include' ? 'bg-lime-300 text-zinc-900' : 'bg-rose-300 text-rose-950',
          ]"
        >
          {{ activeCount }}
        </span>
        <ChevronRightIcon
          :class="['text-zinc-400 transition-transform', isOpen ? 'rotate-90' : 'rotate-0']"
        />
      </div>
    </button>

    <div v-if="isOpen" class="mt-2">
      <AppInput
        v-if="props.searchable"
        v-model="query"
        type="text"
        placeholder="Поиск..."
        class="mb-2 w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-xs text-white outline-none transition focus:border-lime-300"
      />

      <div class="max-h-52 overflow-y-auto pr-1">
        <div class="flex flex-wrap gap-1.5">
          <button
            v-for="option in filteredOptions"
            :key="String(option)"
            type="button"
            :class="[
              'cursor-pointer rounded-full border px-2.5 py-1 text-xs transition active:scale-95',
              isSelected(option)
                ? props.mode === 'include'
                  ? 'border-emerald-400 bg-emerald-400/20 text-emerald-300'
                  : 'border-rose-400 bg-rose-400/20 text-rose-300'
                : props.mode === 'include'
                  ? 'border-zinc-700 bg-zinc-800 text-zinc-200 hover:border-lime-300/60 hover:bg-zinc-700'
                  : 'border-zinc-700 bg-zinc-800 text-zinc-200 hover:border-rose-300/60 hover:bg-zinc-700',
            ]"
            @click="toggleOption(option)"
          >
            {{ option }}
          </button>
        </div>
      </div>
    </div>
  </AppPanel>
</template>
