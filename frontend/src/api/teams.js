import { get, post, patch, del } from './client'

export function fetchTeams() {
  return get('/teams/')
}

export function fetchTeam(id) {
  return get(`/teams/${id}`)
}

export function createTeam(data) {
  return post('/teams/', data)
}

export function updateTeam(id, data) {
  return patch(`/teams/${id}`, data)
}

export function deleteTeam(id) {
  return del(`/teams/${id}`)
}

export function fetchTeamUsers(id) {
  return get(`/teams/${id}/users`)
}

export function addUserToTeam(id, data) {
  return patch(`/teams/${id}/users`, data)
}

export function removeUserFromTeam(id, userId) {
  return del(`/teams/${id}/users/${userId}`)
}

export function fetchTeamNovels(id) {
  return get(`/teams/${id}/novels`)
}
