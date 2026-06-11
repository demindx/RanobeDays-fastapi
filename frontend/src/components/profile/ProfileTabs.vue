<script setup>
import { computed, ref } from 'vue'
import { useProfile } from '../../composables/useProfile'
import TeamCard from './TeamCard.vue'
import AppTabs from '../shared/AppTabs.vue'
import AppEmptyState from '../shared/AppEmptyState.vue'
import BookmarkNovelCard from '../cards/BookmarkNovelCard.vue'
import HeartIcon from '../icons/HeartIcon.vue'
import AppViewModeToggle from '../shared/AppViewModeToggle.vue'
import AppSectionSwitchTransition from '../shared/AppSectionSwitchTransition.vue'

const { user, bookmarks, comments } = useProfile()
const activeTab = ref('teams')
const activeBookmarkId = ref(bookmarks.value[0]?.id || null)

const tabs = [
  { key: 'teams', label: 'Команды', count: user.value.teams.length },
  { key: 'bookmarks', label: 'Закладки', count: user.value.stats.bookmarksCount },
  { key: 'comments', label: 'Комментарии', count: user.value.stats.commentsCount },
]

const bookmarkTabs = computed(() =>
  bookmarks.value.map((b) => ({
    key: b.id,
    label: b.name,
    count: b.novels.length,
  })),
)

const activeBookmark = computed(
  () => bookmarks.value.find((b) => b.id === activeBookmarkId.value) || null,
)

const viewMode = ref('list')
</script>

<template>
  <div class="rounded-2xl border border-zinc-700/70 bg-zinc-900/80">
    <AppTabs v-model:model-value="activeTab" :tabs="tabs" />

    <div class="p-4 sm:p-6">
      <template v-if="activeTab === 'teams'">
        <div v-if="user.teams.length" class="grid grid-cols-4 gap-4 sm:grid-cols-6 md:grid-cols-8">
          <TeamCard
            v-for="team in user.teams"
            :key="team.id"
            :name="team.name"
            :avatar-color-class="team.avatarColorClass"
          />
        </div>
        <AppEmptyState v-else compact> Пользователь не состоит в командах. </AppEmptyState>
      </template>

      <template v-if="activeTab === 'bookmarks'">
        <div v-if="bookmarks.length" class="flex items-center justify-between gap-2">
          <AppTabs v-model:model-value="activeBookmarkId" :tabs="bookmarkTabs" class="flex-1" />
          <AppViewModeToggle v-model="viewMode" />
        </div>

        <div class="mt-3">
          <AppEmptyState v-if="!activeBookmark"> Нет активной закладки. </AppEmptyState>

          <AppEmptyState v-else-if="!activeBookmark.novels.length">
            В этой закладке пока нет новел.
          </AppEmptyState>

          <template v-else>
            <AppSectionSwitchTransition>
              <div :key="activeBookmarkId">
                <div
                  v-if="viewMode === 'list'"
                  class="divide-y divide-zinc-800/60 overflow-hidden rounded-xl border border-zinc-800"
                >
                  <div
                    v-for="item in activeBookmark.novels"
                    :key="item.id"
                    class="flex items-center gap-3 bg-zinc-900/50 px-4 py-3 transition hover:bg-zinc-800/50 sm:px-5 sm:py-3.5"
                  >
                    <div
                      class="h-12 w-9 shrink-0 rounded-md bg-gradient-to-br"
                      :class="item.coverStyle"
                    />
                    <div class="min-w-0 flex-1">
                      <p class="truncate text-sm font-medium text-zinc-200">
                        {{ item.title }}
                      </p>
                      <p class="truncate text-xs text-zinc-500">
                        {{ item.author }} · {{ item.chapterLabel }}
                      </p>
                    </div>
                    <div
                      class="flex shrink-0 items-center gap-1 rounded-full bg-zinc-800/70 px-2 py-1 text-xs text-zinc-400"
                    >
                      <span class="text-lime-400">★</span>
                      {{ item.rating }}
                    </div>
                  </div>
                </div>

                <div
                  v-else
                  class="grid grid-cols-2 gap-2.5 min-[480px]:grid-cols-3 sm:gap-3 lg:grid-cols-4"
                >
                  <BookmarkNovelCard
                    v-for="item in activeBookmark.novels"
                    :key="item.id"
                    :item="item"
                  />
                </div>
              </div>
            </AppSectionSwitchTransition>
          </template>
        </div>
      </template>

      <template v-if="activeTab === 'comments'">
        <div v-if="comments.length" class="space-y-3">
          <div
            v-for="comment in comments"
            :key="comment.id"
            class="rounded-lg border border-zinc-800 bg-zinc-900/50 px-4 py-3"
          >
            <div class="mb-1 flex items-center gap-2 text-xs text-zinc-500">
              <span>{{ new Date(comment.date).toLocaleDateString('ru-RU') }}</span>
              <span class="text-zinc-600">•</span>
              <span class="text-lime-400">{{ comment.novelTitle }}</span>
            </div>
            <p class="text-sm leading-relaxed text-zinc-300">{{ comment.text }}</p>
            <div class="mt-2 flex items-center gap-1 text-xs text-zinc-500">
              <HeartIcon />
              {{ comment.likes }}
            </div>
          </div>
        </div>
        <AppEmptyState v-else compact> Комментариев пока нет. </AppEmptyState>
      </template>
    </div>
  </div>
</template>
