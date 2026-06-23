import { get, patch } from './client'

export function fetchMe() {
  return get('/users/me')
}

export function fetchUsers() {
  return get('/users/')
}

export function fetchUserById(id) {
  return get(`/users/${id}`)
}

export function fetchUserProfile(id) {
  return get(`/users/${id}/profile`)
}

export function updateUserProfile(id, data) {
  return patch(`/users/${id}/profile`, data)
}
