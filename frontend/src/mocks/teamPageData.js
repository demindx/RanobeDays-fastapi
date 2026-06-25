import { catalogNovels } from './catalogData'

export const teamPageData = {
  id: 'team-1',
  name: 'Клан Феникса',
  slug: 'klan-feniksa',
  avatarColorClass: 'bg-orange-500',
  type: 'translators',
  typeLabel: 'Переводчики',
  shortDescription: 'Переводы китайской и корейской литературы',
  description:
    'Крупнейшее русскоязычное сообщество переводчиков, специализирующееся на китайской и корейской литературе. Основана в 2024 году, объединяет более 10 талантливых переводчиков и редакторов. Переводим более 5 новелл одновременно, следим за качеством перевода и регулярностью релизов.\n\nНаша миссия — сделать азиатскую литературу доступной для русскоязычных читателей в самом высоком качестве. Каждая глава проходит вычитку, редактуру и проверку терминологии.',
  createdAt: '2024-09-01',
  stats: {
    membersCount: 6,
    novelsCount: 5,
    chaptersTotal: 847,
  },
}

export const teamMembers = [
  { id: 'user-1', nickname: 'MikasaReader', role: 'creator', avatarColorClass: 'bg-lime-500' },
  { id: 'user-2', nickname: 'ShadowSage', role: 'manager', avatarColorClass: 'bg-blue-500' },
  { id: 'user-3', nickname: 'NovelWhisperer', role: 'manager', avatarColorClass: 'bg-violet-500' },
  { id: 'user-4', nickname: 'Aster', role: 'translator', avatarColorClass: 'bg-emerald-500' },
  { id: 'user-5', nickname: 'PageTurner', role: 'translator', avatarColorClass: 'bg-amber-500' },
  { id: 'user-6', nickname: 'LoreKeeper', role: 'translator', avatarColorClass: 'bg-rose-500' },
]

const teamNovelIds = [1, 3, 4, 5, 6]

export const teamNovels = teamNovelIds
  .map((id) => catalogNovels.find((n) => n.id === id))
  .filter(Boolean)
