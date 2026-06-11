<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useChapter } from '../composables/useChapter'
import { useChapterSettings } from '../composables/useChapterSettings'
import ChapterContent from '../components/chapter/ChapterContent.vue'
import ChapterSettingsPanel from '../components/chapter/ChapterSettingsPanel.vue'
import SettingsIcon from '../components/icons/SettingsIcon.vue'
import AppSelect from '../components/shared/AppSelect.vue'

const router = useRouter()
const {
  novelId,
  chapterId,
  chapter,
  chapterOptions,
  hasPrev,
  hasNext,
  prevChapterId,
  nextChapterId,
} = useChapter()
const { settings, currentBg, currentFont } = useChapterSettings()

const isSettingsOpen = ref(false)
const showToolbar = ref(true)
const readProgress = ref(0)
let hideTimer = null

const textColor = computed(() => currentBg()?.text || '#e4e4e7')
const bgColor = computed(() => currentBg()?.bg || '#0f0f11')

const showToolbarWithTimer = () => {
  showToolbar.value = true
  clearTimeout(hideTimer)
  hideTimer = setTimeout(() => {
    showToolbar.value = false
  }, 3000)
}

const goToChapter = (id) => {
  router.push(`/novel/${novelId.value}/chapter/${id}`)
}

const goPrev = () => {
  if (hasPrev.value) router.push(`/novel/${novelId.value}/chapter/${prevChapterId.value}`)
}

const goNext = () => {
  if (hasNext.value) router.push(`/novel/${novelId.value}/chapter/${nextChapterId.value}`)
}

const handleKeydown = (e) => {
  if (e.key === 'ArrowLeft') goPrev()
  if (e.key === 'ArrowRight') goNext()
}

const handleScroll = () => {
  const scrollY = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  readProgress.value = docHeight > 0 ? Math.min((scrollY / docHeight) * 100, 100) : 0
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
  window.addEventListener('scroll', handleScroll, { passive: true })
  showToolbarWithTimer()
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('scroll', handleScroll)
  clearTimeout(hideTimer)
})
</script>

<template>
  <div
    class="relative flex min-h-screen flex-col transition-colors duration-300"
    :style="{ backgroundColor: bgColor }"
    @mousemove="showToolbarWithTimer"
    @click="showToolbarWithTimer"
  >
    <div
      :class="[
        'fixed inset-x-0 top-0 z-30 transition-all duration-300',
        showToolbar || isSettingsOpen ? 'translate-y-0 opacity-100' : '-translate-y-full opacity-0',
      ]"
    >
      <div
        class="border-b px-3 py-2"
        :style="{
          backgroundColor: bgColor,
          borderColor: 'rgba(128,128,128,0.15)',
        }"
      >
        <div class="mx-auto flex w-full max-w-3xl items-center justify-between">
          <button
            type="button"
            class="flex h-8 w-8 shrink-0 cursor-pointer items-center justify-center rounded-lg transition hover:bg-white/10"
            :style="{ color: textColor }"
            @click="router.push(`/novel/${novelId}`)"
          >
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none">
              <path
                d="M19 12H5M12 19l-7-7 7-7"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>

          <div class="flex items-center gap-3">
            <button
              type="button"
              :disabled="!hasPrev"
              :class="[
                'flex h-8 w-8 shrink-0 items-center justify-center rounded-lg transition',
                hasPrev ? 'cursor-pointer hover:bg-white/10' : 'cursor-default opacity-30',
              ]"
              :style="{ color: textColor }"
              @click="goPrev"
            >
              <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none">
                <path
                  d="M15 18L9 12L15 6"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>

            <div class="w-40 sm:w-52">
              <AppSelect
                :model-value="chapterId"
                :options="chapterOptions"
                variant="neutral"
                placeholder="Глава"
                @update:model-value="goToChapter"
              />
            </div>

            <button
              type="button"
              :disabled="!hasNext"
              :class="[
                'flex h-8 w-8 shrink-0 items-center justify-center rounded-lg transition',
                hasNext ? 'cursor-pointer hover:bg-white/10' : 'cursor-default opacity-30',
              ]"
              :style="{ color: textColor }"
              @click="goNext"
            >
              <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none">
                <path
                  d="M9 18L15 12L9 6"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>

          <button
            type="button"
            class="flex h-8 w-8 shrink-0 cursor-pointer items-center justify-center rounded-lg transition hover:bg-white/10"
            :style="{ color: textColor }"
            @click="isSettingsOpen = true"
          >
            <SettingsIcon class="h-4 w-4" />
          </button>
        </div>
      </div>

      <div class="h-[1px]" :style="{ backgroundColor: textColor, opacity: 0.15 }">
        <div
          class="h-full transition-all duration-300"
          :style="{
            width: readProgress + '%',
            backgroundColor: textColor,
            opacity: 0.4,
          }"
        />
      </div>
    </div>

    <div
      class="fixed inset-y-0 left-0 z-10 flex w-12 items-center justify-center transition-opacity duration-300"
      :class="hasPrev ? 'cursor-pointer' : 'pointer-events-none opacity-0'"
      @click="goPrev"
    />

    <div
      class="fixed inset-y-0 right-0 z-10 flex w-12 items-center justify-center transition-opacity duration-300"
      :class="hasNext ? 'cursor-pointer' : 'pointer-events-none opacity-0'"
      @click="goNext"
    />

    <div class="flex-1 pt-12">
      <ChapterContent />
    </div>

    <div class="pb-12 text-center">
      <p v-if="chapter" class="pb-4 text-xs" :style="{ color: textColor, opacity: 0.2 }">
        Глава {{ chapter.number }}
      </p>
    </div>

    <ChapterSettingsPanel :open="isSettingsOpen" @close="isSettingsOpen = false" />
  </div>
</template>
