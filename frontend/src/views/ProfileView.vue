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
      Профиль
    </SectionAccentTitle>
    <StatePanel
      title="Раздел в разработке"
      description="Профиль пользователя будет доступен после интеграции API."
      variant="info"
    />
  </section>
</template>
