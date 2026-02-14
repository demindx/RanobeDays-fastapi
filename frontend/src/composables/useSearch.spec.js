import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'

const mockUseRouter = vi.fn()

vi.mock('vue-router', () => ({
  useRouter: () => mockUseRouter(),
}))

describe('useSearch', () => {
  beforeEach(() => {
    mockUseRouter.mockReset()
  })

  it('navigates to catalog with trimmed query', async () => {
    const push = vi.fn().mockResolvedValue(undefined)
    const router = {
      currentRoute: ref({ path: '/', query: {} }),
      push,
    }
    mockUseRouter.mockReturnValue(router)

    const { useSearch } = await import('./useSearch')
    const { search } = useSearch()

    await search('  mushoku tensei  ')

    expect(push).toHaveBeenCalledWith({
      path: '/catalog',
      query: { q: 'mushoku tensei' },
    })
  })

  it('navigates with empty query object for blank input', async () => {
    const push = vi.fn().mockResolvedValue(undefined)
    const router = {
      currentRoute: ref({ path: '/', query: { q: 'old' } }),
      push,
    }
    mockUseRouter.mockReturnValue(router)

    const { useSearch } = await import('./useSearch')
    const { search } = useSearch()

    await search('   ')

    expect(push).toHaveBeenCalledWith({
      path: '/catalog',
      query: {},
    })
  })

  it('does not navigate when already on catalog with same query', async () => {
    const push = vi.fn().mockResolvedValue(undefined)
    const router = {
      currentRoute: ref({ path: '/catalog', query: { q: 'rezero' } }),
      push,
    }
    mockUseRouter.mockReturnValue(router)

    const { useSearch } = await import('./useSearch')
    const { search } = useSearch()

    await search('rezero')

    expect(push).not.toHaveBeenCalled()
  })
})
