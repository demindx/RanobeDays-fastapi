import { get, post } from './client'

export function fetchCountries() {
  return get('/country/')
}

export function fetchCountry(id) {
  return get(`/country/${id}`)
}

export function createCountry(name) {
  return post('/country/', { name })
}
