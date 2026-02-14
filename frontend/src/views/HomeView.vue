<script setup>
import { computed } from 'vue'
import NovelCardComponent from '../components/novel/NovelCardComponent.vue'
import NovelCardWithTags from '../components/novel/NovelCardWithTags.vue'
import StatePanel from '@/components/common/StatePanel.vue'
import { novels, novelsWithTags } from '../mocks/novels'

const hasNovels = computed(() => novels.length > 0)
const hasNovelsWithTags = computed(() => novelsWithTags.length > 0)
</script>

<template>
  <main class="bg-[var(--background-color)] min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-white text-2xl mb-6">
        Ранобэ
      </h1>

      <StatePanel
        v-if="!hasNovels"
        title="Пока нет данных"
        description="Список ранобэ на главной скоро появится."
        variant="empty"
      />

      <template v-else>
        <h2 class="sr-only">
          Список ранобэ
        </h2>
        <div
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-rd-4"
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
      </template>
      <div class="divider my-8 border-t border-gray-700" />
    </div>

    <div class="container mx-auto px-4 py-8">
      <h2 class="text-white text-xl mb-4">
        Пример с тегами
      </h2>

      <StatePanel
        v-if="!hasNovelsWithTags"
        title="Нет карточек с тегами"
        description="Контент с тегами будет добавлен позже."
        variant="empty"
      />

      <div
        v-else
        class="flex flex-wrap gap-rd-4"
      >
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
