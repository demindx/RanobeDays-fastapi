import { get, post } from './client'

export function fetchCountries() {
  return get('/api/v1/country/')
}

export function fetchCountry(id) {
  return get(`/api/v1/country/${id}`)
}

export function createCountry(name) {
  return post('/api/v1/country/', { name })
}
