<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppEmptyState from '../components/shared/AppEmptyState.vue'
import AppLoading from '../components/shared/AppLoading.vue'
import AppSectionSwitchTransition from '../components/shared/AppSectionSwitchTransition.vue'
import NovelPageLayout from '../components/novel/NovelPageLayout.vue'
import NovelSidebar from '../components/novel/NovelSidebar.vue'
import NovelTabs from '../components/novel/NovelTabs.vue'
import NovelDescriptionTab from '../components/novel/NovelDescriptionTab.vue'
import NovelChaptersTab from '../components/novel/NovelChaptersTab.vue'
import { useNovelPage } from '../composables/useNovelPage'

const route = useRoute()
const novelId = computed(() => String(route.params.id || '1'))
const {
  novel,
  loading,
  error,
  activeTab,
  bookmarkOptions,
  selectedBookmarkId,
  readingCtaLabel,
  userRating,
  setActiveTab,
  selectBookmark,
  removeFromBookmarks,
  setUserRating,
} = useNovelPage(novelId)

const currentTabComponent = computed(() =>
  activeTab.value === 'description' ? NovelDescriptionTab : NovelChaptersTab,
)
</script>

<template>
  <div>
    <AppLoading v-if="loading" label="Загрузка новеллы..." />

    <AppEmptyState v-else-if="error">
      {{ error }}
    </AppEmptyState>

    <AppEmptyState v-else-if="!novel"> Новела не найдена. </AppEmptyState>

    <NovelPageLayout v-else>
      <template #sidebar>
        <NovelSidebar
          :novel="novel"
          :bookmark-options="bookmarkOptions"
          :selected-bookmark-id="selectedBookmarkId"
          :reading-cta-label="readingCtaLabel"
          :user-rating="userRating"
          @update-rating="setUserRating"
          @update-bookmark="selectBookmark"
          @remove-bookmark="removeFromBookmarks"
        />
      </template>

      <template #content>
        <div class="space-y-3">
          <div class="rounded-2xl border border-zinc-700/70 bg-zinc-900/70 p-3 sm:p-4">
            <h1 class="text-xl font-semibold text-white sm:text-2xl">{{ novel.title }}</h1>
          </div>

          <NovelTabs :active-tab="activeTab" @change="setActiveTab" />

          <AppSectionSwitchTransition>
            <component
              :is="currentTabComponent"
              :key="activeTab"
              :novel="activeTab === 'description' ? novel : undefined"
              :novel-id="activeTab === 'chapters' ? novelId : undefined"
              :chapters="activeTab === 'chapters' ? novel.chapters : undefined"
            />
          </AppSectionSwitchTransition>
        </div>
      </template>
    </NovelPageLayout>
  </div>
</template>
