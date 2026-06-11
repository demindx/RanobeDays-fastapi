<script setup>
import { computed, ref } from 'vue'
import { useBookmarks } from '../composables/useBookmarks'
import SettingsIcon from '../components/icons/SettingsIcon.vue'
import AppButton from '../components/shared/AppButton.vue'
import AppEmptyState from '../components/shared/AppEmptyState.vue'
import AppSectionSwitchTransition from '../components/shared/AppSectionSwitchTransition.vue'
import AppTabs from '../components/shared/AppTabs.vue'
import AppViewModeToggle from '../components/shared/AppViewModeToggle.vue'
import BookmarkNovelCard from '../components/cards/BookmarkNovelCard.vue'
import BookmarksSettingsModal from '../components/bookmarks/BookmarksSettingsModal.vue'

const {
  bookmarks,
  activeBookmark,
  activeBookmarkId,
  isSettingsOpen,
  setActive,
  openSettings,
  closeSettings,
} = useBookmarks()

const viewMode = ref('grid')

const bookmarkTabs = computed(() =>
  bookmarks.value.map((b) => ({
    key: b.id,
    label: b.name,
    count: b.items.length,
  })),
)
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
                class="grid grid-cols-2 gap-2.5 min-[480px]:grid-cols-3 sm:gap-3 lg:grid-cols-4"
              >
                <BookmarkNovelCard
                  v-for="item in activeBookmark.items"
                  :key="item.id"
                  :item="item"
                />
              </div>

              <div
                v-else
                class="divide-y divide-zinc-800/60 overflow-hidden rounded-xl border border-zinc-800"
              >
                <div
                  v-for="item in activeBookmark.items"
                  :key="item.id"
                  class="flex items-center gap-3 bg-zinc-900/50 px-4 py-3 transition hover:bg-zinc-800/50 sm:px-5 sm:py-3.5"
                >
                  <div
                    class="h-12 w-9 shrink-0 rounded-md bg-gradient-to-br"
                    :class="item.coverStyle"
                  />
                  <div class="min-w-0 flex-1">
                    <p class="truncate text-sm font-medium text-zinc-200">{{ item.title }}</p>
                    <p class="truncate text-xs text-zinc-500">
                      {{ item.author }} · {{ item.chapterLabel }}
                    </p>
                  </div>
                  <span
                    class="shrink-0 rounded-full bg-zinc-800/70 px-2 py-1 text-xs text-zinc-400"
                  >
                    ★ {{ item.rating }}
                  </span>
                </div>
              </div>
            </template>
          </div>
        </AppSectionSwitchTransition>
      </div>
    </div>

    <BookmarksSettingsModal :open="isSettingsOpen" @close="closeSettings" />
  </div>
</template>
