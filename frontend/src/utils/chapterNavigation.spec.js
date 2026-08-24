import { describe, expect, it } from 'vitest'
import { getChapterNavigation } from './chapterNavigation'

const chapters = [
  { id: 30, number: 3 },
  { id: 10, number: 1 },
  { id: 20, number: 2 },
]

describe('getChapterNavigation', () => {
  it('sorts chapters by number and returns adjacent ids', () => {
    expect(getChapterNavigation(chapters, 20)).toEqual({
      chapters: [
        { id: 10, number: 1 },
        { id: 20, number: 2 },
        { id: 30, number: 3 },
      ],
      currentIndex: 1,
      prevChapterId: 10,
      nextChapterId: 30,
    })
  })

  it('does not offer navigation when the current chapter is absent', () => {
    expect(getChapterNavigation(chapters, 999)).toMatchObject({
      currentIndex: -1,
      prevChapterId: null,
      nextChapterId: null,
    })
  })
})
