const compareChapters = (left, right) => {
  const numberDifference = Number(left.number) - Number(right.number)
  if (Number.isFinite(numberDifference) && numberDifference !== 0) return numberDifference
  return String(left.id).localeCompare(String(right.id))
}

export function getChapterNavigation(chapters, chapterId) {
  const orderedChapters = Array.isArray(chapters) ? [...chapters].sort(compareChapters) : []
  const currentIndex = orderedChapters.findIndex(
    (chapter) => String(chapter.id) === String(chapterId),
  )

  return {
    chapters: orderedChapters,
    currentIndex,
    prevChapterId: currentIndex > 0 ? orderedChapters[currentIndex - 1].id : null,
    nextChapterId:
      currentIndex >= 0 && currentIndex < orderedChapters.length - 1
        ? orderedChapters[currentIndex + 1].id
        : null,
  }
}
