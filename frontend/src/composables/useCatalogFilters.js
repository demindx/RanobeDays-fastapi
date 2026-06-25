import { computed, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const createIncludeExclude = () => ({ include: [], exclude: [] })
const createYearRange = () => ({ from: '', to: '' })

const FILTER_KEYS = ['ageRatings', 'genres', 'tags', 'originalLanguages', 'translationLanguages']

export const createCatalogFilters = () => ({
  releaseYearRange: createYearRange(),
  ageRatings: createIncludeExclude(),
  genres: createIncludeExclude(),
  tags: createIncludeExclude(),
  originalLanguages: createIncludeExclude(),
  translationLanguages: createIncludeExclude(),
})

const toArray = (value) => (Array.isArray(value) ? value : [value])

const parseQueryList = (value) => {
  if (!value) return []
  if (Array.isArray(value)) return value
  return value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

const matchesFilter = (novelValue, filterState) => {
  const values = toArray(novelValue)
  const include = filterState.include
  const exclude = filterState.exclude

  if (exclude.some((item) => values.includes(item))) return false
  if (!include.length) return true
  return include.some((item) => values.includes(item))
}

export const useCatalogFilters = (novelsRef) => {
  const route = useRoute()
  const router = useRouter()
  const filters = reactive(createCatalogFilters())

  let isApplyingFromUrl = false

  const applyQueryToFilters = () => {
    isApplyingFromUrl = true
    const q = route.query

    filters.releaseYearRange.from = String(q.yearFrom ?? '')
    filters.releaseYearRange.to = String(q.yearTo ?? '')

    for (const key of FILTER_KEYS) {
      filters[key].include = parseQueryList(q[key])
      filters[key].exclude = parseQueryList(q[key + 'Exclude'])
    }
    isApplyingFromUrl = false
  }

  watch(() => route.query, applyQueryToFilters, { immediate: true })

  const buildQueryFromFilters = () => {
    const query = {}
    if (filters.releaseYearRange.from) query.yearFrom = filters.releaseYearRange.from
    if (filters.releaseYearRange.to) query.yearTo = filters.releaseYearRange.to
    for (const key of FILTER_KEYS) {
      if (filters[key].include.length) query[key] = filters[key].include.join(',')
      if (filters[key].exclude.length) query[key + 'Exclude'] = filters[key].exclude.join(',')
    }
    return query
  }

  const syncUrl = () => {
    if (isApplyingFromUrl) return
    router.replace({ query: buildQueryFromFilters() })
  }

  const setReleaseYearRange = (bound, value) => {
    if (bound !== 'from' && bound !== 'to') return
    const trimmed = String(value ?? '').trim()
    if (filters.releaseYearRange[bound] === trimmed) return
    filters.releaseYearRange[bound] = trimmed
    syncUrl()
  }

  const matchesYearRange = (releaseYear) => {
    const fromRaw = filters.releaseYearRange.from
    const toRaw = filters.releaseYearRange.to
    const from = Number.parseInt(fromRaw, 10)
    const to = Number.parseInt(toRaw, 10)
    const hasFrom = Number.isFinite(from)
    const hasTo = Number.isFinite(to)
    if (!hasFrom && !hasTo) return true
    if (hasFrom && releaseYear < from) return false
    if (hasTo && releaseYear > to) return false
    return true
  }

  const toggleValue = (filterKey, mode, value) => {
    const target = filters[filterKey]
    if (!target) return
    const oppositeMode = mode === 'include' ? 'exclude' : 'include'
    target[oppositeMode] = target[oppositeMode].filter((item) => item !== value)
    if (target[mode].includes(value)) {
      target[mode] = target[mode].filter((item) => item !== value)
    } else {
      target[mode] = [...target[mode], value]
    }
    syncUrl()
  }

  const resetFilters = () => {
    filters.releaseYearRange.from = ''
    filters.releaseYearRange.to = ''
    for (const key of FILTER_KEYS) {
      filters[key].include = []
      filters[key].exclude = []
    }
    syncUrl()
  }

  const activeFiltersCount = computed(() => {
    let count = 0
    if (filters.releaseYearRange.from) count += 1
    if (filters.releaseYearRange.to) count += 1
    for (const key of FILTER_KEYS) {
      count += filters[key].include.length + filters[key].exclude.length
    }
    return count
  })

  const filteredNovels = computed(() =>
    novelsRef.value.filter(
      (item) =>
        matchesYearRange(item.releaseYear) &&
        matchesFilter(item.ageRating, filters.ageRatings) &&
        matchesFilter(item.genres, filters.genres) &&
        matchesFilter(item.tags, filters.tags) &&
        matchesFilter(item.originalLanguage, filters.originalLanguages) &&
        matchesFilter(item.translationLanguage, filters.translationLanguages),
    ),
  )

  return {
    filters,
    filteredNovels,
    activeFiltersCount,
    setReleaseYearRange,
    toggleValue,
    resetFilters,
  }
}
