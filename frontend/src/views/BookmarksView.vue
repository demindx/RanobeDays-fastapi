<script setup>
import { computed, ref } from 'vue'
import { useBookmarks } from '../composables/useBookmarks'
import SettingsIcon from '../components/icons/SettingsIcon.vue'
import AppButton from '../components/shared/AppButton.vue'
import AppEmptyState from '../components/shared/AppEmptyState.vue'
import AppSectionSwitchTransition from '../components/shared/AppSectionSwitchTransition.vue'
import AppTabs from '../components/shared/AppTabs.vue'
import AppViewModeToggle from '../components/shared/AppViewModeToggle.vue'
import NovelGridCard from '../components/cards/NovelGridCard.vue'
import NovelListCard from '../components/cards/NovelListCard.vue'
import BookmarksSettingsModal from '../components/bookmarks/BookmarksSettingsModal.vue'
import { mapBookmarkItem } from '../utils/mapBookmarkItem'

const { bookmarks, activeBookmark, activeBookmarkId, isSettingsOpen, openSettings, closeSettings } =
  useBookmarks()

const viewMode = ref('grid')

const bookmarkTabs = computed(() =>
  bookmarks.value.map((b) => ({
    key: b.id,
    label: b.name,
    count: b.items.length,
  })),
)

const mappedItems = computed(() => (activeBookmark.value?.items || []).map(mapBookmarkItem))
</script>

<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <h1 class="text-xl font-bold text-white sm:text-2xl">Закладки</h1>
      <div class="flex items-center gap-2">
        <AppViewModeToggle v-model="viewMode" />
        <AppButton variant="neutral" size="sm" class="gap-1.5" @click="openSettings">
          <SettingsIcon />
          <span class="hidden sm:inline">Настройки</span>
        </AppButton>
      </div>
    </div>

    <div class="rounded-2xl border border-zinc-700/70 bg-zinc-900/80">
      <AppTabs v-model:model-value="activeBookmarkId" :tabs="bookmarkTabs" />

      <div class="p-4 sm:p-6">
        <AppEmptyState v-if="!bookmarks.length">
          Нет видимых закладок. Включите их в настройках.
          <AppButton
            variant="primary"
            size="sm"
            class="mt-3 block font-semibold"
            @click="openSettings"
          >
            Открыть настройки
          </AppButton>
        </AppEmptyState>

        <AppSectionSwitchTransition v-else>
          <div :key="activeBookmarkId">
            <AppEmptyState v-if="!activeBookmark"> Выберите закладку выше. </AppEmptyState>

            <AppEmptyState v-else-if="!activeBookmark.items.length">
              В этой закладке пока нет новел.
            </AppEmptyState>

            <template v-else>
              <div
                v-if="viewMode === 'grid'"
                class="grid grid-cols-2 gap-2 min-[480px]:gap-2.5 sm:gap-3 lg:grid-cols-4 xl:grid-cols-5"
              >
                <NovelGridCard
                  v-for="(item, idx) in mappedItems"
                  :key="activeBookmark.items[idx]?.id || idx"
                  :novel="item"
                />
              </div>

              <div v-else class="space-y-3">
                <NovelListCard
                  v-for="(item, idx) in mappedItems"
                  :key="activeBookmark.items[idx]?.id || idx"
                  :novel="item"
                />
              </div>
            </template>
          </div>
        </AppSectionSwitchTransition>
      </div>
    </div>

    <BookmarksSettingsModal :open="isSettingsOpen" @close="closeSettings" />
  </div>
</template>
