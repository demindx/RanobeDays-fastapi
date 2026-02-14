<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import NovelCardComponent from '@/components/novel/NovelCardComponent.vue'

const props = defineProps({
  novels: {
    type: Array,
    default: () => [],
  },
  title: {
    type: String,
    default: 'Популярное сейчас',
  },
})

const trackRef = ref(null)
const isDragging = ref(false)
const hasDragged = ref(false)
const dragStartX = ref(0)
const dragStartScrollLeft = ref(0)
const dragLastX = ref(0)
const dragLastTime = ref(0)
const dragVelocity = ref(0)
const momentumFrame = ref(null)
const blockWidth = ref(0)
const singleList = computed(() => props.novels || [])
const loopedNovels = computed(() => [...singleList.value, ...singleList.value, ...singleList.value])

const syncBlockWidth = () => {
  if (!trackRef.value) return
  blockWidth.value = trackRef.value.scrollWidth / 3
}

const centerTrack = () => {
  if (!trackRef.value) return
  trackRef.value.scrollLeft = blockWidth.value
}

const handleInfiniteLoop = () => {
  if (!trackRef.value || blockWidth.value === 0) return

  if (trackRef.value.scrollLeft <= 0) {
    trackRef.value.scrollLeft += blockWidth.value
  } else if (trackRef.value.scrollLeft >= blockWidth.value * 2) {
    trackRef.value.scrollLeft -= blockWidth.value
  }
}

const scrollTrack = (direction) => {
  if (!trackRef.value || blockWidth.value === 0) return

  const scrollAmount = Math.round(trackRef.value.clientWidth * 0.82)
  trackRef.value.scrollBy({
    left: direction * scrollAmount,
    behavior: 'smooth',
  })
}

const stopMomentum = () => {
  if (momentumFrame.value) {
    cancelAnimationFrame(momentumFrame.value)
    momentumFrame.value = null
  }
}

const runMomentum = () => {
  if (!trackRef.value) return

  const step = () => {
    if (!trackRef.value) {
      momentumFrame.value = null
      return
    }

    dragVelocity.value *= 0.94
    trackRef.value.scrollLeft -= dragVelocity.value * 16
    handleInfiniteLoop()

    if (Math.abs(dragVelocity.value) < 0.02) {
      momentumFrame.value = null
      return
    }

    momentumFrame.value = requestAnimationFrame(step)
  }

  stopMomentum()
  momentumFrame.value = requestAnimationFrame(step)
}

const onMouseDown = (event) => {
  if (!trackRef.value || event.button !== 0) return
  event.preventDefault()
  stopMomentum()

  isDragging.value = true
  hasDragged.value = false
  dragStartX.value = event.clientX
  dragStartScrollLeft.value = trackRef.value.scrollLeft
  dragLastX.value = event.clientX
  dragLastTime.value = performance.now()
  dragVelocity.value = 0
}

const onMouseMove = (event) => {
  if (!isDragging.value || !trackRef.value) return

  const deltaFromStart = event.clientX - dragStartX.value
  if (Math.abs(deltaFromStart) > 3) {
    hasDragged.value = true
  }

  trackRef.value.scrollLeft = dragStartScrollLeft.value - deltaFromStart
  handleInfiniteLoop()

  const deltaX = event.clientX - dragLastX.value
  const now = performance.now()
  const deltaTime = Math.max(1, now - dragLastTime.value)
  dragVelocity.value = deltaX / deltaTime

  dragLastX.value = event.clientX
  dragLastTime.value = now
}

const onMouseUp = () => {
  if (!isDragging.value) return
  isDragging.value = false
  if (hasDragged.value) {
    runMomentum()
  }
}

const onTrackClickCapture = (event) => {
  if (!hasDragged.value) return
  event.preventDefault()
  event.stopPropagation()
  hasDragged.value = false
}

const initTrack = async () => {
  await nextTick()
  syncBlockWidth()
  centerTrack()
}

watch(
  () => props.novels,
  () => {
    void initTrack()
  },
  { deep: true },
)

onMounted(() => {
  void initTrack()
  window.addEventListener('mousemove', onMouseMove, { passive: true })
  window.addEventListener('mouseup', onMouseUp)
  window.addEventListener('resize', syncBlockWidth)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseup', onMouseUp)
  window.removeEventListener('resize', syncBlockWidth)
  stopMomentum()
})
</script>

<template>
  <section
    class="hero-carousel"
    aria-label="Карусель новел"
  >
    <div class="hero-carousel__header">
      <h2 class="hero-carousel__title">
        {{ title }}
      </h2>
      <div class="hero-carousel__actions">
        <button
          type="button"
          class="hero-carousel__nav"
          aria-label="Прокрутить влево"
          @click="scrollTrack(-1)"
        >
          ‹
        </button>
        <button
          type="button"
          class="hero-carousel__nav"
          aria-label="Прокрутить вправо"
          @click="scrollTrack(1)"
        >
          ›
        </button>
      </div>
    </div>

    <div
      ref="trackRef"
      class="hero-carousel__track"
      :class="{ 'hero-carousel__track--dragging': isDragging }"
      @mousedown="onMouseDown"
      @click.capture="onTrackClickCapture"
      @dragstart.prevent
      @scroll="handleInfiniteLoop"
    >
      <div
        v-for="(novel, index) in loopedNovels"
        :key="`${novel.slug}-${index}`"
        class="hero-carousel__slide"
      >
        <NovelCardComponent
          :title="novel.title"
          :country="novel.country"
          :image-src="novel.imageSrc"
          :slug="novel.slug"
          :bookmark-status="novel.bookmarkStatus"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-carousel {
  width: 100%;
  padding: 1.25rem 0 1.75rem;
}

.hero-carousel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem 0.5rem;
}

.hero-carousel__title {
  color: var(--foreground-third-color);
  font-size: 1.1rem;
  font-weight: 700;
}

.hero-carousel__actions {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.hero-carousel__nav {
  width: 2rem;
  height: 2rem;
  border-radius: 999px;
  border: 1px solid var(--border-soft-color);
  background: color-mix(in srgb, var(--third-color) 84%, transparent);
  color: var(--foreground-third-color);
  font-size: 1.1rem;
  line-height: 1;
  cursor: pointer;
}

.hero-carousel__track {
  display: flex;
  align-items: stretch;
  gap: 0.6rem;
  overflow-x: auto;
  scroll-snap-type: x proximity;
  scroll-padding: 1rem;
  padding: 0.25rem 1rem 0.25rem;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  cursor: grab;
  user-select: none;
}

.hero-carousel__track::-webkit-scrollbar {
  display: none;
}

.hero-carousel__track--dragging {
  cursor: grabbing;
  scroll-snap-type: none;
}

.hero-carousel__track :deep(img) {
  -webkit-user-drag: none;
  user-drag: none;
}

.hero-carousel__slide {
  flex: 0 0 auto;
  scroll-snap-align: start;
}

@media (max-width: 767px) {
  .hero-carousel {
    padding-top: 0.9rem;
  }
}
</style>
