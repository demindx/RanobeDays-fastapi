const STATUS_LABELS = {
  frozen: 'Заморожено',
  continues: 'Онгоинг',
  completed: 'Завершено',
  abadoned: 'Заброшено',
}

function toCoverUrl(item) {
  const raw = item.cover_path || item.coverUrl || ''
  if (typeof raw === 'string' && /^https?:\/\//i.test(raw)) return raw
  return ''
}

function toReleaseYear(value) {
  if (!value) return null
  const year = new Date(value).getFullYear()
  return Number.isFinite(year) ? year : null
}

export function mapNovel(item) {
  if (!item) return null

  const id = item.id ?? item.slug ?? item.title ?? ''

  const coverUrl = toCoverUrl(item)

  return {
    id,
    title: item.title || 'Без названия',
    slug: item.slug || '',
    synopsis: item.description || '',
    description: item.description || '',
    type: item.type || 'original',
    status: STATUS_LABELS[item.status] || item.status || '',
    releaseYear: toReleaseYear(item.publish_date),
    publish_date: item.publish_date || null,
    ageRating: item.age_limit != null ? `${item.age_limit}+` : '16+',
    rating: item.rating ?? null,
    genres:
      item.categories?.filter((c) => c.type === 'genre').map((c) => c.name) || item.genres || [],
    tags: item.categories?.filter((c) => c.type === 'tag').map((c) => c.name) || item.tags || [],
    originalLanguage: item.language?.name || item.originalLanguage || '',
    translationLanguage: item.country?.name || item.translationLanguage || '',
    coverStyle: coverUrl ? '' : item.coverStyle || 'from-lime-300 to-emerald-500',
    coverUrl,
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
  const rawParagraphs = Array.isArray(item.content)
    ? item.content
    : String(item.content || '').split(/\n\n+/)
  const paragraphs = rawParagraphs.map((p) => p.trim()).filter(Boolean)
  return {
    ...item,
    id: item.id ?? `ch-${item.number || 0}`,
    publishedAt: item.created_at || item.published_at || null,
    isRead: !!item.is_read,
    content: paragraphs,
  }
}

export function mapChaptersList(items) {
  if (!Array.isArray(items)) return []
  return items.map(mapChapter)
}

export function mapTeamMember(item) {
  if (!item) return null
  const user = item.user || {}
  const nickname = user.user_profile?.nickname || item.nickname || user.login || ''
  const email = user.email || item.email || ''

  return {
    id: user.id ?? item.user_id ?? (email || nickname),
    nickname,
    email,
    role: item.role || '',
    avatarColorClass: 'bg-lime-500',
  }
}
