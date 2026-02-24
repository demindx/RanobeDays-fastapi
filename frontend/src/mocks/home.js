import { novels } from '@/mocks/novels'

const chapterNumber = (index, base) => `Глава ${base + index}`

export const continueReadingItems = novels.slice(0, 4).map((novel, index) => ({
  slug: novel.slug,
  title: novel.title,
  imageSrc: novel.imageSrc,
  lastReadChapter: chapterNumber(index, 37),
  progress: Math.min(95, 28 + index * 17),
}))

export const popularTodayItems = novels.slice(0, 10).map((novel, index) => ({
  slug: novel.slug,
  title: novel.title,
  imageSrc: novel.imageSrc,
  country: novel.country,
  bookmarkStatus: novel.bookmarkStatus || (index % 2 === 0 ? 'Читаю' : 'Буду читать'),
}))

export const newChaptersTodayItems = novels.slice(2, 12).map((novel, index) => ({
  slug: novel.slug,
  title: novel.title,
  imageSrc: novel.imageSrc,
  country: novel.country,
  bookmarkStatus: novel.bookmarkStatus,
  chapter: chapterNumber(index, 112),
  releasedAt: `${(index % 5) + 1} ч назад`,
  isNew: index < 5,
}))

export const latestUpdatesItems = novels.slice(0, 12).map((novel, index) => ({
  id: `${novel.slug}-${index}`,
  slug: novel.slug,
  title: novel.title,
  chapter: chapterNumber(index, 154),
  updatedAt: `${(index % 9) + 3} мин назад`,
  bookmarkStatus: novel.bookmarkStatus,
}))
