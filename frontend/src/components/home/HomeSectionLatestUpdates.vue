<script setup>
import SectionAccentTitle from '@/components/common/SectionAccentTitle.vue'
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

defineEmits(['retry', 'open-item'])
</script>

<template>
  <section class="home-section">
    <div class="home-section__header">
      <SectionAccentTitle>Последние обновления</SectionAccentTitle>
    </div>

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
      class="updates-list"
      aria-busy="true"
    >
      <div
        v-for="index in 8"
        :key="index"
        class="updates-list__skeleton"
      />
    </div>

    <StatePanel
      v-else-if="items.length === 0"
      title="Обновлений пока нет"
      description="Когда выйдут новые главы, они появятся здесь."
      variant="empty"
    />

    <ul
      v-else
      class="updates-list"
    >
      <li
        v-for="item in items"
        :key="item.id"
        class="updates-item"
      >
        <div class="updates-item__main">
          <router-link
            :to="`/novel/${item.slug}`"
            class="updates-item__title"
            @click="$emit('open-item', item)"
          >
            {{ item.title }}
          </router-link>
          <p class="updates-item__meta">
            <span>{{ item.chapter }}</span>
            <span>{{ item.updatedAt }}</span>
          </p>
        </div>
        <span class="updates-item__status">
          {{ item.bookmarkStatus }}
        </span>
        <router-link
          :to="`/novel/${item.slug}`"
          class="updates-item__cta"
          @click="$emit('open-item', item)"
        >
          Открыть
        </router-link>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.home-section {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  min-width: 0;
}


.updates-list {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.updates-item {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0.5rem;
  border: 1px solid var(--border-soft-color);
  border-radius: 10px;
  background: color-mix(in srgb, var(--third-color) 88%, transparent);
  padding: 0.65rem 0.75rem;
}

.updates-item__title {
  display: inline-block;
  max-width: 100%;
  color: var(--foreground-third-color);
  text-decoration: none;
  font-weight: 700;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.updates-item__meta {
  margin-top: 0.15rem;
  color: var(--foreground-secondary-color);
  font-size: 0.74rem;
  display: flex;
  gap: 0.45rem;
}

.updates-item__status {
  justify-self: start;
  border-radius: 999px;
  border: 1px solid var(--border-soft-color);
  color: var(--foreground-secondary-color);
  font-size: 0.66rem;
  padding: 0.15rem 0.42rem;
}

.updates-item__cta {
  justify-self: start;
  border-radius: 999px;
  border: 1px solid color-mix(in srgb, var(--first-color) 40%, transparent);
  color: var(--first-color);
  font-size: 0.68rem;
  font-weight: 700;
  text-decoration: none;
  padding: 0.2rem 0.54rem;
}

.updates-list__skeleton {
  height: 78px;
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

@media (min-width: 768px) {
  .updates-item {
    grid-template-columns: minmax(0, 1fr) auto auto;
    align-items: center;
  }

  .updates-item__status {
    justify-self: end;
  }

  .updates-item__cta {
    justify-self: end;
  }
}
</style>
