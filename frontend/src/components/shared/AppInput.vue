<script setup>
const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: undefined,
  },
  value: {
    type: [String, Number],
    default: undefined,
  },
})

const emit = defineEmits(['update:modelValue', 'input'])

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
  emit('input', event)
}
</script>

<template>
  <input
    :value="props.modelValue ?? props.value"
    class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white outline-none transition focus:border-lime-300"
    v-bind="$attrs"
    @input="handleInput"
  />
</template>
