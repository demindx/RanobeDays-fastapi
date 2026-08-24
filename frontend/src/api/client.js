const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

const TOKEN_KEY = 'ranobe-api-token'

function loadToken() {
  if (typeof window === 'undefined') return null
  try {
    return window.localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

function persistToken(token) {
  if (typeof window === 'undefined') return
  try {
    if (token) window.localStorage.setItem(TOKEN_KEY, token)
    else window.localStorage.removeItem(TOKEN_KEY)
  } catch {
    return
  }
}

let authToken = loadToken()

export function setAuthToken(token) {
  authToken = token
  persistToken(token)
}

export function clearAuthToken() {
  authToken = null
  persistToken(null)
}

export function hasAuthToken() {
  return !!authToken
}

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

export async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`
  const headers = {
    ...options.headers,
  }

  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`
  }

  const config = {
    credentials: 'include',
    ...options,
    headers,
  }

  const isJsonBody =
    config.body &&
    typeof config.body === 'object' &&
    (Array.isArray(config.body) || Object.getPrototypeOf(config.body) === Object.prototype)

  if (isJsonBody) {
    config.headers['Content-Type'] = 'application/json'
    config.body = JSON.stringify(config.body)
  }

  let response
  try {
    response = await fetch(url, config)
  } catch (err) {
    throw new ApiError(err.message || 'Сетевая ошибка', 0, null)
  }

  if (!response.ok) {
    let errorData = null
    try {
      errorData = await response.json()
    } catch {
      // response body is not JSON
    }
    const message =
      errorData?.message ||
      (Array.isArray(errorData?.detail) ? errorData.detail[0]?.msg : null) ||
      `Ошибка ${response.status}`
    throw new ApiError(message, response.status, errorData)
  }

  if (response.status === 204) {
    return null
  }

  const responseText = await response.text()
  if (!responseText) return null

  const json = JSON.parse(responseText)

  if (json && typeof json === 'object' && 'data' in json) {
    return json.data
  }

  return json
}

export function get(endpoint, options = {}) {
  return request(endpoint, { ...options, method: 'GET' })
}

export function post(endpoint, body, options = {}) {
  return request(endpoint, { ...options, method: 'POST', body })
}

export function put(endpoint, body, options = {}) {
  return request(endpoint, { ...options, method: 'PUT', body })
}

export function patch(endpoint, body, options = {}) {
  return request(endpoint, { ...options, method: 'PATCH', body })
}

export function del(endpoint, options = {}) {
  return request(endpoint, { ...options, method: 'DELETE' })
}
