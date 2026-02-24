<script setup>
import { computed, ref } from 'vue'
import NovelPosterCard from '@/components/novel/NovelPosterCard.vue'
import NovelHeroCarousel from '../components/novel/NovelHeroCarousel.vue'
import NovelDetailCard from '@/components/novel/NovelDetailCard.vue'
import NovelCompactCard from '@/components/novel/NovelCompactCard.vue'
import StatePanel from '@/components/common/StatePanel.vue'
import SectionAccentTitle from '@/components/common/SectionAccentTitle.vue'
import TextInputField from '@/components/common/TextInputField.vue'
import DropdownSelectField from '@/components/common/DropdownSelectField.vue'
import TagDropdownSelector from '@/components/common/TagDropdownSelector.vue'
import { novels, novelsWithTags } from '../mocks/novels'

const hasNovels = computed(() => novels.length > 0)
const hasNovelsWithTags = computed(() => novelsWithTags.length > 0)
const demoInput = ref('')
const demoSelect = ref('jp')
const demoTags = ref(['action', 'romance', 'adventure', 'comedy', 'drama'])

const countryOptions = [
  { label: 'Япония', value: 'jp' },
  { label: 'Корея', value: 'kr' },
  { label: 'Китай', value: 'cn' },
]

const tagOptions = [
  { label: 'Экшен', value: 'action' },
  { label: 'Романтика', value: 'romance' },
  { label: 'Приключения', value: 'adventure' },
  { label: 'Комедия', value: 'comedy' },
  { label: 'Драма', value: 'drama' },
  { label: 'Фэнтези', value: 'fantasy' },
  { label: 'Мистика', value: 'mystery' },
]

</script>

<template>
  <section class="bg-[var(--background-color)] min-h-screen">
    <NovelHeroCarousel
      v-if="hasNovels"
      :novels="novels"
      title="Подборка для вас"
    />

    <div class="container mx-auto px-4 py-8">
      <SectionAccentTitle
        as="h1"
        class="mb-6"
      >
        Ранобэ
      </SectionAccentTitle>

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
          <NovelPosterCard
            v-for="novel in novels"
            :key="novel.slug"
            :title="novel.title"
            :country="novel.country"
            :image-src="novel.imageSrc"
            :slug="novel.slug"
            :bookmark-status="novel.bookmarkStatus"
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
        class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-rd-4"
      >
        <NovelDetailCard
          v-for="novel in novelsWithTags"
          :key="novel.slug"
          :title="novel.title"
          :description="novel.description"
          :image-src="novel.imageSrc"
          :tags="novel.tags"
          :slug="novel.slug"
          :bookmark-status="novel.bookmarkStatus"
        />
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <h2 class="text-white text-xl mb-4">
        Компактная карточка
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-rd-4">
        <NovelCompactCard
          v-for="novel in novelsWithTags.slice(0, 6)"
          :key="`compact-${novel.slug}`"
          :title="novel.title"
          :description="novel.description"
          :image-src="novel.imageSrc"
          :slug="novel.slug"
          :bookmark-status="novel.bookmarkStatus"
        />
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <h2 class="text-white text-xl mb-4">
        Пример полей
      </h2>
      <div class="flex flex-col sm:flex-row sm:flex-wrap items-stretch sm:items-center gap-rd-4">
        <TextInputField
          v-model="demoInput"
          aria-label="Пример текстового поля"
          placeholder="Введите значение"
        />
        <DropdownSelectField
          v-model="demoSelect"
          aria-label="Пример выпадающего списка"
          :options="countryOptions"
        />
        <TagDropdownSelector
          v-model="demoTags"
          aria-label="Пример селектора тегов"
          :options="tagOptions"
        />
      </div>
    </div>
  </section>
</template>
