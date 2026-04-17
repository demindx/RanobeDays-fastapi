import { computed, reactive } from 'vue'

const createIncludeExclude = () => ({ include: [], exclude: [] })

export const createCatalogFilters = () => ({
	releaseYears: createIncludeExclude(),
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
		Object.keys(filters).forEach((key) => {
			filters[key].include = []
			filters[key].exclude = []
		})
	}

	const activeFiltersCount = computed(() =>
		Object.values(filters).reduce((acc, current) => acc + current.include.length + current.exclude.length, 0)
	)

	const filteredNovels = computed(() =>
		novelsRef.value.filter(
			(item) =>
				matchesFilter(item.releaseYear, filters.releaseYears) &&
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
		toggleValue,
		resetFilters
	}
}
