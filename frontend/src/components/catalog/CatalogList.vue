<script setup>
import NovelListCard from '../cards/NovelListCard.vue'

const props = defineProps({
  novels: {
    type: Array,
    default: () => [],
  },
})
</script>

<template>
  <div class="space-y-3">
    <NovelListCard v-for="item in props.novels" :key="item.id" :novel="item" />
  </div>
</template>
