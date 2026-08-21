<script setup>
import NovelGridCard from '../cards/NovelGridCard.vue'

const props = defineProps({
  novels: {
    type: Array,
    default: () => [],
  },
  filtersOpen: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <div
    :class="[
      'grid items-stretch gap-2 min-[480px]:gap-2.5 sm:gap-3',
      props.filtersOpen
        ? 'grid-cols-2 min-[480px]:grid-cols-3 sm:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4'
        : 'grid-cols-2 min-[480px]:grid-cols-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5',
    ]"
  >
    <NovelGridCard v-for="item in props.novels" :key="item.id" :novel="item" />
  </div>
</template>
