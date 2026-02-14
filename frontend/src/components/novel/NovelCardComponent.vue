<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  country: {
    type: String,
    required: true,
  },
  slug: {
    type: String,
    required: true,
  },
  imageSrc: {
    type: String,
    default: '',
  },
  bookmarkStatus: {
    type: String,
    default: '',
  },
})

const isLoading = ref(true)
const hasError = ref(false)

const displayImage = computed(() => {
  if (hasError.value || !props.imageSrc) {
    return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="160" height="200" viewBox="0 0 160 200"><rect width="160" height="200" fill="%23C4FF61"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="14" fill="%23494949">Нет обложки</text></svg>'
  }
  return props.imageSrc
})

const onImageLoad = () => {
  isLoading.value = false
}

const onImageError = (event) => {
  isLoading.value = false
  hasError.value = true
  const target = event.target
  target.src = displayImage.value
}

const bookmarkBadgeClass = computed(() => {
  const normalized = props.bookmarkStatus.toLowerCase()

  if (normalized.includes('люб')) return 'novel-card__bookmark-badge--favorite'
  if (normalized.includes('буд')) return 'novel-card__bookmark-badge--planned'
  if (normalized.includes('чита')) return 'novel-card__bookmark-badge--reading'
  return 'novel-card__bookmark-badge--default'
})
</script>

<template>
  <article class="novel-card">
    <router-link
      :to="`/novel/${slug}`"
      class="novel-card__link"
    >
      <div class="novel-card__image-wrapper">
        <div class="novel-card__image-clip">
          <div
            v-if="isLoading"
            class="novel-card__skeleton"
            aria-hidden="true"
          />
          <img
            :src="displayImage"
            :alt="title"
            class="novel-card__image"
            :class="{ 'novel-card__image--loaded': !isLoading }"
            loading="lazy"
            @load="onImageLoad"
            @error="onImageError"
          >
        </div>
        <div
          v-if="bookmarkStatus"
          class="novel-card__bookmark-badge"
          :class="bookmarkBadgeClass"
        >
          {{ bookmarkStatus }}
        </div>
        <div
          class="novel-card__country-badge"
        >
          {{ country }}
        </div>
      </div>
      <h3 class="novel-card__title">
        {{ title }}
      </h3>
    </router-link>
  </article>
</template>

<style scoped>
.novel-card {
  display: flex;
  justify-content: center;
  padding: 0.5rem;
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.novel-card:hover {
  transform: translateY(-4px);
}

.novel-card__link {
  text-decoration: none;
  display: flex;
  flex-direction: column;
  width: 160px;
  border-radius: 4px;
}

.novel-card__link:focus-visible {
  outline: 2px solid var(--first-color);
  outline-offset: 4px;
}

.novel-card__image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  border-radius: 4px;
  overflow: visible;
  box-shadow: var(--shadow-soft);
  background-color: var(--surface-elevated-color);
}

.novel-card__image-clip {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  overflow: hidden;
}

.novel-card__skeleton {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    110deg,
    var(--surface-elevated-color) 8%,
    var(--surface-hover-color) 18%,
    var(--surface-elevated-color) 33%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite linear;
}

@keyframes shimmer {
  to {
    background-position: -200% 0;
  }
}

.novel-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.novel-card__image--loaded {
  opacity: 1;
}

.novel-card__country-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 2px 8px;
  background: color-mix(in srgb, var(--surface-overlay-color) 68%, transparent);
  color: var(--first-color);
  font-size: 0.7rem;
  font-weight: 500;
  border-radius: 4px;
  backdrop-filter: blur(4px);
}

.novel-card__bookmark-badge {
  position: absolute;
  top: -6px;
  right: -10px;
  z-index: 3;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  max-width: calc(100% - 16px);
  padding: 4px 8px;
  border-radius: 6px;
  color: #fff;
  font-size: 0.65rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.01em;
  backdrop-filter: blur(6px);
  box-shadow: var(--shadow-soft);
  border: 1px solid rgba(255, 255, 255, 0.2);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.novel-card__bookmark-badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  flex-shrink: 0;
}

.novel-card__bookmark-badge--reading {
  background: linear-gradient(135deg, rgba(47, 143, 104, 0.94), rgba(31, 102, 73, 0.92));
}

.novel-card__bookmark-badge--planned {
  background: linear-gradient(135deg, rgba(58, 79, 159, 0.94), rgba(42, 60, 126, 0.92));
}

.novel-card__bookmark-badge--favorite {
  background: linear-gradient(135deg, rgba(158, 58, 103, 0.94), rgba(125, 45, 82, 0.92));
}

.novel-card__bookmark-badge--default {
  background: linear-gradient(135deg, rgba(79, 79, 79, 0.94), rgba(58, 58, 58, 0.92));
}

.novel-card__title {
  margin-top: 0.75rem;
  color: var(--foreground-third-color);
  font-size: 0.875rem;
  font-weight: 600;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  background: transparent;
  transition: color 0.2s ease;
}

.novel-card:hover .novel-card__title {
  color: var(--first-color);
}

.novel-card__link:focus-visible .novel-card__title {
  color: var(--first-color);
}
</style>
