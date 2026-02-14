<script setup>
import StatePanel from '@/components/common/StatePanel.vue'

const props = defineProps({
  slug: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <section class="container mx-auto px-4 py-8 text-white">
    <h1 class="text-2xl font-semibold mb-3">
      Карточка ранобэ
    </h1>
    <StatePanel
      title="Детальная страница в разработке"
      :description="`Slug: ${props.slug}`"
      variant="info"
    />
  </section>
</template>
