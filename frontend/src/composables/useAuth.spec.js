import { beforeEach, describe, expect, it, vi } from 'vitest'

const authApi = vi.hoisted(() => ({
  loginUser: vi.fn(),
  registerUser: vi.fn(),
  logoutUser: vi.fn(),
  fetchProfile: vi.fn(),
}))

vi.mock('../api/auth', () => authApi)
vi.mock('../api/client', () => ({ hasAuthToken: () => false }))

import { useAuth } from './useAuth'

describe('useAuth session consistency', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
    authApi.loginUser.mockResolvedValue({ access_token: 'token' })
    authApi.fetchProfile.mockResolvedValue({
      email: 'reader@example.com',
      user_profile: { nickname: 'Reader' },
    })
    authApi.logoutUser.mockResolvedValue(true)
  })

  it('revokes the local session if loading the profile after login fails', async () => {
    authApi.fetchProfile.mockRejectedValue(new Error('profile unavailable'))

    const result = await useAuth().login('reader', 'password')

    expect(result.ok).toBe(false)
    expect(authApi.logoutUser).toHaveBeenCalledOnce()
    expect(useAuth().isAuthenticated.value).toBe(false)
  })

  it('clears local state even when the backend logout request fails', async () => {
    const auth = useAuth()
    await auth.login('reader', 'password')
    expect(auth.isAuthenticated.value).toBe(true)
    authApi.logoutUser.mockRejectedValue(new Error('offline'))

    await expect(auth.logout()).resolves.toBeUndefined()
    expect(auth.isAuthenticated.value).toBe(false)
    expect(auth.user.value).toBeNull()
  })
})
