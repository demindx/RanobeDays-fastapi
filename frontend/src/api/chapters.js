import { get, post, patch, del } from './client'

export function fetchChapters() {
  return get('/api/v1/chapter/')
}

export function fetchChapterById(id) {
  return get(`/api/v1/chapter/${id}`)
}

export function createChapter(data) {
  return post('/api/v1/chapter/', data)
}

export function updateChapter(id, data) {
  return patch(`/api/v1/chapter/${id}`, data)
}

export function deleteChapter(id) {
  return del(`/api/v1/chapter/${id}`)
}
