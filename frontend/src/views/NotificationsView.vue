<script setup>
import StatePanel from '@/components/common/StatePanel.vue'
</script>

<template>
  <section class="container mx-auto px-4 py-8 text-white">
    <h1 class="text-2xl font-semibold mb-3">
      Уведомления
    </h1>
    <StatePanel
      title="Новых уведомлений нет"
      description="Когда появятся новые события, они отобразятся здесь."
      variant="empty"
    />
  </section>
</template>
