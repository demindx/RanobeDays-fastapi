import { get, patch } from './client'

export function fetchMe() {
  return get('/api/v1/users/me')
}

export function fetchUsers() {
  return get('/api/v1/users/')
}

export function fetchUserById(id) {
  return get(`/api/v1/users/${id}`)
}

export function fetchUserProfile(id) {
  return get(`/api/v1/users/${id}/profile`)
}

export function updateUserProfile(id, data) {
  return patch(`/api/v1/users/${id}/profile`, data)
}
