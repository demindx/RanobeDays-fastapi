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
      Вход
    </SectionAccentTitle>
    <StatePanel
      title="Форма входа в работе"
      description="Экран авторизации будет добавлен в следующей итерации."
      variant="info"
    />
  </section>
</template>
