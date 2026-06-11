const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

let authToken = null

export function setAuthToken(token) {
  authToken = token
}

export function clearAuthToken() {
  authToken = null
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
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`
  }

  const config = {
    ...options,
    headers,
  }

  if (config.body && typeof config.body === 'object') {
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
    throw new ApiError(
      errorData?.message || `Ошибка ${response.status}`,
      response.status,
      errorData,
    )
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
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
