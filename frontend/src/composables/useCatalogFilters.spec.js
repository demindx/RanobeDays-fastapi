import { describe, expect, it } from 'vitest'
import { matchesCatalogYearRange, mergeCatalogFilterQuery } from './useCatalogFilters'

describe('catalog filter URL contract', () => {
  it('preserves unrelated query parameters and replaces managed filters', () => {
    expect(
      mergeCatalogFilterQuery(
        { search: 'magic', genres: 'Old', tagsExclude: 'Old', page: '2' },
        { genres: 'Fantasy' },
      ),
    ).toEqual({ search: 'magic', page: '2', genres: 'Fantasy' })
  })
})

describe('catalog year range', () => {
  it('does not match a novel with an unknown year when a range is active', () => {
    expect(matchesCatalogYearRange(null, { from: '', to: '2020' })).toBe(false)
  })

  it('allows an unknown year when no range is active', () => {
    expect(matchesCatalogYearRange(null, { from: '', to: '' })).toBe(true)
  })
})
