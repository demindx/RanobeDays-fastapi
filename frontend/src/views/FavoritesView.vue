<script setup>
import StatePanel from '@/components/common/StatePanel.vue'
</script>

<template>
  <section class="container mx-auto px-4 py-8 text-white">
    <h1 class="text-2xl font-semibold mb-3">
      Закладки
    </h1>
    <StatePanel
      title="Пусто"
      description="Список закладок пока пуст. Добавьте ранобэ из каталога."
      variant="empty"
    />
  </section>
</template>
