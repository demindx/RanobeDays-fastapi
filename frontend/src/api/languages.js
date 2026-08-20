import { get, post } from './client'

export function fetchLanguages() {
  return get('/api/v1/lang/')
}

export function fetchLanguage(id) {
  return get(`/api/v1/lang/${id}`)
}

export function createLanguage(name) {
  return post('/api/v1/lang/', { name })
}
