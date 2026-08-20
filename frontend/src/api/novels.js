import { get } from './client'

export function fetchNovels() {
  return get('/api/v1/novel/')
}

export function fetchNovelById(id) {
  return get(`/api/v1/novel/${id}`)
}
