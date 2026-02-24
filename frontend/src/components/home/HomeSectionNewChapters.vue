<script setup>
import StatePanel from '@/components/common/StatePanel.vue'
import NovelHeroCarousel from '@/components/novel/NovelHeroCarousel.vue'

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

defineEmits(['retry', 'open-item'])
</script>

<template>
  <section class="home-section">
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
      class="chapters-loading"
      aria-busy="true"
    >
      <div
        v-for="index in 5"
        :key="index"
        class="chapter-skeleton"
      />
    </div>

    <StatePanel
      v-else-if="items.length === 0"
      title="Новых глав пока нет"
      description="Проверьте позже, обновления скоро появятся."
      variant="empty"
    />

    <div
      v-else
      class="chapters-carousel-wrapper"
    >
      <NovelHeroCarousel
        :novels="items"
        title="Новые главы сегодня"
      />
    </div>
  </section>
</template>

<style scoped>
.home-section {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  min-width: 0;
}

.chapters-loading {
  display: flex;
  gap: 0.8rem;
  min-width: 0;
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  padding-bottom: 0.45rem;
}

.chapters-carousel-wrapper {
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  border-radius: 14px;
}

.chapter-skeleton {
  flex: 0 0 auto;
  width: 178px;
  height: 320px;
  border-radius: 10px;
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
