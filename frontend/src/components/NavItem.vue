<template>
  <router-link
    :to="to"
    class="text-white font-medium hover:text-[#C4FF61] transition-colors duration-200"
    active-class="text-[#C4FF61]"
  >
    {{ name }}
  </router-link>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true
  },
  to: {
    type: String,
    required: true
  }
});
</script>
