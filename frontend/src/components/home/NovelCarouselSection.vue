<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useDragScroll } from '../../composables/useDragScroll'
import SectionTitle from '../ui/SectionTitle.vue'
import NovelCard from '../cards/NovelCard.vue'
import AppEmptyState from '../shared/AppEmptyState.vue'

const props = defineProps({
  novels: {
    type: Array,
    default: () => [],
  },
})

const { trackRef, isDragging, startDrag, handleTrackClickCapture } = useDragScroll()
const repeatedNovels = computed(() => [...props.novels, ...props.novels, ...props.novels])

const getStepWidth = () => {
  const track = trackRef.value
  const firstCard = track?.children?.[0]
  if (!track || !firstCard) return 0
  const gap = Number.parseFloat(
    window.getComputedStyle(track).columnGap || window.getComputedStyle(track).gap || '0',
  )
  return firstCard.getBoundingClientRect().width + gap
}

const getSetWidth = () => getStepWidth() * props.novels.length

const alignToCenterSet = async () => {
  await nextTick()
  const track = trackRef.value
  const setWidth = getSetWidth()
  if (!track || !setWidth) return
  track.scrollLeft = setWidth
}

const normalizeInfiniteScroll = () => {
  const track = trackRef.value
  const setWidth = getSetWidth()
  const step = getStepWidth()
  if (!track || !setWidth || !step) return
  if (track.scrollLeft <= step) {
    track.scrollLeft += setWidth
  } else if (track.scrollLeft >= setWidth * 2 - step) {
    track.scrollLeft -= setWidth
  }
}

onMounted(() => {
  alignToCenterSet()
})

watch(
  () => props.novels.length,
  () => {
    alignToCenterSet()
  },
)
</script>

<template>
  <section class="space-y-4">
    <SectionTitle title="Популярное" subtitle="Популярное прямо сейчас" />

    <AppEmptyState v-if="!props.novels.length" compact> Новелы пока не найдены. </AppEmptyState>

    <div
      v-else
      ref="trackRef"
      :class="[
        'carousel-track flex gap-3 overflow-x-auto pb-2 select-none sm:gap-4',
        isDragging ? 'cursor-grabbing' : 'cursor-grab',
      ]"
      @scroll="normalizeInfiniteScroll"
      @mousedown="startDrag"
      @click.capture="handleTrackClickCapture"
      @dragstart.prevent
    >
      <NovelCard
        v-for="(novel, index) in repeatedNovels"
        :key="`${novel.id}-${index}`"
        :novel="novel"
      />
    </div>
  </section>
</template>
