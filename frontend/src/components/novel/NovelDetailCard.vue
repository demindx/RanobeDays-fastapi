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

  if (normalized.includes('люб')) return 'novel-detail-card__bookmark-badge--favorite'
  if (normalized.includes('буд')) return 'novel-detail-card__bookmark-badge--planned'
  if (normalized.includes('чита')) return 'novel-detail-card__bookmark-badge--reading'
  return 'novel-detail-card__bookmark-badge--default'
})
</script>

<template>
  <article class="novel-detail-card">
    <component
      :is="hasSlug ? 'router-link' : 'div'"
      :to="hasSlug ? `/novel/${slug}` : undefined"
      class="novel-detail-card__link"
      :class="{ 'novel-detail-card__link--disabled': !hasSlug }"
      :aria-disabled="!hasSlug ? 'true' : undefined"
    >
      <div class="novel-detail-card__image-wrapper">
        <div class="novel-detail-card__image-clip">
          <div
            v-if="isLoading"
            class="novel-detail-card__skeleton"
            aria-hidden="true"
          />
          <img
            :src="displayImage"
            :alt="title"
            class="novel-detail-card__image"
            :class="{ 'novel-detail-card__image--loaded': !isLoading }"
            loading="lazy"
            @load="onImageLoad"
            @error="onImageError"
          >
          <div
            v-if="bookmarkStatus"
            class="novel-detail-card__bookmark-badge"
            :class="bookmarkBadgeClass"
          >
            {{ bookmarkStatus }}
          </div>
        </div>
      </div>

      <div class="novel-detail-card__content">
        <div
          v-if="tags.length"
          class="novel-detail-card__tags"
        >
          <TagComponent
            v-for="tag in tags"
            :id="tag.id"
            :key="tag.id"
            :name="tag.name"
            size="sm"
          />
        </div>

        <h3 class="novel-detail-card__title">
          {{ title }}
        </h3>
        <p class="novel-detail-card__description">
          {{ description }}
        </p>
      </div>
    </component>
  </article>
</template>

<style scoped>
.novel-detail-card {
  width: min(100%, var(--novel-detail-card-width));
  flex: 1 1 var(--novel-detail-card-width);
  background: color-mix(in srgb, var(--third-color) 82%, transparent);
  border-radius: 8px;
  border: 1px solid var(--border-soft-color);
  overflow: hidden;
  box-shadow: var(--shadow-soft);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.novel-detail-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: color-mix(in srgb, var(--first-color) 24%, var(--border-soft-color));
}

.novel-detail-card__link {
  display: flex;
  min-height: var(--novel-detail-card-height);
  text-decoration: none;
}

.novel-detail-card__link:focus-visible {
  outline: 2px solid var(--first-color);
  outline-offset: 3px;
}

.novel-detail-card__link--disabled {
  cursor: default;
}

.novel-detail-card__image-wrapper {
  width: var(--novel-detail-card-media-width);
  flex-shrink: 0;
  background: var(--surface-elevated-color);
}

.novel-detail-card__image-clip {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.novel-detail-card__skeleton {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    110deg,
    var(--surface-elevated-color) 8%,
    var(--surface-hover-color) 18%,
    var(--surface-elevated-color) 33%
  );
  background-size: 200% 100%;
  animation: detail-shimmer 1.5s infinite linear;
}

@keyframes detail-shimmer {
  to {
    background-position: -200% 0;
  }
}

.novel-detail-card__image {
  width: 100%;
  height: var(--novel-detail-card-height);
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.novel-detail-card__image--loaded {
  opacity: 1;
}

.novel-detail-card__bookmark-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  max-width: calc(100% - 12px);
  padding: 3px 7px;
  border-radius: 999px;
  color: #fff;
  font-size: 0.6rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.01em;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(6px);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.novel-detail-card__bookmark-badge--reading {
  background: linear-gradient(135deg, rgba(47, 143, 104, 0.94), rgba(31, 102, 73, 0.92));
}

.novel-detail-card__bookmark-badge--planned {
  background: linear-gradient(135deg, rgba(58, 79, 159, 0.94), rgba(42, 60, 126, 0.92));
}

.novel-detail-card__bookmark-badge--favorite {
  background: linear-gradient(135deg, rgba(158, 58, 103, 0.94), rgba(125, 45, 82, 0.92));
}

.novel-detail-card__bookmark-badge--default {
  background: linear-gradient(135deg, rgba(79, 79, 79, 0.94), rgba(58, 58, 58, 0.92));
}

.novel-detail-card__content {
  display: flex;
  flex: 1;
  min-width: 0;
  flex-direction: column;
  justify-content: center;
  gap: var(--novel-detail-card-content-gap);
  padding: var(--novel-detail-card-content-padding-y) var(--novel-detail-card-content-padding-x);
}

.novel-detail-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.novel-detail-card__tags :deep(.tag) {
  max-width: 100%;
}

.novel-detail-card__title {
  color: var(--foreground-third-color);
  font-size: var(--novel-detail-card-title-size);
  font-weight: 700;
  line-height: 1.3;
  transition: color 0.2s ease;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.novel-detail-card:hover .novel-detail-card__title {
  color: var(--first-color);
}

.novel-detail-card__description {
  color: var(--foreground-secondary-color);
  font-size: var(--novel-detail-card-description-size);
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (max-width: 767px) {
  .novel-detail-card {
    width: 100%;
    flex-basis: 100%;
  }

  .novel-detail-card__image-wrapper {
    width: var(--novel-detail-card-media-width-mobile);
  }

  .novel-detail-card__image {
    height: var(--novel-detail-card-height-mobile);
  }

  .novel-detail-card__link {
    min-height: var(--novel-detail-card-height-mobile);
  }

  .novel-detail-card__tags :deep(.tag) {
    min-height: 1.2rem !important;
    padding: 0.08rem 0.4rem !important;
    font-size: 0.62rem !important;
  }
}
</style>
