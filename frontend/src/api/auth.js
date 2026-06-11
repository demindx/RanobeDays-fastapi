import { get, post, setAuthToken, clearAuthToken } from './client'

export async function loginUser(login, password) {
  const data = await post('/api/auth/login', { login, password })
  if (data.token) {
    setAuthToken(data.token)
  }
  return data
}

export async function registerUser(login, email, password) {
  const data = await post('/api/auth/register', { login, email, password })
  if (data.token) {
    setAuthToken(data.token)
  }
  return data
}

export async function logoutUser() {
  try {
    await post('/api/auth/logout')
  } finally {
    clearAuthToken()
  }
}

export function fetchProfile() {
  return get('/api/auth/profile')
}

export async function refreshToken() {
  try {
    const data = await post('/api/auth/refresh')
    if (data.token) {
      setAuthToken(data.token)
    }
    return data
  } catch {
    clearAuthToken()
    return null
  }
}
