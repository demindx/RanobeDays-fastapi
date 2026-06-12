<script setup>
import NovelListCard from '../cards/NovelListCard.vue'

const props = defineProps({
  novels: {
    type: Array,
    default: () => [],
  },
  onTagClick: {
    type: Function,
    default: null,
  },
})
</script>

<template>
  <div class="space-y-3">
    <NovelListCard
      v-for="item in props.novels"
      :key="item.id"
      :novel="item"
      :on-tag-click="props.onTagClick"
    />
  </div>
</template>
