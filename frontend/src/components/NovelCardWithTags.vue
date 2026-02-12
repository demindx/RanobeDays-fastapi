<template>
  <div class="novel-card bg-[#232323] rounded-lg overflow-hidden shadow-lg flex">
    <div class="image-container w-[160px] flex-shrink-0">
      <img
        :src="imageSrc"
        :alt="title"
        class="w-full h-[240px] object-cover"
        @error="onImageError"
      />
    </div>

    <div class="p-4 flex flex-col justify-center">
      <div class="tags mb-2 flex flex-wrap gap-1">
        <TagComponent v-for="tag in tags" :key="tag.id" :name="tag.name" :id="tag.id" />
      </div>

      <h3 class="title text-white text-base font-bold mb-2">{{ title }}</h3>
      <p class="description text-[#BFBFBF] text-sm line-clamp-4">{{ description }}</p>
    </div>
  </div>
</template>

<script setup>
import TagComponent from './TagComponent.vue'

defineProps({
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
    default: 'https://placehold.co/370x192?text=Cover',
  },
  tags: {
    type: Array,
    default: () => [],
  },
})

const onImageError = (event) => {
  // Set a fallback image if the original fails to load
  event.target.src =
    'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="160" height="240" viewBox="0 0 160 240"><rect width="160" height="240" fill="%232C2C2C"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="16" fill="%23BFBFBF">No Image</text></svg>'
}
</script>
