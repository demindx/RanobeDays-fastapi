<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'

const props = defineProps({
  tabs: {
    type: Array,
    default: () => [],
  },
  modelValue: {
    type: [String, Number],
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

const barRef = ref(null)
const labelRefs = ref({})
const indicatorLeft = ref(0)
const indicatorWidth = ref(0)

const setLabelRef = (key) => (el) => {
  if (el) labelRefs.value[key] = el
}

const recalcIndicator = () => {
  requestAnimationFrame(() => {
    const bar = barRef.value
    const label = labelRefs.value[props.modelValue]
    if (!bar || !label) return

    const barRect = bar.getBoundingClientRect()
    const labelRect = label.getBoundingClientRect()
    indicatorLeft.value = labelRect.left - barRect.left
    indicatorWidth.value = labelRect.width
  })
}

const select = (key) => {
  emit('update:modelValue', key)
  nextTick(recalcIndicator)
}

onMounted(() => {
  recalcIndicator()
})

watch(
  () => props.tabs,
  () => {
    nextTick(recalcIndicator)
  },
  { deep: true },
)
</script>

<template>
  <div ref="barRef" class="relative flex overflow-x-auto border-b border-zinc-800">
    <button
      v-for="tab in props.tabs"
      :key="tab.key"
      type="button"
      :class="[
        'shrink-0 px-5 py-3 text-sm font-medium transition-colors',
        tab.key === props.modelValue ? 'text-lime-300' : 'text-zinc-400 hover:text-zinc-200',
      ]"
      @click="select(tab.key)"
    >
      <span :ref="setLabelRef(tab.key)" class="inline-flex items-center">
        {{ tab.label }}
        <span
          v-if="tab.count != null"
          class="ml-1.5 rounded-full px-1.5 py-0.5 text-xs"
          :class="
            tab.key === props.modelValue
              ? 'bg-lime-300/15 text-lime-300'
              : 'bg-zinc-800 text-zinc-500'
          "
        >
          {{ tab.count }}
        </span>
      </span>
    </button>

    <span
      class="absolute bottom-0 h-0.5 rounded-full bg-lime-300 transition-all duration-300 ease-out"
      :style="{
        left: indicatorLeft + 'px',
        width: indicatorWidth + 'px',
      }"
    />
  </div>
</template>
