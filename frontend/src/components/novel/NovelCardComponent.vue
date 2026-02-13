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
})

const isLoading = ref(true)
const hasError = ref(false)

const displayImage = computed(() => {
  if (hasError.value || !props.imageSrc) {
    return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="160" height="200" viewBox="0 0 160 200"><rect width="160" height="200" fill="%23C4FF61"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="14" fill="%23494949">Нет обложки</text></svg>'
  }
  return props.imageSrc
})

const handleClick = () => {}

const onImageLoad = () => {
  isLoading.value = false
}

const onImageError = (event) => {
  isLoading.value = false
  hasError.value = true
  const target = event.target
  target.src = displayImage.value
}
</script>

<template>
  <article class="novel-card">
    <router-link :to="`/novel/${slug}`" class="novel-card__link" :aria-label="`Открыть ${title}`">
      <div class="novel-card__image-wrapper">
        <div v-if="isLoading" class="novel-card__skeleton" aria-hidden="true"></div>
        <img
          :src="displayImage"
          :alt="title"
          class="novel-card__image"
          :class="{ 'novel-card__image--loaded': !isLoading }"
          loading="lazy"
          @load="onImageLoad"
          @error="onImageError"
        />
        <div class="novel-card__country-badge">
          {{ country }}
        </div>
      </div>
      <h3 class="novel-card__title">{{ title }}</h3>
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
}

.novel-card__image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background-color: #2a2a2a;
}

.novel-card__skeleton {
  position: absolute;
  inset: 0;
  background: linear-gradient(110deg, #2a2a2a 8%, #3a3a3a 18%, #2a2a2a 33%);
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
  background: rgba(0, 0, 0, 0.7);
  color: #c4ff61;
  font-size: 0.7rem;
  font-weight: 500;
  border-radius: 4px;
  backdrop-filter: blur(4px);
}

.novel-card__title {
  margin-top: 0.75rem;
  color: #ffffff;
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
  color: #c4ff61;
}
</style>
