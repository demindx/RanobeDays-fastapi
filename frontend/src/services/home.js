import {
  continueReadingItems,
  latestUpdatesItems,
  newChaptersTodayItems,
  popularTodayItems,
} from '@/mocks/home'

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export const fetchHomeContinueReading = async (isLoggedIn) => {
  await sleep(160)
  if (!isLoggedIn) return []
  return continueReadingItems
}

export const fetchHomeNewChaptersToday = async () => {
  await sleep(180)
  return newChaptersTodayItems
}

export const fetchHomePopularToday = async () => {
  await sleep(170)
  return popularTodayItems
}

export const fetchHomeLatestUpdates = async () => {
  await sleep(190)
  return latestUpdatesItems
}
