import { catalogNovels } from '../mocks/catalogData'

export function mapBookmarkItem(item) {
  const catalogId = item.novelId ?? item.id
  const novel = catalogNovels.find((n) => n.id === catalogId)
  const chapterNum = parseInt(String(item.chapterLabel || '').replace(/\D/g, ''), 10) || 0

  return {
    id: catalogId,
    title: item.title,
    author: item.author,
    rating: item.rating,
    coverStyle: item.coverStyle,
    coverUrl: item.coverUrl,
    href: item.href || (catalogId ? `/novel/${catalogId}` : '#'),
    chapters: chapterNum,
    releaseYear: novel?.releaseYear ?? '',
    ageRating: novel?.ageRating ?? '',
    status: novel?.status ?? '',
    synopsis: novel?.synopsis ?? '',
    genres: novel?.genres ?? [],
    tags: novel?.tags ?? [],
    originalLanguage: novel?.originalLanguage ?? '',
    translationLanguage: novel?.translationLanguage ?? '',
  }
}
