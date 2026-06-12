<script setup>
const props = defineProps({
  filtersOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close-filters'])
</script>

<template>
  <div class="flex gap-4">
    <div class="min-w-0 flex-1">
      <slot name="content" />
    </div>

    <!-- Desktop filter sidebar -->
    <div
      class="hidden shrink-0 self-start transition-all duration-300 ease-in-out lg:block"
      :class="[
        props.filtersOpen ? 'w-72 sticky top-3' : 'w-0 overflow-hidden',
      ]"
    >
      <div v-show="props.filtersOpen" class="w-72">
        <slot name="filters" />
      </div>
    </div>

    <!-- Mobile/tablet overlay -->
    <div
      :class="[
        'fixed inset-0 z-50 lg:hidden',
        props.filtersOpen ? 'pointer-events-auto' : 'pointer-events-none',
      ]"
    >
      <div
        :class="[
          'absolute inset-0 bg-black/50 transition-opacity',
          props.filtersOpen ? 'opacity-100' : 'opacity-0',
        ]"
        @click="emit('close-filters')"
      />
      <div
        :class="[
          'absolute right-0 top-0 h-full max-w-sm overflow-y-auto border-l border-zinc-700 bg-zinc-900 p-3 shadow-2xl transition-transform',
          props.filtersOpen ? 'translate-x-0' : 'translate-x-full',
        ]"
        class="w-[88%]"
      >
        <div class="mb-3 flex items-center justify-between">
          <h2 class="text-base font-semibold text-white">Фильтры</h2>
          <button
            type="button"
            class="cursor-pointer rounded-md border border-zinc-700 px-2 py-1 text-xs text-zinc-300 transition hover:bg-zinc-800 active:scale-95"
            @click="emit('close-filters')"
          >
            Закрыть
          </button>
        </div>
        <slot name="filters" />
      </div>
    </div>
  </div>
</template>
