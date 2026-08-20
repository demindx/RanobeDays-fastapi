import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchChapters, fetchChapterById } from '../api/chapters'
import { mapChapter, mapChaptersList } from '../api/mapper'

export function useChapter() {
  const route = useRoute()

  const novelId = computed(() => route.params.id)

  const chapterId = computed(() => route.params.chapterId)

  const chapters = ref([])

  const chapter = ref(null)

  watch(
    () => [novelId.value, chapterId.value],
    async ([nid, cid]) => {
      chapter.value = null
      if (!cid) return
      try {
        const [allChapters, chapterData] = await Promise.all([
          fetchChapters(),
          fetchChapterById(cid),
        ])
        chapters.value = mapChaptersList(allChapters).filter(
          (c) => String(c.novel_id) === String(nid),
        )
        chapter.value = mapChapter(chapterData)
      } catch {}
    },
    { immediate: true },
  )

  const currentIndex = computed(() =>
    chapters.value.findIndex((c) => String(c.id) === String(chapterId.value)),
  )

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
