import { get } from './client'

export function fetchNovels(filters = {}) {
  const params = new URLSearchParams()

  if (filters.search) params.set('search', filters.search)
  if (filters.genres?.length) params.set('genres', filters.genres.join(','))
  if (filters.tags?.length) params.set('tags', filters.tags.join(','))
  if (filters.ageRating) params.set('ageRating', filters.ageRating)
  if (filters.status) params.set('status', filters.status)
  if (filters.yearFrom) params.set('yearFrom', filters.yearFrom)
  if (filters.yearTo) params.set('yearTo', filters.yearTo)
  if (filters.originalLanguage) params.set('originalLanguage', filters.originalLanguage)
  if (filters.translationLanguage) params.set('translationLanguage', filters.translationLanguage)
  if (filters.page) params.set('page', filters.page)
  if (filters.limit) params.set('limit', filters.limit)

  const query = params.toString()
  return get(`/api/novels${query ? `?${query}` : ''}`)
}

export function fetchNovelById(id) {
  return get(`/api/novels/${id}`)
}

export function fetchFeaturedNovels() {
  return get('/api/novels/featured')
}

export function fetchLatestUpdates() {
  return get('/api/novels/updates')
}

export function fetchContinueReading() {
  return get('/api/novels/continue-reading')
}

export function fetchRecommendations() {
  return get('/api/novels/recommendations')
}

export function fetchNovelChapters(novelId) {
  return get(`/api/novels/${novelId}/chapters`)
}

export function fetchNovelComments(novelId, page = 1) {
  return get(`/api/novels/${novelId}/comments?page=${page}`)
}
