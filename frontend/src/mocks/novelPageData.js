import { catalogNovels } from './catalogData'

export const novelPageData = [
  {
    id: '1',
    title: 'Легенда пепельного трона',
    coverUrl: 'https://tl.rulate.ru/i/book/26/3/29296-100100.jpg',
    coverStyle: 'from-lime-300 to-emerald-500',
    status: 'Онгоинг',
    releaseYear: 2021,
    description:
      'Наследник павшего дома возвращается в столицу, где каждый союз временный, а каждое слово может стоить жизни. Чтобы вернуть трон, ему придется объединить врагов, расколоть старые кланы и выбрать, что важнее: власть или люди, которые в него поверили.',
    genres: ['Фэнтези', 'Политика', 'Приключения'],
    tags: ['Королевство', 'Интриги', 'Магия', 'Стратегия'],
    translators: ['Команда RanobeDays', 'Ari Translation'],
    readingProgress: 43,
    chapters: [
      {
        id: 'c-1',
        number: 127,
        title: 'Ночь перед советом',
        publishedAt: '2026-04-10',
        isRead: true,
      },
      { id: 'c-2', number: 128, title: 'Цена обещаний', publishedAt: '2026-04-12', isRead: true },
      {
        id: 'c-3',
        number: 129,
        title: 'Клятва на пепле',
        publishedAt: '2026-04-14',
        isRead: false,
      },
      { id: 'c-4', number: 130, title: 'Ход королевы', publishedAt: '2026-04-16', isRead: false },
    ],
    comments: [
      {
        id: 'com-1',
        author: 'MikasaReader',
        text: 'Очень сильная глава, особенно диалог в финале.',
        timeAgo: '2 часа назад',
      },
      {
        id: 'com-2',
        author: 'Aster',
        text: 'Нравится, как автор раскрывает политику через личные конфликты.',
        timeAgo: 'вчера',
      },
    ],
  },
]

const defaultComments = [
  {
    id: 'com-template-1',
    author: 'RanobeReader',
    text: 'Хороший темп сюжета, жду новые главы!',
    timeAgo: 'сегодня',
  },
]

const buildNovelFromCatalog = (id) => {
  const source = catalogNovels.find((item) => String(item.id) === String(id))
  if (!source) return null

  const chaptersCount = Number(source.chapters || 0)
  const currentChapter = Math.max(chaptersCount - 2, 1)

  return {
    id: String(source.id),
    title: source.title,
    coverUrl: source.coverUrl || '',
    coverStyle: source.coverStyle || 'from-lime-300 to-emerald-500',
    status: source.status,
    releaseYear: source.releaseYear,
    description: source.synopsis,
    genres: source.genres || [],
    tags: source.tags || [],
    translators: ['Команда RanobeDays'],
    readingProgress: 0,
    chapters: [
      {
        id: `${source.id}-c1`,
        number: currentChapter,
        title: 'Последний релиз',
        publishedAt: '2026-04-12',
        isRead: false,
      },
      {
        id: `${source.id}-c2`,
        number: currentChapter + 1,
        title: 'Новая глава',
        publishedAt: '2026-04-14',
        isRead: false,
      },
    ],
    comments: defaultComments,
  }
}

export const getNovelById = (id) => {
  const fromNovelPageData = novelPageData.find((item) => String(item.id) === String(id))
  if (fromNovelPageData) return fromNovelPageData
  return buildNovelFromCatalog(id)
}
