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
      Уведомления
    </SectionAccentTitle>
    <StatePanel
      title="Новых уведомлений нет"
      description="Когда появятся новые события, они отобразятся здесь."
      variant="empty"
    />
  </section>
</template>
