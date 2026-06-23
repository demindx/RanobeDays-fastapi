import { get, post } from './client'

export function fetchLanguages() {
  return get('/lang/')
}

export function fetchLanguage(id) {
  return get(`/lang/${id}`)
}

export function createLanguage(name) {
  return post('/lang/', { name })
}
