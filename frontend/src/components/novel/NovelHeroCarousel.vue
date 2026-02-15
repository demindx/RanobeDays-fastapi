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
    default: 'Подборка для вас',
  },
})

const viewportRef = ref(null)
const trackRef = ref(null)
const isDragging = ref(false)
const hasDragged = ref(false)
const trackX = ref(0)
const blockWidth = ref(0)

const pointerStartX = ref(0)
const dragStartTrackX = ref(0)
const lastPointerX = ref(0)
const lastPointerTime = ref(0)
const velocity = ref(0)
const pointerHistory = ref([])
const activePointerId = ref(null)

const inertiaRaf = ref(null)
const snapRaf = ref(null)

const sourceNovels = computed(() => props.novels || [])
const loopedNovels = computed(() => [...sourceNovels.value, ...sourceNovels.value, ...sourceNovels.value])

const stopInertia = () => {
  if (inertiaRaf.value) {
    cancelAnimationFrame(inertiaRaf.value)
    inertiaRaf.value = null
  }
}

const stopSnap = () => {
  if (snapRaf.value) {
    cancelAnimationFrame(snapRaf.value)
    snapRaf.value = null
  }
}

const normalizeTrack = () => {
  if (blockWidth.value <= 0) return
  while (trackX.value > 0) {
    trackX.value -= blockWidth.value
  }
  while (trackX.value <= -2 * blockWidth.value) {
    trackX.value += blockWidth.value
  }
}

const getNearestStep = () => {
  if (!trackRef.value) return 176
  const firstSlide = trackRef.value.querySelector('.hero-carousel__slide')
  if (!firstSlide) return 176
  const slideWidth = firstSlide.getBoundingClientRect().width
  const styles = getComputedStyle(trackRef.value)
  const gap = Number.parseFloat(styles.columnGap || styles.gap || '0')
  return slideWidth + (Number.isNaN(gap) ? 0 : gap)
}

const snapToNearest = () => {
  if (blockWidth.value <= 0) return
  const step = getNearestStep()
  if (step <= 0) return

  const local = trackX.value + blockWidth.value
  const snappedLocal = Math.round(local / step) * step
  const target = snappedLocal - blockWidth.value

  const animate = () => {
    const diff = target - trackX.value
    trackX.value += diff * 0.18
    normalizeTrack()

    if (Math.abs(diff) < 0.5) {
      trackX.value = target
      normalizeTrack()
      snapRaf.value = null
      return
    }

    snapRaf.value = requestAnimationFrame(animate)
  }

  stopSnap()
  snapRaf.value = requestAnimationFrame(animate)
}

const runInertia = () => {
  if (Math.abs(velocity.value) < 0.01) {
    return
  }

  let previous = performance.now()
  const animate = (now) => {
    const delta = Math.min(32, now - previous)
    previous = now

    trackX.value += velocity.value * delta
    normalizeTrack()

    const friction = Math.pow(0.965, delta / 16.67)
    velocity.value *= friction

    if (Math.abs(velocity.value) < 0.02) {
      inertiaRaf.value = null
      return
    }

    inertiaRaf.value = requestAnimationFrame(animate)
  }

  stopInertia()
  inertiaRaf.value = requestAnimationFrame(animate)
}

const measure = () => {
  if (!trackRef.value || sourceNovels.value.length === 0) return
  const slides = trackRef.value.querySelectorAll('.hero-carousel__slide')
  const baseCount = sourceNovels.value.length
  if (slides.length <= baseCount) return

  const first = slides[0]
  const nextBlockStart = slides[baseCount]
  if (!first || !nextBlockStart) return

  blockWidth.value = nextBlockStart.offsetLeft - first.offsetLeft
  // Start from the middle block so infinite loop works in both directions.
  trackX.value = -blockWidth.value
}

const scrollByPage = (direction) => {
  if (!viewportRef.value) return
  stopInertia()
  stopSnap()
  velocity.value = 0
  trackX.value += direction * -viewportRef.value.clientWidth * 0.82
  normalizeTrack()
  snapToNearest()
}

const onPointerDown = (event) => {
  if (event.button !== 0 || !viewportRef.value) return
  event.preventDefault()

  stopInertia()
  stopSnap()

  isDragging.value = true
  hasDragged.value = false
  activePointerId.value = event.pointerId
  viewportRef.value.setPointerCapture(event.pointerId)

  pointerStartX.value = event.clientX
  dragStartTrackX.value = trackX.value
  lastPointerX.value = event.clientX
  lastPointerTime.value = performance.now()
  velocity.value = 0
  pointerHistory.value = [{ x: event.clientX, t: lastPointerTime.value }]
}

const onPointerMove = (event) => {
  if (!isDragging.value || activePointerId.value !== event.pointerId) return

  const totalDelta = event.clientX - pointerStartX.value
  if (Math.abs(totalDelta) > 3) {
    hasDragged.value = true
  }

  trackX.value = dragStartTrackX.value + totalDelta
  normalizeTrack()

  const now = performance.now()
  const deltaTime = Math.max(1, now - lastPointerTime.value)
  const deltaX = event.clientX - lastPointerX.value
  velocity.value = Math.max(-4.5, Math.min(4.5, deltaX / deltaTime))

  lastPointerX.value = event.clientX
  lastPointerTime.value = now
  pointerHistory.value.push({ x: event.clientX, t: now })
  if (pointerHistory.value.length > 8) {
    pointerHistory.value.shift()
  }
}

const onPointerUp = (event) => {
  if (!isDragging.value || activePointerId.value !== event.pointerId || !viewportRef.value) return

  isDragging.value = false
  viewportRef.value.releasePointerCapture(event.pointerId)
  activePointerId.value = null

  if (!hasDragged.value) return

  if (pointerHistory.value.length >= 2) {
    const first = pointerHistory.value[0]
    const last = pointerHistory.value[pointerHistory.value.length - 1]
    const dt = Math.max(1, last.t - first.t)
    const sampledVelocity = (last.x - first.x) / dt
    if (Math.abs(sampledVelocity) > Math.abs(velocity.value)) {
      velocity.value = sampledVelocity
    }
  }

  velocity.value *= 2.7
  velocity.value = Math.max(-6.5, Math.min(6.5, velocity.value))
  runInertia()
}

const onPointerCancel = () => {
  if (!isDragging.value) return
  isDragging.value = false
  activePointerId.value = null
  if (hasDragged.value) {
    runInertia()
  }
}

const onClickCapture = (event) => {
  if (!hasDragged.value) return
  event.preventDefault()
  event.stopPropagation()
  hasDragged.value = false
}

const initialize = async () => {
  await nextTick()
  measure()
}

watch(
  () => props.novels,
  () => {
    void initialize()
  },
  { deep: true },
)

onMounted(() => {
  void initialize()
  window.addEventListener('resize', measure)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', measure)
  stopInertia()
  stopSnap()
})
</script>

<template>
  <section
    class="hero-carousel"
    aria-label="Карусель новел"
  >
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-[1250px] w-full">
      <div class="hero-carousel__header">
        <h2 class="hero-carousel__title">
          {{ title }}
        </h2>
        <div class="hero-carousel__actions">
          <button
            type="button"
            class="hero-carousel__nav"
            aria-label="Прокрутить влево"
            @click="scrollByPage(-1)"
          >
            ‹
          </button>
          <button
            type="button"
            class="hero-carousel__nav"
            aria-label="Прокрутить вправо"
            @click="scrollByPage(1)"
          >
            ›
          </button>
        </div>
      </div>
    </div>

    <div
      ref="viewportRef"
      class="hero-carousel__viewport"
      :class="{ 'hero-carousel__viewport--dragging': isDragging }"
      @pointerdown="onPointerDown"
      @pointermove="onPointerMove"
      @pointerup="onPointerUp"
      @pointercancel="onPointerCancel"
      @click.capture="onClickCapture"
    >
      <div
        ref="trackRef"
        class="hero-carousel__track"
        :style="{ transform: `translate3d(${trackX}px, 0, 0)` }"
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

.hero-carousel__viewport {
  overflow: hidden;
  cursor: grab;
  user-select: none;
  padding: 0.25rem 1rem;
}

.hero-carousel__viewport--dragging {
  cursor: grabbing;
}

.hero-carousel__track {
  display: flex;
  align-items: stretch;
  gap: 0.6rem;
  will-change: transform;
}

.hero-carousel__slide {
  flex: 0 0 auto;
}

.hero-carousel__viewport :deep(img) {
  -webkit-user-drag: none;
  user-drag: none;
  pointer-events: none;
}

@media (max-width: 767px) {
  .hero-carousel {
    padding-top: 0.9rem;
  }
}
</style>
