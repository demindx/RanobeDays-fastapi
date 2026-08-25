import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchChapters, fetchChapterById } from '../api/chapters'
import { mapChapter, mapChaptersList } from '../api/mapper'
import { useAsyncState } from './useAsyncState'
import { getChapterNavigation } from '../utils/chapterNavigation'

export function useChapter() {
  const route = useRoute()

  const novelId = computed(() => route.params.id)

  const chapterId = computed(() => route.params.chapterId)

  const chapters = ref([])

  const chapter = ref(null)

  const { loading, error, run } = useAsyncState()

  watch(
    () => [novelId.value, chapterId.value],
    async ([nid, cid]) => {
      chapter.value = null
      if (!cid) return
      const result = await run(() => Promise.all([fetchChapters(), fetchChapterById(cid)]))
      if (!result) return
      const [allChapters, chapterData] = result
      const filteredChapters = mapChaptersList(allChapters).filter(
        (c) => String(c.novel_id) === String(nid),
      )
      chapters.value = getChapterNavigation(filteredChapters, cid).chapters
      chapter.value = mapChapter(chapterData)
    },
    { immediate: true },
  )

  const navigation = computed(() => getChapterNavigation(chapters.value, chapterId.value))

  const hasPrev = computed(() => navigation.value.prevChapterId !== null)

  const hasNext = computed(() => navigation.value.nextChapterId !== null)

  const prevChapterId = computed(() => navigation.value.prevChapterId)

  const nextChapterId = computed(() => navigation.value.nextChapterId)

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
    loading,
    error,
  }
}
