import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ref } from 'vue'

const mockUseRouter = vi.fn()
const mockUseRoute = vi.fn()

vi.mock('vue-router', () => ({
  useRouter: () => mockUseRouter(),
  useRoute: () => mockUseRoute(),
}))

describe('useSearch', () => {
  beforeEach(() => {
    mockUseRouter.mockReset()
    mockUseRoute.mockReset()
  })

  it('navigates to catalog with trimmed query', async () => {
    const push = vi.fn().mockResolvedValue(undefined)
    const router = {
      currentRoute: ref({ path: '/', query: {} }),
      push,
    }
    mockUseRoute.mockReturnValue({ query: {} })
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
    mockUseRoute.mockReturnValue({ query: { q: 'old' } })
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
    mockUseRoute.mockReturnValue({ query: { q: 'rezero' } })
    mockUseRouter.mockReturnValue(router)

    const { useSearch } = await import('./useSearch')
    const { search } = useSearch()

    await search('rezero')

    expect(push).not.toHaveBeenCalled()
  })
})
