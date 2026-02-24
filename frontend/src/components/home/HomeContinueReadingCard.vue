<script setup>
defineProps({
  item: {
    type: Object,
    required: true,
  },
})

defineEmits(['open'])
</script>

<template>
  <article class="continue-card">
    <router-link
      :to="`/novel/${item.slug}`"
      class="continue-card__media-link"
      @click="$emit('open', item)"
    >
      <img
        :src="item.imageSrc"
        :alt="item.title"
        loading="lazy"
        class="continue-card__image"
      >
    </router-link>
    <div class="continue-card__content">
      <h2 class="continue-card__title">
        {{ item.title }}
      </h2>
      <p class="continue-card__chapter">
        {{ item.lastReadChapter }}
      </p>
      <div class="continue-card__progress-track">
        <div
          class="continue-card__progress-value"
          :style="{ width: `${item.progress}%` }"
        />
      </div>
      <button
        type="button"
        class="continue-card__cta"
        @click="$emit('open', item)"
      >
        Продолжить
      </button>
    </div>
  </article>
</template>

<style scoped>
.continue-card {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 0.7rem;
  border: 1px solid var(--border-soft-color);
  border-radius: 12px;
  background: color-mix(in srgb, var(--third-color) 88%, transparent);
  min-height: 132px;
  padding: 0.6rem;
}

.continue-card__media-link {
  display: block;
  border-radius: 8px;
  overflow: hidden;
}

.continue-card__image {
  width: 100%;
  height: 100%;
  min-height: 118px;
  object-fit: cover;
}

.continue-card__content {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  min-width: 0;
}

.continue-card__title {
  color: var(--foreground-third-color);
  font-size: 0.9rem;
  font-weight: 700;
  line-height: 1.3;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.continue-card__chapter {
  color: var(--foreground-secondary-color);
  font-size: 0.75rem;
}

.continue-card__progress-track {
  width: 100%;
  height: 4px;
  border-radius: 999px;
  background: color-mix(in srgb, white 10%, transparent);
  overflow: hidden;
}

.continue-card__progress-value {
  height: 100%;
  border-radius: inherit;
  background: var(--first-color);
}

.continue-card__cta {
  margin-top: auto;
  align-self: flex-start;
  border: none;
  border-radius: 999px;
  padding: 0.38rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--foreground-color);
  background: var(--first-color);
  cursor: pointer;
}
</style>
