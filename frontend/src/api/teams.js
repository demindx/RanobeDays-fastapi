import { get, post, patch, del } from './client'

export function fetchTeams() {
  return get('/api/v1/teams/')
}

export function fetchTeam(id) {
  return get(`/api/v1/teams/${id}`)
}

export function createTeam(data) {
  return post('/api/v1/teams/', data)
}

export function updateTeam(id, data) {
  return patch(`/api/v1/teams/${id}`, data)
}

export function deleteTeam(id) {
  return del(`/api/v1/teams/${id}`)
}

export function fetchTeamUsers(id) {
  return get(`/api/v1/teams/${id}/users`)
}

export function addUserToTeam(id, data) {
  return patch(`/api/v1/teams/${id}/users`, data)
}

export function removeUserFromTeam(id, userId) {
  return del(`/api/v1/teams/${id}/users/${userId}`)
}

export function fetchTeamNovels(id) {
  return get(`/api/v1/teams/${id}/novels`)
}
