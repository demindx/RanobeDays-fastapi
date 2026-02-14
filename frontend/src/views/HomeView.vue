<script setup>
import NovelCardComponent from '../components/novel/NovelCardComponent.vue'
import NovelCardWithTags from '../components/novel/NovelCardWithTags.vue'
import { novels, novelsWithTags } from '../mocks/novels'
</script>

<template>
  <main class="bg-[var(--background-color)] min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-white text-2xl mb-6">
        Ранобэ
      </h1>
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
      >
        <NovelCardComponent
          v-for="novel in novels"
          :key="novel.slug"
          :title="novel.title"
          :country="novel.country"
          :image-src="novel.imageSrc"
          :slug="novel.slug"
        />
      </div>
      <div class="divider my-8 border-t border-gray-700" />
    </div>

    <div class="container mx-auto px-4 py-8">
      <h2 class="text-white text-xl mb-4">
        Пример с тегами
      </h2>
      <div class="flex flex-wrap gap-4">
        <NovelCardWithTags
          v-for="novel in novelsWithTags"
          :key="novel.slug"
          :title="novel.title"
          :description="novel.description"
          :image-src="novel.imageSrc"
          :tags="novel.tags"
          :slug="novel.slug"
        />
      </div>
    </div>
  </main>
</template>
