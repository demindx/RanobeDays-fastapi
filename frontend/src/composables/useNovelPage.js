import { computed, ref, watch } from 'vue'
import { useBookmarks } from './useBookmarks'
import { getNovelById, novelPageData } from '../mocks/novelPageData'

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

  return {
    novel,
    activeTab,
    bookmarkOptions,
    selectedBookmarkId,
    readingCtaLabel,
    setActiveTab,
    selectBookmark,
    removeFromBookmarks,
  }
}
