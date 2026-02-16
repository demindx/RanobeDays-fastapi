<script setup>
import { computed, ref } from 'vue'

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
    return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="96" height="136" viewBox="0 0 96 136"><rect width="96" height="136" fill="%232C2C2C"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="10" fill="%23BFBFBF">Нет обложки</text></svg>'
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

  if (normalized.includes('люб')) return 'novel-compact-card__bookmark-badge--favorite'
  if (normalized.includes('буд')) return 'novel-compact-card__bookmark-badge--planned'
  if (normalized.includes('чита')) return 'novel-compact-card__bookmark-badge--reading'
  return 'novel-compact-card__bookmark-badge--default'
})
</script>

<template>
  <article class="novel-compact-card">
    <component
      :is="hasSlug ? 'router-link' : 'div'"
      :to="hasSlug ? `/novel/${slug}` : undefined"
      class="novel-compact-card__link"
      :class="{ 'novel-compact-card__link--disabled': !hasSlug }"
      :aria-disabled="!hasSlug ? 'true' : undefined"
    >
      <div class="novel-compact-card__image-wrapper">
        <div class="novel-compact-card__image-clip">
          <div
            v-if="isLoading"
            class="novel-compact-card__skeleton"
            aria-hidden="true"
          />
          <img
            :src="displayImage"
            :alt="title"
            class="novel-compact-card__image"
            :class="{ 'novel-compact-card__image--loaded': !isLoading }"
            loading="lazy"
            @load="onImageLoad"
            @error="onImageError"
          >
          <div
            v-if="bookmarkStatus"
            class="novel-compact-card__bookmark-badge"
            :class="bookmarkBadgeClass"
          >
            {{ bookmarkStatus }}
          </div>
        </div>
      </div>

      <div class="novel-compact-card__content">
        <h3 class="novel-compact-card__title">
          {{ title }}
        </h3>
        <p class="novel-compact-card__description">
          {{ description }}
        </p>
      </div>
    </component>
  </article>
</template>

<style scoped>
.novel-compact-card {
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

.novel-compact-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: color-mix(in srgb, var(--first-color) 24%, var(--border-soft-color));
}

.novel-compact-card__link {
  display: flex;
  min-height: var(--novel-compact-card-height);
  text-decoration: none;
}

.novel-compact-card__link:focus-visible {
  outline: 2px solid var(--first-color);
  outline-offset: 3px;
}

.novel-compact-card__link--disabled {
  cursor: default;
}

.novel-compact-card__image-wrapper {
  width: var(--novel-compact-card-media-width);
  flex-shrink: 0;
  background: var(--surface-elevated-color);
}

.novel-compact-card__image-clip {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.novel-compact-card__skeleton {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    110deg,
    var(--surface-elevated-color) 8%,
    var(--surface-hover-color) 18%,
    var(--surface-elevated-color) 33%
  );
  background-size: 200% 100%;
  animation: compact-shimmer 1.5s infinite linear;
}

@keyframes compact-shimmer {
  to {
    background-position: -200% 0;
  }
}

.novel-compact-card__image {
  width: 100%;
  height: var(--novel-compact-card-height);
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.novel-compact-card__image--loaded {
  opacity: 1;
}

.novel-compact-card__bookmark-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  z-index: 2;
  max-width: calc(100% - 12px);
  padding: 3px 6px;
  border-radius: 999px;
  color: #fff;
  font-size: 0.56rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.01em;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(6px);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.novel-compact-card__bookmark-badge--reading {
  background: linear-gradient(135deg, rgba(47, 143, 104, 0.94), rgba(31, 102, 73, 0.92));
}

.novel-compact-card__bookmark-badge--planned {
  background: linear-gradient(135deg, rgba(58, 79, 159, 0.94), rgba(42, 60, 126, 0.92));
}

.novel-compact-card__bookmark-badge--favorite {
  background: linear-gradient(135deg, rgba(158, 58, 103, 0.94), rgba(125, 45, 82, 0.92));
}

.novel-compact-card__bookmark-badge--default {
  background: linear-gradient(135deg, rgba(79, 79, 79, 0.94), rgba(58, 58, 58, 0.92));
}

.novel-compact-card__content {
  display: flex;
  flex: 1;
  min-width: 0;
  flex-direction: column;
  justify-content: center;
  gap: var(--novel-compact-card-content-gap);
  padding: var(--novel-compact-card-content-padding-y) var(--novel-compact-card-content-padding-x);
}

.novel-compact-card__title {
  color: var(--foreground-third-color);
  font-size: var(--novel-compact-card-title-size);
  font-weight: 700;
  line-height: 1.3;
  transition: color 0.2s ease;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.novel-compact-card:hover .novel-compact-card__title {
  color: var(--first-color);
}

.novel-compact-card__description {
  color: var(--foreground-secondary-color);
  font-size: var(--novel-compact-card-description-size);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (max-width: 767px) {
  .novel-compact-card__image-wrapper {
    width: var(--novel-compact-card-media-width-mobile);
  }

  .novel-compact-card__image {
    height: var(--novel-compact-card-height-mobile);
  }

  .novel-compact-card__link {
    min-height: var(--novel-compact-card-height-mobile);
  }
}
</style>
