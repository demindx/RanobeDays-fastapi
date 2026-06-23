import { get, post, patch, del } from './client'

export function fetchChapters() {
  return get('/chapter/')
}

export function fetchChapterById(id) {
  return get(`/chapter/${id}`)
}

export function createChapter(data) {
  return post('/chapter/', data)
}

export function updateChapter(id, data) {
  return patch(`/chapter/${id}`, data)
}

export function deleteChapter(id) {
  return del(`/chapter/${id}`)
}
