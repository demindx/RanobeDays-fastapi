<script setup>
import { onMounted, ref } from 'vue'
import NovelCarouselSection from '../components/home/NovelCarouselSection.vue'
import LatestUpdatesSection from '../components/home/LatestUpdatesSection.vue'
import ContinueReadingSection from '../components/home/ContinueReadingSection.vue'
import YouMayLikeSection from '../components/home/YouMayLikeSection.vue'
import AppLoading from '../components/shared/AppLoading.vue'
import { fetchNovels } from '../api/novels'
import { fetchChapters } from '../api/chapters'
import { mapChaptersList, mapNovelsList } from '../api/mapper'
import { useAsyncState } from '../composables/useAsyncState'
import {
  featuredNovels as fallbackFeaturedNovels,
  latestUpdates as fallbackLatestUpdates,
  continueReading as fallbackContinueReading,
  youMayLike as fallbackYouMayLike,
} from '../mocks/homePageData'

const featuredNovels = ref(fallbackFeaturedNovels)
const latestUpdates = ref(fallbackLatestUpdates)
const continueReading = ref(fallbackContinueReading)
const youMayLike = ref(fallbackYouMayLike)
const { loading, run } = useAsyncState()

const relativeTime = (dateValue) => {
  if (!dateValue) return 'недавно'
  const ageInMinutes = Math.max(0, Math.floor((Date.now() - new Date(dateValue)) / 60000))
  if (ageInMinutes < 60) return `${Math.max(1, ageInMinutes)} мин. назад`
  if (ageInMinutes < 1440) return `${Math.floor(ageInMinutes / 60)} ч. назад`
  return `${Math.floor(ageInMinutes / 1440)} дн. назад`
}

const toHomeNovel = (novel) => ({
  ...novel,
  genre: novel.genres?.[0] || novel.type || 'Новелла',
  chapter: novel.chapterCount ? `Глава ${novel.chapterCount}` : 'Новые главы',
  chapters: novel.chapterCount || 0,
  href: `/novel/${novel.id}`,
})

onMounted(async () => {
  const result = await run(() => Promise.all([fetchNovels(), fetchChapters()]))
  if (!result) return

  const [novelsData, chaptersData] = result
  const novels = mapNovelsList(novelsData)
  const chapters = mapChaptersList(chaptersData)
  if (!novels.length) return

  const novelsById = new Map(novels.map((novel) => [String(novel.id), novel]))
  const chapterCount = new Map()
  chapters.forEach((chapter) => {
    const key = String(chapter.novel_id)
    chapterCount.set(key, (chapterCount.get(key) || 0) + 1)
  })

  const homeNovels = novels.map((novel) =>
    toHomeNovel({ ...novel, chapterCount: chapterCount.get(String(novel.id)) || 0 }),
  )
  featuredNovels.value = homeNovels.slice(0, 8)
  youMayLike.value = homeNovels.slice(8, 13).map((novel) => ({
    id: novel.id,
    novelId: novel.id,
    title: novel.title,
    genre: novel.genre,
    rating: novel.rating || '—',
    href: `/novel/${novel.id}`,
  }))

  latestUpdates.value = chapters
    .slice()
    .sort((a, b) => new Date(b.publishedAt || 0) - new Date(a.publishedAt || 0))
    .slice(0, 15)
    .map((chapter) => ({
      id: chapter.id,
      novelId: chapter.novel_id,
      novelTitle: novelsById.get(String(chapter.novel_id))?.title || 'Неизвестная новелла',
      chapter: `Глава ${chapter.number}: ${chapter.title}`,
      timeAgo: relativeTime(chapter.publishedAt),
      href: `/novel/${chapter.novel_id}/chapter/${chapter.id}`,
    }))
})
</script>

<template>
  <div class="flex flex-col gap-6 md:gap-8">
    <AppLoading v-if="loading" label="Загрузка новелл..." />
    <NovelCarouselSection :novels="featuredNovels" />
    <ContinueReadingSection :items="continueReading" />

    <div class="grid gap-6 lg:grid-cols-10">
      <div class="lg:col-span-7">
        <LatestUpdatesSection :updates="latestUpdates" />
      </div>
      <div class="lg:col-span-3">
        <YouMayLikeSection :items="youMayLike" />
      </div>
    </div>
  </div>
</template>
