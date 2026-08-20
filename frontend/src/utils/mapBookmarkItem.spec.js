import { describe, it, expect } from 'vitest'
import { mapBookmarkItem } from './mapBookmarkItem'

describe('mapBookmarkItem', () => {
  it('maps an item by novelId and parses chapter number', () => {
    const item = {
      novelId: 1,
      title: 'Легенда пепельного трона',
      author: 'Куанг Ли',
      chapterLabel: 'Глава 129',
      rating: 4.8,
      coverStyle: 'from-lime-300 to-emerald-500',
    }

    const result = mapBookmarkItem(item)

    expect(result.id).toBe(1)
    expect(result.title).toBe('Легенда пепельного трона')
    expect(result.chapters).toBe(129)
    expect(result.href).toBe('/novel/1')
    expect(result.releaseYear).toBe(2021)
  })

  it('falls back to item.id when novelId is absent', () => {
    const result = mapBookmarkItem({ id: 3, title: 'Y', chapterLabel: 'Глава 3' })

    expect(result.id).toBe(3)
    expect(result.href).toBe('/novel/3')
    expect(result.chapters).toBe(3)
  })
})
