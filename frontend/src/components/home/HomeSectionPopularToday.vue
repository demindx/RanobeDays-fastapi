<script setup>
import NovelHeroCarousel from '@/components/novel/NovelHeroCarousel.vue'
import StatePanel from '@/components/common/StatePanel.vue'

defineProps({
  items: {
    type: Array,
    default: () => [],
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

defineEmits(['retry'])
</script>

<template>
  <section class="home-popular">
    <StatePanel
      v-if="error"
      title="Ошибка загрузки"
      :description="error"
      variant="error"
      action-label="Повторить"
      @action="$emit('retry')"
    />

    <div
      v-else-if="isLoading"
      class="home-popular__skeleton"
      aria-busy="true"
    />

    <StatePanel
      v-else-if="items.length === 0"
      title="Популярных новел пока нет"
      description="Вернитесь позже, рейтинг обновляется ежедневно."
      variant="empty"
    />

    <NovelHeroCarousel
      v-else
      :novels="items"
      title="Популярные новелы за сегодня"
    />
  </section>
</template>

<style scoped>
.home-popular {
  min-width: 0;
  width: 100%;
}

.home-popular__skeleton {
  height: 280px;
  border-radius: 12px;
  background: linear-gradient(
    110deg,
    var(--surface-elevated-color) 8%,
    var(--surface-hover-color) 18%,
    var(--surface-elevated-color) 33%
  );
  background-size: 200% 100%;
  animation: home-shimmer 1.4s linear infinite;
}

@keyframes home-shimmer {
  to {
    background-position: -200% 0;
  }
}

</style>
