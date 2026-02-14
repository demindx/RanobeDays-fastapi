<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import NovelCardComponent from '@/components/novel/NovelCardComponent.vue'
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
    <div class="flex items-center justify-between gap-3 mb-4">
      <h1 class="text-2xl font-semibold">
        Каталог
      </h1>
      <p
        v-if="searchQuery"
        class="text-sm text-rd-text-muted"
      >
        Поиск: "{{ searchQuery }}"
      </p>
    </div>

    <div
      v-if="error"
      class="rounded-md border border-red-500/40 bg-red-950/20 px-4 py-3 mb-4"
      role="alert"
    >
      <p class="text-sm text-red-200 mb-2">
        {{ error }}
      </p>
      <button
        type="button"
        class="inline-flex px-3 py-1.5 rounded-md bg-rd-accent text-rd-text-strong font-semibold text-sm"
        @click="loadNovels"
      >
        Повторить
      </button>
    </div>

    <div
      v-else-if="isLoading"
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
      aria-live="polite"
      aria-busy="true"
    >
      <div
        v-for="index in 5"
        :key="index"
        class="h-[260px] rounded-md bg-[var(--surface-elevated-color)] animate-pulse"
      />
    </div>

    <div
      v-else-if="novels.length === 0"
      class="rounded-md border bg-[var(--surface-elevated-color)] border-[var(--border-soft-color)] px-4 py-6 text-rd-text-muted"
      aria-live="polite"
    >
      По вашему запросу ничего не найдено.
    </div>

    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
      aria-live="polite"
    >
      <NovelCardComponent
        v-for="novel in novels"
        :key="novel.slug"
        :title="novel.title"
        :country="novel.country"
        :slug="novel.slug"
        :image-src="novel.imageSrc"
      />
    </div>
  </section>
</template>
