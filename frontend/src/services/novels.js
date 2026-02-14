import { novels } from '@/mocks/novels'

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export const fetchCatalogNovels = async (query = '') => {
  await sleep(180)

  const normalized = String(query || '').trim().toLowerCase()
  if (!normalized) {
    return novels
  }

  return novels.filter((novel) => {
    return (
      novel.title.toLowerCase().includes(normalized) ||
      novel.country.toLowerCase().includes(normalized)
    )
  })
}
