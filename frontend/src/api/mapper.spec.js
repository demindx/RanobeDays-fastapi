import { describe, it, expect } from 'vitest'
import { mapNovel, mapNovelsList, mapChapter, mapChaptersList } from './mapper'

describe('mapNovel', () => {
  it('maps backend fields to frontend shape', () => {
    const input = {
      id: 1,
      title: 'Test',
      slug: 'test',
      description: 'Desc',
      type: 'original',
      status: 'continues',
      publish_date: '2021-06-15T00:00:00Z',
      age_limit: 16,
      cover_path: 'default_cover.png',
      language: { name: 'Китайский' },
      country: { name: 'Русский' },
      categories: [
        { name: 'Фэнтези', type: 'genre' },
        { name: 'Магия', type: 'tag' },
      ],
    }

    const result = mapNovel(input)

    expect(result.id).toBe(1)
    expect(result.title).toBe('Test')
    expect(result.status).toBe('Онгоинг')
    expect(result.ageRating).toBe('16+')
    expect(result.releaseYear).toBe(2021)
    expect(result.genres).toEqual(['Фэнтези'])
    expect(result.tags).toEqual(['Магия'])
    expect(result.originalLanguage).toBe('Китайский')
    expect(result.translationLanguage).toBe('Русский')
    expect(result.coverUrl).toBe('')
  })

  it('keeps http cover url and clears gradient', () => {
    const result = mapNovel({ id: 1, cover_path: 'https://example.com/a.jpg' })
    expect(result.coverUrl).toBe('https://example.com/a.jpg')
    expect(result.coverStyle).toBe('')
  })

  it('returns null for null input', () => {
    expect(mapNovel(null)).toBeNull()
  })
})

describe('mapChapter', () => {
  it('splits content into paragraphs and maps dates', () => {
    const input = {
      id: 1,
      number: 5,
      title: 'Title',
      content: 'a\n\nb\n\nc',
      created_at: '2026-01-01T00:00:00Z',
    }

    const result = mapChapter(input)

    expect(result.content).toEqual(['a', 'b', 'c'])
    expect(result.publishedAt).toBe('2026-01-01T00:00:00Z')
    expect(result.isRead).toBe(false)
  })
})

describe('list mappers', () => {
  it('tolerate non-array input', () => {
    expect(mapNovelsList(null)).toEqual([])
    expect(mapChaptersList(undefined)).toEqual([])
  })

  it('map arrays', () => {
    expect(mapNovelsList([{ id: 1 }])).toHaveLength(1)
    expect(mapChaptersList([{ id: 1, content: 'x' }])).toHaveLength(1)
  })
})
