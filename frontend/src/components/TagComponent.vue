<template>
  <router-link :to="`/catalog?tag=${id}`" class="no-underline">
    <div class="inline-block px-2 py-0.5 rounded-full bg-[#C3E57E] text-[#494949] text-xs font-medium hover:bg-opacity-90 transition-colors cursor-pointer">
      {{ name }}
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true
  },
  id: {
    type: [String, Number],
    required: true
  }
});
</script>
