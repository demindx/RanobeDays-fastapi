<template>
  <div class="card-container">
    <router-link :to="`/novel/${slug}`" class="no-underline">
      <div class="card">
        <div class="image-container">
          <img
            :src="imageSrc"
            :alt="title"
            class="card-image"
            @error="onImageError"
          />
        </div>
        <div class="info">
          <div class="country">{{ country }}</div>
          <div class="title">{{ title }}</div>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  country: {
    type: String,
    required: true
  },
  slug: {
    type: String,
    required: true
  },
  imageSrc: {
    type: String,
    default: 'https://placehold.co/160x200?text=Cover'
  }
});

const onImageError = (event) => {
  // Set a fallback image if the original fails to load
  event.target.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="160" height="200" viewBox="0 0 160 200"><rect width="160" height="200" fill="%23C4FF61"/></svg>';
};
</script>

<style scoped>
.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.card {
  width: 160px;
  background: transparent;
  border-radius: 3px;
  overflow: visible;
  display: flex;
  flex-direction: column;
}

.image-container {
  width: 100%;
  height: 200px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  background-color: #C4FF61; /* Green background when image is not loaded */
}

.card-image {
  width: 100%;
  height: 200px;
  display: block;
  object-fit: cover;
  border-radius: 3px;
}

.info {
  padding: 0.5rem;
  text-align: left;
  background: transparent;
}

.country {
  color: #9CA3AF; /* Darker gray */
  font-size: 0.75rem;
  margin-bottom: 0.25rem;
  background: transparent;
}

.title {
  color: white; /* White color */
  font-size: 0.875rem;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  background: transparent;
}
</style>
