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
  <div class="grid gap-4 lg:grid-cols-12">
    <div class="lg:col-span-8 xl:col-span-9">
      <slot name="content" />
    </div>

    <div class="hidden lg:col-span-4 lg:block xl:col-span-3">
      <slot name="filters" />
    </div>
  </div>

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
        'absolute right-0 top-0 h-full w-[88%] max-w-sm overflow-y-auto border-l border-zinc-700 bg-zinc-900 p-3 shadow-2xl transition-transform',
        props.filtersOpen ? 'translate-x-0' : 'translate-x-full',
      ]"
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
</template>
