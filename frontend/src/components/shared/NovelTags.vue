<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  genres: {
    type: Array,
    default: () => [],
  },
  tags: {
    type: Array,
    default: () => [],
  },
  showLabels: {
    type: Boolean,
    default: false,
  },
  clickable: {
    type: Boolean,
    default: true,
  },
})

const router = useRouter()

const goToCatalog = (value, type) => {
  router.push({ path: '/catalog', query: { [type]: value } })
}
</script>

<template>
  <div class="space-y-1.5">
    <div v-if="props.genres.length" class="flex flex-wrap items-center gap-1.5">
      <span v-if="props.showLabels" class="text-xs font-semibold text-zinc-400">Жанры:</span>
      <template v-for="genre in props.genres" :key="`genre-${genre}`">
        <button
          v-if="props.clickable"
          type="button"
          class="cursor-pointer rounded-full border border-emerald-300/40 bg-emerald-400/15 px-2 py-0.5 text-xs text-emerald-200 transition hover:border-emerald-300/70 hover:bg-emerald-400/25 active:scale-95"
          @click.stop="goToCatalog(genre, 'genres')"
        >
          {{ genre }}
        </button>
        <span
          v-else
          class="rounded-full border border-emerald-300/40 bg-emerald-400/15 px-2 py-0.5 text-xs text-emerald-200"
        >
          {{ genre }}
        </span>
      </template>
    </div>

    <div v-if="props.tags.length" class="flex flex-wrap items-center gap-1.5">
      <span v-if="props.showLabels" class="text-xs font-semibold text-zinc-400">Теги:</span>
      <template v-for="tag in props.tags" :key="`tag-${tag}`">
        <button
          v-if="props.clickable"
          type="button"
          class="cursor-pointer rounded-md border border-lime-300/40 bg-lime-400/15 px-2 py-0.5 text-xs text-lime-200 transition hover:border-lime-300/70 hover:bg-lime-400/25 active:scale-95"
          @click.stop="goToCatalog(tag, 'tags')"
        >
          {{ tag }}
        </button>
        <span
          v-else
          class="rounded-md border border-lime-300/40 bg-lime-400/15 px-2 py-0.5 text-xs text-lime-200"
        >
          {{ tag }}
        </span>
      </template>
    </div>
  </div>
</template>
