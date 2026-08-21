<script setup>
import { useDragScroll } from '../../composables/useDragScroll'
import SectionTitle from '../ui/SectionTitle.vue'
import ContinueCard from '../cards/ContinueCard.vue'
import AppEmptyState from '../shared/AppEmptyState.vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})

const { trackRef, isDragging, startDrag, handleTrackClickCapture } = useDragScroll()
</script>

<template>
  <section class="space-y-4">
    <SectionTitle title="Продолжить чтение" subtitle="Ваш текущий прогресс" />

    <AppEmptyState v-if="!props.items.length" compact>
      Добавьте новелы в библиотеку, чтобы отслеживать прогресс.
    </AppEmptyState>

    <div
      v-else
      ref="trackRef"
      :class="[
        'carousel-track flex gap-3 overflow-x-auto pb-2 select-none sm:gap-4',
        isDragging ? 'cursor-grabbing' : 'cursor-grab',
      ]"
      @mousedown="startDrag"
      @click.capture="handleTrackClickCapture"
      @dragstart.prevent
    >
      <div
        v-for="item in props.items"
        :key="item.id"
        class="w-[260px] shrink-0 sm:w-[300px] lg:w-[340px]"
      >
        <ContinueCard :item="item" />
      </div>
    </div>
  </section>
</template>
