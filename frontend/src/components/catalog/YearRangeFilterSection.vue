<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  filterState: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['change'])

const open = ref(false)

const toggleOpen = () => {
  open.value = !open.value
}

const activeCount = computed(() => {
  let count = 0
  if (props.filterState.from) count += 1
  if (props.filterState.to) count += 1
  return count
})
</script>

<template>
  <div class="px-3 py-2">
    <button
      type="button"
      class="flex w-full cursor-pointer items-center justify-between gap-2 py-1 text-left"
      @click="toggleOpen"
    >
      <span class="text-sm text-zinc-300">Год выпуска</span>
      <div class="flex items-center gap-2">
        <span v-if="activeCount" class="text-[11px] text-zinc-500">{{ activeCount }}</span>
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

    <div v-if="open" class="mt-2 grid grid-cols-2 gap-2">
      <div>
        <label class="mb-1 block text-xs text-zinc-500">От</label>
        <input
          :value="props.filterState.from"
          type="number"
          inputmode="numeric"
          placeholder="2020"
          min="1900"
          max="2100"
          class="w-full rounded-lg border border-zinc-700 bg-zinc-800/50 px-2.5 py-1.5 text-xs text-zinc-200 outline-none transition placeholder:text-zinc-600 focus:border-zinc-600"
          @input="emit('change', 'from', $event.target.value)"
        />
      </div>
      <div>
        <label class="mb-1 block text-xs text-zinc-500">До</label>
        <input
          :value="props.filterState.to"
          type="number"
          inputmode="numeric"
          placeholder="2025"
          min="1900"
          max="2100"
          class="w-full rounded-lg border border-zinc-700 bg-zinc-800/50 px-2.5 py-1.5 text-xs text-zinc-200 outline-none transition placeholder:text-zinc-600 focus:border-zinc-600"
          @input="emit('change', 'to', $event.target.value)"
        />
      </div>
    </div>
  </div>
</template>
