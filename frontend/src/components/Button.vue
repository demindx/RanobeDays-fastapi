<script setup>
const props = defineProps({
  callback: {
    type: Function,
    default: null
  },
  disabled: {
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <button
    class="bg-[#C4FF61] hover:bg-[#b3e659] text-[#494949] font-medium py-2 px-6 rounded-full transition-colors duration-200"
    :class="{'opacity-50 cursor-not-allowed': disabled}"
    :disabled="disabled"
    @click="callback"
  >
    <slot/>
  </button>
</template>
