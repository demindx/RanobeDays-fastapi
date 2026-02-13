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
})

const isLoading = ref(true)
const hasError = ref(false)

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
</script>

<template>
  <article class="novel-card-with-tags">
    <router-link
      :to="slug ? `/novel/${slug}` : '#'"
      class="novel-card-with-tags__link"
      :aria-label="`Открыть ${title}`"
    >
      <div class="novel-card-with-tags__image-wrapper">
        <div v-if="isLoading" class="novel-card-with-tags__skeleton" aria-hidden="true"></div>
        <img
          :src="displayImage"
          :alt="title"
          class="novel-card-with-tags__image"
          :class="{ 'novel-card-with-tags__image--loaded': !isLoading }"
          loading="lazy"
          @load="onImageLoad"
          @error="onImageError"
        />
      </div>

      <div class="novel-card-with-tags__content">
        <div class="novel-card-with-tags__tags" v-if="tags.length">
          <TagComponent v-for="tag in tags" :key="tag.id" :name="tag.name" :id="tag.id" size="sm" />
        </div>

        <h3 class="novel-card-with-tags__title">{{ title }}</h3>
        <p class="novel-card-with-tags__description">{{ description }}</p>
      </div>
    </router-link>
  </article>
</template>

<style scoped>
.novel-card-with-tags {
  background: #232323;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.novel-card-with-tags:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.novel-card-with-tags__link {
  display: flex;
  text-decoration: none;
}

.novel-card-with-tags__image-wrapper {
  position: relative;
  width: 160px;
  flex-shrink: 0;
  overflow: hidden;
  background-color: #2a2a2a;
}

.novel-card-with-tags__skeleton {
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
  gap: 0.25rem;
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
  color: #c4ff61;
}

.novel-card-with-tags__description {
  color: #bfbfbf;
  font-size: 0.875rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
