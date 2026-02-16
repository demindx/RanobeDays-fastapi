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
      Закладки
    </SectionAccentTitle>
    <StatePanel
      title="Пусто"
      description="Список закладок пока пуст. Добавьте ранобэ из каталога."
      variant="empty"
    />
  </section>
</template>
