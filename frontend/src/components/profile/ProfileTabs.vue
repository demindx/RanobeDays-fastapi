<script setup>
import { computed, ref } from 'vue'
import { useProfile } from '../../composables/useProfile'
import TeamCard from './TeamCard.vue'
import AppTabs from '../shared/AppTabs.vue'
import AppEmptyState from '../shared/AppEmptyState.vue'
import NovelGridCard from '../cards/NovelGridCard.vue'
import NovelListCard from '../cards/NovelListCard.vue'
import HeartIcon from '../icons/HeartIcon.vue'
import AppViewModeToggle from '../shared/AppViewModeToggle.vue'
import AppSectionSwitchTransition from '../shared/AppSectionSwitchTransition.vue'
import { catalogNovels } from '../../mocks/catalogData'

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

const toNovelShape = (item) => {
  const catalogId = item.novelId ?? item.id
  const novel = catalogNovels.find((n) => n.id === catalogId)
  const chapterNum = parseInt(String(item.chapterLabel || '').replace(/\D/g, ''), 10) || 0
  return {
    id: catalogId,
    title: item.title,
    author: item.author,
    rating: item.rating,
    coverStyle: item.coverStyle,
    coverUrl: item.coverUrl,
    href: item.href || (catalogId ? `/novel/${catalogId}` : '#'),
    chapters: chapterNum,
    releaseYear: novel?.releaseYear ?? '',
    ageRating: novel?.ageRating ?? '',
    status: novel?.status ?? '',
    synopsis: novel?.synopsis ?? '',
    genres: novel?.genres ?? [],
    tags: novel?.tags ?? [],
    originalLanguage: novel?.originalLanguage ?? '',
    translationLanguage: novel?.translationLanguage ?? '',
  }
}

const mappedNovels = computed(() => (activeBookmark.value?.novels || []).map(toNovelShape))
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
            :id="team.id"
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
                <div v-if="viewMode === 'list'" class="space-y-3">
                  <NovelListCard
                    v-for="(item, idx) in mappedNovels"
                    :key="activeBookmark.novels[idx]?.id || idx"
                    :novel="item"
                  />
                </div>

                <div
                  v-else
                  class="grid grid-cols-2 gap-2 min-[480px]:gap-2.5 sm:gap-3 lg:grid-cols-4 xl:grid-cols-5"
                >
                  <NovelGridCard
                    v-for="(item, idx) in mappedNovels"
                    :key="activeBookmark.novels[idx]?.id || idx"
                    :novel="item"
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
