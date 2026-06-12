import { computed, ref, watch } from 'vue'
import { useBookmarks } from './useBookmarks'
import { getNovelById, novelPageData } from '../mocks/novelPageData'

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

  const novel = computed(() => getNovelById(novelIdRef.value) || novelPageData[0] || null)

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
