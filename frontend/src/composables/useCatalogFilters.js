import { computed, reactive } from 'vue'

const createIncludeExclude = () => ({ include: [], exclude: [] })
const createYearRange = () => ({ from: '', to: '' })

export const createCatalogFilters = () => ({
	releaseYearRange: createYearRange(),
	ageRatings: createIncludeExclude(),
	genres: createIncludeExclude(),
	tags: createIncludeExclude(),
	originalLanguages: createIncludeExclude(),
	translationLanguages: createIncludeExclude()
})

const toArray = (value) => (Array.isArray(value) ? value : [value])

const matchesFilter = (novelValue, filterState) => {
	const values = toArray(novelValue)
	const include = filterState.include
	const exclude = filterState.exclude

	if (exclude.some((item) => values.includes(item))) return false
	if (!include.length) return true
	return include.some((item) => values.includes(item))
}

export const useCatalogFilters = (novelsRef) => {
	const filters = reactive(createCatalogFilters())

	const setReleaseYearRange = (bound, value) => {
		if (bound !== 'from' && bound !== 'to') return
		const trimmed = String(value ?? '').trim()
		filters.releaseYearRange[bound] = trimmed
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
			return
		}
		target[mode] = [...target[mode], value]
	}

	const resetFilters = () => {
		filters.releaseYearRange.from = ''
		filters.releaseYearRange.to = ''
		Object.keys(filters).forEach((key) => {
			if (key === 'releaseYearRange') return
			filters[key].include = []
			filters[key].exclude = []
		})
	}

	const activeFiltersCount = computed(() => {
		let count = 0
		if (filters.releaseYearRange.from) count += 1
		if (filters.releaseYearRange.to) count += 1
		Object.keys(filters).forEach((key) => {
			if (key === 'releaseYearRange') return
			count += filters[key].include.length + filters[key].exclude.length
		})
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
				matchesFilter(item.translationLanguage, filters.translationLanguages)
		)
	)

	return {
		filters,
		filteredNovels,
		activeFiltersCount,
		setReleaseYearRange,
		toggleValue,
		resetFilters
	}
}
