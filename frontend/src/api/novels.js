import { get } from './client'

export function fetchNovels(options = {}) {
  return get('/api/v1/novel/?limit=100', options)
}

export function fetchNovelById(id) {
  return get(`/api/v1/novel/${id}`)
}
