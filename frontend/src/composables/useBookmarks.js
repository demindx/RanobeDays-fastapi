import { computed, ref } from 'vue'
import { initialBookmarks } from '../mocks/bookmarksData'

const normalizeName = (value) =>
  String(value ?? '')
    .trim()
    .replace(/\s+/g, ' ')

const cloneBookmarks = () =>
  initialBookmarks.map((bookmark) => ({
    ...bookmark,
    items: bookmark.items.map((item) => ({ ...item })),
  }))

const bookmarks = ref(cloneBookmarks())
const isSettingsOpen = ref(false)
const activeBookmarkId = ref(bookmarks.value[0]?.id || null)

const sortByOrder = (list) => [...list].sort((a, b) => a.order - b.order)

export const useBookmarks = () => {
  const sortedBookmarks = computed(() => sortByOrder(bookmarks.value))
  const activeBookmark = computed(
    () => sortedBookmarks.value.find((bookmark) => bookmark.id === activeBookmarkId.value) || null,
  )

  const setActive = (bookmarkId) => {
    if (!sortedBookmarks.value.some((bookmark) => bookmark.id === bookmarkId)) return
    activeBookmarkId.value = bookmarkId
  }

  const openSettings = () => {
    isSettingsOpen.value = true
  }

  const closeSettings = () => {
    isSettingsOpen.value = false
  }

  const togglePrivacy = (bookmarkId) => {
    const target = bookmarks.value.find((bookmark) => bookmark.id === bookmarkId)
    if (!target) return
    target.isPublic = !target.isPublic
  }

  const hasNameConflict = (name, ignoreId = null) => {
    const normalized = normalizeName(name).toLowerCase()
    return bookmarks.value.some(
      (bookmark) =>
        bookmark.id !== ignoreId && normalizeName(bookmark.name).toLowerCase() === normalized,
    )
  }

  const renameBookmark = (bookmarkId, nextName) => {
    const target = bookmarks.value.find((bookmark) => bookmark.id === bookmarkId)
    if (!target) return { ok: false, error: 'Закладка не найдена.' }

    const normalized = normalizeName(nextName)
    if (!normalized) return { ok: false, error: 'Название не может быть пустым.' }
    if (hasNameConflict(normalized, bookmarkId))
      return { ok: false, error: 'Закладка с таким названием уже существует.' }

    target.name = normalized
    return { ok: true }
  }

  const createBookmark = (name) => {
    const normalized = normalizeName(name)
    if (!normalized) return { ok: false, error: 'Введите название новой закладки.' }
    if (hasNameConflict(normalized))
      return { ok: false, error: 'Закладка с таким названием уже существует.' }

    const maxOrder = bookmarks.value.reduce((max, bookmark) => Math.max(max, bookmark.order), 0)
    const id = `bookmark-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`
    bookmarks.value.push({
      id,
      name: normalized,
      isPublic: true,
      order: maxOrder + 1,
      items: [],
    })
    return { ok: true }
  }

  return {
    bookmarks: sortedBookmarks,
    activeBookmark,
    activeBookmarkId,
    isSettingsOpen,
    setActive,
    openSettings,
    closeSettings,
    togglePrivacy,
    renameBookmark,
    createBookmark,
  }
}
