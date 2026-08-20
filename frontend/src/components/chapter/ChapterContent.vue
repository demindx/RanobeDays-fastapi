<script setup>
import { computed } from 'vue'
import { useChapterSettings } from '../../composables/useChapterSettings'
import AppEmptyState from '../shared/AppEmptyState.vue'
import AppLoading from '../shared/AppLoading.vue'

const props = defineProps({
  chapter: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
})

const { settings, currentBg, currentFont } = useChapterSettings()

const textColor = computed(() => currentBg()?.text || '#e4e4e7')
const maxWidthStyle = computed(() => settings.value.contentWidth + 'px')
const fontFamily = computed(() => currentFont()?.family || 'Inter, sans-serif')
</script>

<template>
  <AppLoading v-if="props.loading" label="Загрузка главы..." />

  <AppEmptyState v-else-if="props.error" compact>
    {{ props.error }}
  </AppEmptyState>

  <AppEmptyState v-else-if="!props.chapter" compact> Глава не найдена. </AppEmptyState>

  <article
    v-else
    :style="{
      color: textColor,
      fontFamily: fontFamily,
      fontSize: settings.fontSize + 'px',
      lineHeight: 1.85,
      maxWidth: maxWidthStyle,
    }"
    class="mx-auto w-full px-5 py-10 transition-all duration-300 sm:px-8 sm:py-14"
  >
    <div class="mb-10 text-center">
      <h1 class="text-xl font-bold sm:text-2xl">Глава {{ props.chapter.number }}</h1>
      <h2 v-if="props.chapter.title" class="mt-2 text-base opacity-60 sm:text-lg">
        {{ props.chapter.title }}
      </h2>
    </div>

    <div class="space-y-5" :style="{ wordSpacing: '0.05em' }">
      <p v-for="(paragraph, idx) in props.chapter.content" :key="idx">
        {{ paragraph }}
      </p>
    </div>
  </article>
</template>
