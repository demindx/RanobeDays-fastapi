<script setup>
import { onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useAppStore } from '@/stores/app'
import HomeSectionPopularToday from '@/components/home/HomeSectionPopularToday.vue'
import HomeSectionContinueReading from '@/components/home/HomeSectionContinueReading.vue'
import HomeSectionNewChapters from '@/components/home/HomeSectionNewChapters.vue'
import HomeSectionLatestUpdates from '@/components/home/HomeSectionLatestUpdates.vue'
import { useHomeContinueReading } from '@/composables/useHomeContinueReading'
import { useHomePopularToday } from '@/composables/useHomePopularToday'
import { useHomeNewChapters } from '@/composables/useHomeNewChapters'
import { useHomeLatestUpdates } from '@/composables/useHomeLatestUpdates'
import { trackUiEvent } from '@/services/analytics'

const appStore = useAppStore()
const { isLoggedIn } = storeToRefs(appStore)

const continueReading = useHomeContinueReading()
const popularToday = useHomePopularToday()
const newChapters = useHomeNewChapters()
const latestUpdates = useHomeLatestUpdates()

const reloadContinueReading = async () => {
  if (!isLoggedIn.value) {
    continueReading.items.value = []
    continueReading.error.value = ''
    continueReading.isLoading.value = false
    return
  }
  await continueReading.load(isLoggedIn.value)
}

const reloadHome = async () => {
  const tasks = [popularToday.load(), newChapters.load(), latestUpdates.load()]
  if (isLoggedIn.value) {
    tasks.push(continueReading.load(true))
  }
  await Promise.all(tasks)
}

const handleContinueOpen = (item) => {
  trackUiEvent('home_continue_click', { slug: item.slug })
}

const handleNewChapterOpen = (item) => {
  trackUiEvent('home_new_chapter_click', { slug: item.slug, chapter: item.chapter })
}

const handleLatestUpdateOpen = (item) => {
  trackUiEvent('home_latest_update_click', { slug: item.slug, chapter: item.chapter })
}

const handleContinueLogin = () => {
  appStore.login()
  trackUiEvent('home_continue_login_click')
}

watch(
  () => isLoggedIn.value,
  () => {
    void reloadContinueReading()
  },
)

onMounted(() => {
  void reloadHome()
})
</script>

<template>
  <div class="home-page__layout">
    <HomeSectionPopularToday
      :items="popularToday.items.value"
      :is-loading="popularToday.isLoading.value"
      :error="popularToday.error.value"
      @retry="popularToday.load"
    />

    <div class="container mx-auto px-4 py-6 md:py-8 home-page__content">
      <HomeSectionContinueReading
        v-if="isLoggedIn"
        :items="continueReading.items.value"
        :is-loading="continueReading.isLoading.value"
        :error="continueReading.error.value"
        :is-logged-in="isLoggedIn"
        @retry="reloadContinueReading"
        @open-item="handleContinueOpen"
        @login="handleContinueLogin"
      />

      <HomeSectionNewChapters
        :items="newChapters.items.value"
        :is-loading="newChapters.isLoading.value"
        :error="newChapters.error.value"
        @retry="newChapters.load"
        @open-item="handleNewChapterOpen"
      />

      <HomeSectionLatestUpdates
        :items="latestUpdates.items.value"
        :is-loading="latestUpdates.isLoading.value"
        :error="latestUpdates.error.value"
        @retry="latestUpdates.load"
        @open-item="handleLatestUpdateOpen"
      />
    </div>
  </div>
</template>

<style scoped>
.home-page__layout {
  display: grid;
  gap: 0;
  min-width: 0;
}

.home-page__content {
  display: grid;
  gap: 1.25rem;
  min-width: 0;
}

@media (min-width: 1024px) {
  .home-page__content {
    gap: 1.5rem;
  }
}
</style>
