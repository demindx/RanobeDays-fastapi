import { beforeEach, describe, expect, it, vi } from 'vitest'
import { clearAuthToken, get, post, request } from './client'

const jsonResponse = (body, init = {}) =>
  new Response(JSON.stringify(body), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })

describe('API client request contract', () => {
  beforeEach(() => {
    clearAuthToken()
    vi.restoreAllMocks()
  })

  it('includes browser credentials without forcing a JSON content type on GET', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(jsonResponse({ data: [] }))

    await get('/api/v1/novel/')

    const [, config] = fetchMock.mock.calls[0]
    expect(config.credentials).toBe('include')
    expect(config.headers).not.toHaveProperty('Content-Type')
  })

  it('serializes an object body and marks it as JSON', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(jsonResponse({ data: null }))

    await post('/api/v1/auth/login', { login: 'reader' })

    const [, config] = fetchMock.mock.calls[0]
    expect(config.credentials).toBe('include')
    expect(config.headers['Content-Type']).toBe('application/json')
    expect(config.body).toBe('{"login":"reader"}')
  })

  it('passes FormData through without overriding its content type', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(jsonResponse({ data: null }))
    const form = new FormData()
    form.set('cover', new Blob(['image']))

    await post('/api/v1/cover', form)

    const [, config] = fetchMock.mock.calls[0]
    expect(config.body).toBe(form)
    expect(config.headers).not.toHaveProperty('Content-Type')
  })

  it('returns null for any successful response without a body', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(null, { status: 200 }))

    await expect(request('/api/v1/empty')).resolves.toBeNull()
  })
})
