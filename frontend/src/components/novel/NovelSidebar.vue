<script setup>
import { computed } from 'vue'
import AppButton from '../shared/AppButton.vue'
import AppSelect from '../shared/AppSelect.vue'
import AppPanel from '../shared/AppPanel.vue'

const props = defineProps({
  novel: {
    type: Object,
    required: true,
  },
  bookmarkOptions: {
    type: Array,
    default: () => [],
  },
  selectedBookmarkId: {
    type: String,
    default: '',
  },
  readingCtaLabel: {
    type: String,
    default: 'Читать',
  },
})

const emit = defineEmits(['update-bookmark', 'remove-bookmark'])

const readHref = computed(() => {
  const firstChapter = props.novel.chapters?.[0]
  if (firstChapter) {
    return `/novel/${props.novel.id}/chapter/${firstChapter.id}`
  }
  return `/novel/${props.novel.id}`
})
</script>

<template>
  <AppPanel class="rounded-2xl p-3 sm:p-4">
    <div
      :class="[
        'relative aspect-[2/3] w-full overflow-hidden rounded-xl bg-gradient-to-br',
        props.novel.coverStyle,
      ]"
    >
      <img
        v-if="props.novel.coverUrl"
        :src="props.novel.coverUrl"
        :alt="props.novel.title"
        class="absolute inset-0 h-full w-full object-cover"
        loading="lazy"
      />
    </div>

    <div class="mt-4 space-y-2">
      <p class="text-xs font-medium uppercase tracking-wide text-emerald-300">
        Добавить в закладку
      </p>
      <AppSelect
        :model-value="props.selectedBookmarkId"
        :options="props.bookmarkOptions"
        placeholder="Выберите закладку"
        variant="green"
        :action-label="props.selectedBookmarkId ? 'Убрать из закладок' : ''"
        @update:model-value="emit('update-bookmark', $event)"
        @action="emit('remove-bookmark')"
      />
    </div>

    <AppButton variant="primary-gradient" block class="mt-3 font-semibold" :href="readHref">
      {{ props.readingCtaLabel }}
    </AppButton>

    <div class="mt-3 rounded-xl border border-zinc-700/70 bg-zinc-800/60 p-3">
      <p class="text-xs text-zinc-400">
        Статус: <span class="font-medium text-zinc-200">{{ props.novel.status }}</span>
      </p>
      <p class="mt-1 text-xs text-zinc-400">
        Год выпуска: <span class="font-medium text-zinc-200">{{ props.novel.releaseYear }}</span>
      </p>
    </div>
  </AppPanel>
</template>
