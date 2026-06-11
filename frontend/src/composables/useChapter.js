import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getChapterById, getChapters } from '../mocks/chapterData'

export function useChapter() {
  const route = useRoute()

  const novelId = computed(() => route.params.id)

  const chapterId = computed(() => route.params.chapterId)

  const chapters = computed(() => getChapters(novelId.value))

  const chapter = computed(() => getChapterById(novelId.value, chapterId.value))

  const currentIndex = computed(() => chapters.value.findIndex((c) => c.id === chapterId.value))

  const hasPrev = computed(() => currentIndex.value > 0)

  const hasNext = computed(() => currentIndex.value < chapters.value.length - 1)

  const prevChapterId = computed(() =>
    hasPrev.value ? chapters.value[currentIndex.value - 1]?.id : null,
  )

  const nextChapterId = computed(() =>
    hasNext.value ? chapters.value[currentIndex.value + 1]?.id : null,
  )

  const chapterOptions = computed(() =>
    chapters.value.map((c) => ({
      value: c.id,
      label: `Глава ${c.number}: ${c.title}`,
    })),
  )

  const novelTitle = computed(() =>
    chapters.value.length > 0 ? `Глава ${chapter.value?.number || ''}` : '',
  )

  return {
    novelId,
    chapterId,
    chapter,
    chapters,
    chapterOptions,
    hasPrev,
    hasNext,
    prevChapterId,
    nextChapterId,
    novelTitle,
  }
}
