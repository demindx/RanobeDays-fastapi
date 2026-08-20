import { get, post, setAuthToken, clearAuthToken } from './client'

const FINGERPRINT_KEY = 'ranobe-fingerprint'

function getFingerprint() {
  if (typeof window === 'undefined') return ''
  try {
    let fingerprint = window.localStorage.getItem(FINGERPRINT_KEY)
    if (!fingerprint) {
      fingerprint = Math.random().toString(36).slice(2) + Date.now().toString(36)
      window.localStorage.setItem(FINGERPRINT_KEY, fingerprint)
    }
    return fingerprint
  } catch {
    return ''
  }
}

export async function loginUser(login, password) {
  const data = await post('/api/v1/auth/login', {
    login,
    password,
    fingerprint: getFingerprint(),
  })
  const token = data?.access_token
  if (token) {
    setAuthToken(token)
  }
  return data
}

export async function registerUser(login, email, password) {
  await post('/api/v1/auth/register', {
    login,
    email,
    nickname: login,
    password1: password,
    password2: password,
  })
  return loginUser(login, password)
}

export async function logoutUser() {
  try {
    await post('/api/v1/auth/logout')
  } finally {
    clearAuthToken()
  }
}

export function fetchProfile() {
  return get('/api/v1/users/me')
}

export async function refreshToken() {
  try {
    const data = await post('/api/v1/auth/refresh')
    const token = data?.access_token
    if (token) {
      setAuthToken(token)
    }
    return data
  } catch {
    clearAuthToken()
    return null
  }
}
