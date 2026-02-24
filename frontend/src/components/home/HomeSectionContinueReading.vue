<script setup>
import SectionAccentTitle from '@/components/common/SectionAccentTitle.vue'
import StatePanel from '@/components/common/StatePanel.vue'
import HomeContinueReadingCard from '@/components/home/HomeContinueReadingCard.vue'

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
  isLoggedIn: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['retry', 'open-item', 'login'])
</script>

<template>
  <section class="home-section">
    <div class="home-section__header">
      <SectionAccentTitle as="h1">
        Продолжить чтение
      </SectionAccentTitle>
    </div>

    <StatePanel
      v-if="!isLoggedIn"
      title="Войдите, чтобы продолжить чтение"
      description="Синхронизируйте прогресс, чтобы возвращаться к последней главе в один клик."
      variant="info"
      action-label="Войти"
      @action="$emit('login')"
    />

    <StatePanel
      v-else-if="error"
      title="Ошибка загрузки"
      :description="error"
      variant="error"
      action-label="Повторить"
      @action="$emit('retry')"
    />

    <div
      v-else-if="isLoading"
      class="continue-grid"
      aria-busy="true"
    >
      <div
        v-for="index in 4"
        :key="index"
        class="continue-card continue-card--skeleton"
      />
    </div>

    <StatePanel
      v-else-if="items.length === 0"
      title="Нет активного чтения"
      description="Добавьте ранобэ в закладки, чтобы продолжить позже."
      variant="empty"
    />

    <div
      v-else
      class="continue-grid"
    >
      <HomeContinueReadingCard
        v-for="item in items"
        :key="item.slug"
        :item="item"
        @open="$emit('open-item', $event)"
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

.home-section__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.continue-grid {
  display: grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 0.85rem;
}

.continue-card--skeleton {
  min-height: 132px;
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

@media (min-width: 768px) {
  .continue-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
