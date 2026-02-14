<script setup>
import { ref, computed } from 'vue'
import TagComponent from './TagComponent.vue'

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  imageSrc: {
    type: String,
    default: '',
  },
  tags: {
    type: Array,
    default: () => [],
  },
  slug: {
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
const hasSlug = computed(() => Boolean(props.slug))

const displayImage = computed(() => {
  if (hasError.value || !props.imageSrc) {
    return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="160" height="240" viewBox="0 0 160 240"><rect width="160" height="240" fill="%232C2C2C"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="14" fill="%23BFBFBF">Нет обложки</text></svg>'
  }
  return props.imageSrc
})

const onImageLoad = () => {
  isLoading.value = false
}

const onImageError = (event) => {
  isLoading.value = false
  hasError.value = true
  event.target.src = displayImage.value
}

const bookmarkBadgeClass = computed(() => {
  const normalized = props.bookmarkStatus.toLowerCase()

  if (normalized.includes('люб')) return 'novel-card-with-tags__bookmark-badge--favorite'
  if (normalized.includes('буд')) return 'novel-card-with-tags__bookmark-badge--planned'
  if (normalized.includes('чита')) return 'novel-card-with-tags__bookmark-badge--reading'
  return 'novel-card-with-tags__bookmark-badge--default'
})
</script>

<template>
  <article class="novel-card-with-tags">
    <component
      :is="hasSlug ? 'router-link' : 'div'"
      :to="hasSlug ? `/novel/${slug}` : undefined"
      class="novel-card-with-tags__link"
      :class="{ 'novel-card-with-tags__link--disabled': !hasSlug }"
      :aria-disabled="!hasSlug ? 'true' : undefined"
    >
      <div class="novel-card-with-tags__image-wrapper">
        <div class="novel-card-with-tags__image-clip">
          <div
            v-if="isLoading"
            class="novel-card-with-tags__skeleton"
            aria-hidden="true"
          />
          <img
            :src="displayImage"
            :alt="title"
            class="novel-card-with-tags__image"
            :class="{ 'novel-card-with-tags__image--loaded': !isLoading }"
            loading="lazy"
            @load="onImageLoad"
            @error="onImageError"
          >
          <div
            v-if="bookmarkStatus"
            class="novel-card-with-tags__bookmark-badge"
            :class="bookmarkBadgeClass"
          >
            {{ bookmarkStatus }}
          </div>
        </div>
      </div>

      <div class="novel-card-with-tags__content">
        <div
          v-if="tags.length"
          class="novel-card-with-tags__tags"
        >
          <TagComponent
            v-for="tag in tags"
            :id="tag.id"
            :key="tag.id"
            :name="tag.name"
            size="sm"
          />
        </div>

        <h3 class="novel-card-with-tags__title">
          {{ title }}
        </h3>
        <p class="novel-card-with-tags__description">
          {{ description }}
        </p>
      </div>
    </component>
  </article>
</template>

<style scoped>
.novel-card-with-tags {
  background: var(--background-color);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.novel-card-with-tags:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.novel-card-with-tags__link {
  display: flex;
  text-decoration: none;
}

.novel-card-with-tags__link:focus-visible {
  outline: 2px solid var(--first-color);
  outline-offset: 4px;
}

.novel-card-with-tags__link--disabled {
  cursor: default;
}

.novel-card-with-tags__image-wrapper {
  position: relative;
  width: 160px;
  flex-shrink: 0;
  overflow: visible;
  background-color: var(--surface-elevated-color);
}

.novel-card-with-tags__image-clip {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.novel-card-with-tags__skeleton {
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

.novel-card-with-tags__image {
  width: 100%;
  height: 240px;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.novel-card-with-tags__image--loaded {
  opacity: 1;
}

.novel-card-with-tags__bookmark-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  max-width: calc(100% - 16px);
  padding: 4px 8px;
  border-radius: 999px;
  color: #fff;
  font-size: 0.66rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.01em;
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: var(--shadow-soft);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.novel-card-with-tags__bookmark-badge::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  flex-shrink: 0;
}

.novel-card-with-tags__bookmark-badge--reading {
  background: linear-gradient(135deg, rgba(47, 143, 104, 0.94), rgba(31, 102, 73, 0.92));
}

.novel-card-with-tags__bookmark-badge--planned {
  background: linear-gradient(135deg, rgba(58, 79, 159, 0.94), rgba(42, 60, 126, 0.92));
}

.novel-card-with-tags__bookmark-badge--favorite {
  background: linear-gradient(135deg, rgba(158, 58, 103, 0.94), rgba(125, 45, 82, 0.92));
}

.novel-card-with-tags__bookmark-badge--default {
  background: linear-gradient(135deg, rgba(79, 79, 79, 0.94), rgba(58, 58, 58, 0.92));
}

.novel-card-with-tags__content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 1;
  min-width: 0;
}

.novel-card-with-tags__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.novel-card-with-tags__title {
  color: white;
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  line-height: 1.3;
  transition: color 0.2s ease;
}

.novel-card-with-tags:hover .novel-card-with-tags__title {
  color: var(--first-color);
}

.novel-card-with-tags__link:focus-visible .novel-card-with-tags__title {
  color: var(--first-color);
}

.novel-card-with-tags__description {
  color: var(--foreground-secondary-color);
  font-size: 0.875rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
