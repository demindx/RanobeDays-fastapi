<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import NovelPosterCard from '@/components/novel/NovelPosterCard.vue'
import StatePanel from '@/components/common/StatePanel.vue'
import SectionAccentTitle from '@/components/common/SectionAccentTitle.vue'
import { fetchCatalogNovels } from '@/services/novels'

const route = useRoute()
const novels = ref([])
const isLoading = ref(false)
const error = ref('')

const searchQuery = computed(() => String(route.query.q || '').trim())

const loadNovels = async () => {
  isLoading.value = true
  error.value = ''

  try {
    novels.value = await fetchCatalogNovels(searchQuery.value)
  } catch {
    error.value = 'Не удалось загрузить каталог. Попробуйте снова.'
    novels.value = []
  } finally {
    isLoading.value = false
  }
}

watch(
  () => route.query.q,
  () => {
    void loadNovels()
  },
  { immediate: true },
)
</script>

<template>
  <section class="container mx-auto px-4 py-8 text-white">
    <div class="mb-4 flex flex-col items-start gap-2 sm:flex-row sm:items-center sm:justify-between sm:gap-3">
      <SectionAccentTitle as="h1">
        Каталог
      </SectionAccentTitle>
      <p
        v-if="searchQuery"
        class="max-w-full break-words text-sm text-rd-text-muted sm:max-w-[60%] sm:text-right"
      >
        Поиск: "{{ searchQuery }}"
      </p>
    </div>

    <StatePanel
      v-if="error"
      title="Ошибка загрузки"
      :description="error"
      variant="error"
      action-label="Повторить"
      @action="loadNovels"
    />

    <div
      v-else-if="isLoading"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-rd-4"
      aria-live="polite"
      aria-busy="true"
      aria-label="Загрузка каталога"
    >
      <div
        v-for="index in 5"
        :key="index"
        class="h-[260px] rounded-rd-md bg-[var(--surface-elevated-color)] animate-pulse"
      />
    </div>

    <StatePanel
      v-else-if="novels.length === 0"
      title="Ничего не найдено"
      description="Попробуйте изменить запрос или убрать фильтры."
      variant="empty"
    />

    <template v-else>
      <h2 class="sr-only">
        Результаты каталога
      </h2>
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-rd-4"
        aria-live="polite"
      >
        <NovelPosterCard
          v-for="novel in novels"
          :key="novel.slug"
          :title="novel.title"
          :country="novel.country"
          :slug="novel.slug"
          :image-src="novel.imageSrc"
          :bookmark-status="novel.bookmarkStatus"
        />
      </div>
    </template>
  </section>
</template>
