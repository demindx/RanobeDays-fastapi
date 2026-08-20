import { computed, ref, watch } from 'vue'
import { useBookmarks } from './useBookmarks'
import { fetchNovelById } from '../api/novels'
import { fetchChapters } from '../api/chapters'
import { mapNovel, mapChaptersList } from '../api/mapper'
import { useAsyncState } from './useAsyncState'

const RATING_KEY = 'ranobe-ratings'

const loadRatings = () => {
  if (typeof window === 'undefined') return {}
  try {
    return JSON.parse(window.localStorage.getItem(RATING_KEY) || '{}')
  } catch {
    return {}
  }
}

const saveRatings = (ratings) => {
  if (typeof window === 'undefined') return
  window.localStorage.setItem(RATING_KEY, JSON.stringify(ratings))
}

const userRatings = ref(loadRatings())

export const useNovelPage = (novelIdRef) => {
  const activeTab = ref('description')
  const selectedBookmarkId = ref('')
  const isBookmarkManuallyCleared = ref(false)
  const { bookmarks } = useBookmarks()

  const novel = ref(null)
  const chapters = ref([])
  const { loading, error, run } = useAsyncState()

  watch(
    novelIdRef,
    async (id) => {
      novel.value = null
      chapters.value = []
      if (!id) return
      const result = await run(() => Promise.all([fetchNovelById(id), fetchChapters()]))
      if (!result) return
      const [novelData, chaptersData] = result
      const mapped = mapNovel(novelData)
      if (!mapped) return
      chapters.value = mapChaptersList(chaptersData).filter(
        (c) => String(c.novel_id) === String(id),
      )
      mapped.chapters = chapters.value
      novel.value = mapped
    },
    { immediate: true },
  )

  const bookmarkOptions = computed(() =>
    bookmarks.value.map((bookmark) => ({
      value: bookmark.id,
      label: bookmark.name,
    })),
  )

  const readingCtaLabel = computed(() => {
    if (!novel.value) return 'Читать'
    return (novel.value.readingProgress || 0) > 0 ? 'Продолжить чтение' : 'Читать'
  })

  const setActiveTab = (tab) => {
    if (tab !== 'description' && tab !== 'chapters') return
    activeTab.value = tab
  }

  const selectBookmark = (bookmarkId) => {
    selectedBookmarkId.value = String(bookmarkId || '')
    isBookmarkManuallyCleared.value = false
  }

  const removeFromBookmarks = () => {
    selectedBookmarkId.value = ''
    isBookmarkManuallyCleared.value = true
  }

  watch(
    bookmarkOptions,
    (options) => {
      if (!options.length) {
        selectedBookmarkId.value = ''
        return
      }
      if (!selectedBookmarkId.value) {
        if (!isBookmarkManuallyCleared.value) {
          selectedBookmarkId.value = String(options[0].value)
        }
        return
      }
      if (options.some((option) => String(option.value) === selectedBookmarkId.value)) return
      selectedBookmarkId.value = String(options[0].value)
    },
    { immediate: true },
  )

  const userRating = computed(() => userRatings.value[novelIdRef.value] || 0)

  const setUserRating = (rating) => {
    const val = Math.max(0, Math.min(5, Math.round(rating)))
    userRatings.value = { ...userRatings.value, [novelIdRef.value]: val }
    saveRatings(userRatings.value)
  }

  return {
    novel,
    chapters,
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
  }
}
