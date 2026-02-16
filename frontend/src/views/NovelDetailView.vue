<script setup>
import StatePanel from '@/components/common/StatePanel.vue'
import SectionAccentTitle from '@/components/common/SectionAccentTitle.vue'

const props = defineProps({
  slug: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <section class="container mx-auto px-4 py-8 text-white">
    <SectionAccentTitle
      as="h1"
      class="mb-3"
    >
      Карточка ранобэ
    </SectionAccentTitle>
    <StatePanel
      title="Детальная страница в разработке"
      :description="`Slug: ${props.slug}`"
      variant="info"
    />
  </section>
</template>
