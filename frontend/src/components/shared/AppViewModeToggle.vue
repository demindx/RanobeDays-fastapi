<script setup>
const props = defineProps({
  modelValue: { type: String, default: 'grid' },
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <div class="flex shrink-0 rounded-lg border border-zinc-700 bg-zinc-800 p-0.5">
    <button
      type="button"
      :class="[
        'cursor-pointer rounded-md px-3 py-1.5 text-xs transition active:scale-95',
        props.modelValue === 'grid'
          ? 'bg-lime-300 font-semibold text-zinc-900'
          : 'text-zinc-300 hover:bg-zinc-700',
      ]"
      @click="emit('update:modelValue', 'grid')"
    >
      Сетка
    </button>
    <button
      type="button"
      :class="[
        'cursor-pointer rounded-md px-3 py-1.5 text-xs transition active:scale-95',
        props.modelValue === 'list'
          ? 'bg-lime-300 font-semibold text-zinc-900'
          : 'text-zinc-300 hover:bg-zinc-700',
      ]"
      @click="emit('update:modelValue', 'list')"
    >
      Список
    </button>
  </div>
</template>
