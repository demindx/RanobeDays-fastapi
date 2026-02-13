<script setup>
import Header from '../components/layout/Header.vue'
import NovelCardComponent from '../components/novel/NovelCardComponent.vue'
import NovelCardWithTags from '../components/novel/NovelCardWithTags.vue'
</script>

<template>
  <main class="bg-[#232323] min-h-screen">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-white text-2xl mb-6">Ранобэ</h1>
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
      >
        <NovelCardComponent
          title="Великий демон"
          country="Япония"
          :image-src="'invalid-url.jpg'"
          slug="great-demon"
        />
        <NovelCardComponent
          title="Путь воина"
          country="Корея"
          :image-src="'https://placehold.co/160x200?text=Cover'"
          slug="warrior-path"
        />
        <NovelCardComponent
          title="Магическая академия"
          country="Япония"
          :image-src="'invalid-url.jpg'"
          slug="magic-academy"
        />
        <NovelCardComponent
          title="Последний мечник"
          country="Китай"
          :image-src="'https://placehold.co/160x200?text=Cover'"
          slug="last-swordsman"
        />
        <NovelCardComponent
          title="Императорская гвардия"
          country="Япония"
          :image-src="'invalid-url.jpg'"
          slug="imperial-guard"
        />
      </div>
      <div class="divider my-8 border-t border-gray-700"></div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <h2 class="text-white text-xl mb-4">Пример с тегами</h2>
      <div class="flex flex-wrap gap-4">
        <NovelCardWithTags
          title="Великий демон"
          description="История о великом демоне, который был призван в мир людей..."
          :image-src="'https://placehold.co/160x240?text=Cover'"
          :tags="[
            { id: 1, name: 'Фэнтези' },
            { id: 2, name: 'Боевик' },
            { id: 3, name: 'Приключения' },
          ]"
        />
        <NovelCardWithTags
          title="Путь воина"
          description="Путешествие молодого воина в поисках силы и мудрости..."
          :image-src="'https://placehold.co/160x240?text=Cover'"
          :tags="[
            { id: 4, name: 'Экшен' },
            { id: 5, name: 'Драма' },
          ]"
        />
      </div>
    </div>
  </main>
</template>
