export const profileUser = {
  joinDate: '2024-09-15',
  stats: {
    chaptersRead: 1847,
    novelsCompleted: 12,
    readingHours: 347,
    streakDays: 23,
    bookmarksCount: 5,
    commentsCount: 34,
  },
  teams: [
    { id: 'team-1', name: 'Клан Феникса', avatarColorClass: 'bg-orange-500' },
    { id: 'team-2', name: 'Переводчики', avatarColorClass: 'bg-violet-500' },
    { id: 'team-3', name: 'Ночные чтецы', avatarColorClass: 'bg-blue-500' },
    { id: 'team-4', name: 'Библиотека', avatarColorClass: 'bg-rose-500' },
  ],
}

function generateCalendarData() {
  const data = []
  const now = new Date()
  for (let i = 119; i >= 0; i--) {
    const date = new Date(now)
    date.setDate(date.getDate() - i)
    const dateStr = date.toISOString().slice(0, 10)
    const dayOfWeek = date.getDay()
    const activity = Math.max(
      0,
      Math.round(
        (3 +
          Math.sin(i * 0.3) * 2 +
          Math.cos(i * 0.1) * 1.5 +
          (dayOfWeek > 0 && dayOfWeek < 6 ? 1 : -0.5)) *
          Math.random() *
          5,
      ),
    )
    data.push({ date: dateStr, count: activity })
  }
  return data
}

export const calendarData = generateCalendarData()

export const userBookmarks = [
  {
    id: 'b-1',
    name: 'Читаю',
    novelCount: 4,
    isPublic: true,
    novels: [
      {
        id: 1,
        title: 'Легенда пепельного трона',
        author: 'Куанг Ли',
        coverStyle: 'from-lime-300 to-emerald-500',
        chapterLabel: 'Глава 129',
        rating: 4.8,
      },
      {
        id: 4,
        title: 'Путь ледяного феникса',
        author: 'Мин Сон',
        coverStyle: 'from-indigo-300 to-violet-600',
        chapterLabel: 'Глава 215',
        rating: 4.9,
      },
      {
        id: 9,
        title: 'Я Сам Решаю Судьбу',
        author: 'Ло Вэй',
        coverStyle: 'from-lime-300 to-green-500',
        coverUrl: 'https://tl.rulate.ru/i/book/26/3/29296-100100.jpg',
        chapterLabel: 'Глава 21',
        rating: 4.7,
      },
      {
        id: 6,
        title: 'Песнь лунного клинка',
        author: 'Ло Юн',
        coverStyle: 'from-sky-300 to-indigo-500',
        chapterLabel: 'Глава 92',
        rating: 4.7,
      },
    ],
  },
  {
    id: 'b-2',
    name: 'В планах',
    novelCount: 8,
    isPublic: false,
    novels: [
      {
        id: 3,
        title: 'Алхимик без имени',
        author: 'Андрес Рой',
        coverStyle: 'from-amber-300 to-orange-500',
        chapterLabel: 'Глава 410',
        rating: 4.6,
      },
      {
        id: 5,
        title: 'Тень архивариуса',
        author: 'Рин Араи',
        coverStyle: 'from-rose-300 to-pink-600',
        chapterLabel: 'Глава 34',
        rating: 4.5,
      },
      {
        id: 7,
        title: 'Наследник бездны',
        author: 'Сара Морн',
        coverStyle: 'from-fuchsia-400 to-purple-700',
        chapterLabel: 'Глава 56',
        rating: 4.4,
      },
    ],
  },
  {
    id: 'b-3',
    name: 'Прочитано',
    novelCount: 12,
    isPublic: true,
    novels: [
      {
        id: 10,
        title: 'Император Пути Пилюль и Боевых Искусств',
        author: 'Цинь Жун',
        coverStyle: 'from-amber-300 to-orange-600',
        coverUrl: 'https://tl.rulate.ru/i/book/26/4/22438-100100.jpg',
        chapterLabel: 'Завершено',
        rating: 4.6,
      },
      {
        id: 11,
        title: 'Грибной господин',
        author: 'Мо Цзюнь',
        coverStyle: 'from-green-300 to-emerald-600',
        coverUrl: 'https://tl.rulate.ru/i/book/26/4/24333-100100.jpg',
        chapterLabel: 'Завершено',
        rating: 4.5,
      },
    ],
  },
]

export const userComments = [
  {
    id: 'c-1',
    novelId: 1,
    novelTitle: 'Легенда пепельного трона',
    text: 'Одна из лучших новелл в жанре политического фэнтези. Персонажи прописаны глубоко, интриги держат в напряжении до последней главы.',
    date: '2026-06-10',
    likes: 12,
  },
  {
    id: 'c-2',
    novelId: 4,
    novelTitle: 'Путь ледяного феникса',
    text: 'Сильная героиня, отличная динамика боёв. Немного затянута арка кланов, но в целом очень достойно.',
    date: '2026-06-07',
    likes: 8,
  },
  {
    id: 'c-3',
    novelId: 9,
    novelTitle: 'Я Сам Решаю Судьбу',
    text: 'Концепция с системой выбора сделана интересно. Жду продолжения!',
    date: '2026-06-03',
    likes: 5,
  },
  {
    id: 'c-4',
    novelId: 6,
    novelTitle: 'Песнь лунного клинка',
    text: 'Боевые сцены на высшем уровне. Перевод качественный, читается на одном дыхании.',
    date: '2026-05-28',
    likes: 15,
  },
  {
    id: 'c-5',
    novelId: 12,
    novelTitle: 'Марвел: Начиная со способности копировать таланты сверхлюдей',
    text: 'Неожиданно хороший фанфик по Marvel. Автор явно знает вселенную.',
    date: '2026-05-20',
    likes: 3,
  },
]
