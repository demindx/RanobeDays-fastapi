<script setup>
import StatePanel from '@/components/common/StatePanel.vue'
import SectionAccentTitle from '@/components/common/SectionAccentTitle.vue'
</script>

<template>
  <section class="container mx-auto px-4 py-8 text-white">
    <SectionAccentTitle
      as="h1"
      class="mb-3"
    >
      Топ
    </SectionAccentTitle>
    <StatePanel
      title="Топ ранобэ"
      description="Раздел топа подготовлен. Данные рейтинга будут подключены на следующем шаге."
      variant="info"
    />
  </section>
</template>
