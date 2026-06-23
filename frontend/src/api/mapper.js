export function mapNovel(item) {
  if (!item) return null

  const id = item.id || (item.slug ? item.slug : Math.random().toString(36).slice(2, 10))

  return {
    id,
    title: item.title || 'Без названия',
    slug: item.slug || '',
    synopsis: item.description || '',
    description: item.description || '',
    type: item.type || 'original',
    status: item.status || '',
    releaseYear: item.publish_date ? new Date(item.publish_date).getFullYear() : null,
    publish_date: item.publish_date || null,
    ageRating: item.age_limit ? `${item.age_limit}+` : '16+',
    rating: item.rating || null,
    genres:
      item.categories?.filter((c) => c.type === 'genre').map((c) => c.name) || item.genres || [],
    tags: item.categories?.filter((c) => c.type === 'tag').map((c) => c.name) || item.tags || [],
    originalLanguage: item.language?.name || item.originalLanguage || '',
    translationLanguage: item.country?.name || item.translationLanguage || '',
    coverStyle: item.cover_path ? '' : 'from-lime-300 to-emerald-500',
    coverUrl: item.cover_path || item.coverUrl || '',
    chapters: item.chapters || [],
    comments: item.comments || [],
    language: item.language || null,
    country: item.country || null,
    readingProgress: item.reading_progress || 0,
    translators: item.team?.name ? [item.team.name] : [],
  }
}

export function mapNovelsList(items) {
  if (!Array.isArray(items)) return []
  return items.map(mapNovel)
}

export function mapChapter(item) {
  if (!item) return null
  return {
    ...item,
    id: item.id || `ch-${item.number || 0}`,
  }
}

export function mapChaptersList(items) {
  if (!Array.isArray(items)) return []
  return items.map(mapChapter)
}
