<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  novel: {
    type: Object,
    required: true,
  },
})

const novelHref = computed(() =>
  props.novel.href && props.novel.href !== '#' ? props.novel.href : `/novel/${props.novel.id}`,
)

const isInternalLink = computed(() => novelHref.value.startsWith('/'))
</script>

<template>
  <component
    :is="isInternalLink ? RouterLink : 'a'"
    :to="isInternalLink ? novelHref : undefined"
    :href="isInternalLink ? undefined : novelHref"
    class="grid grid-cols-[74px_minmax(0,1fr)] gap-2.5 rounded-2xl border border-zinc-700/70 bg-zinc-900/70 p-2.5 transition hover:border-lime-300/60 card-interactive min-[360px]:grid-cols-[88px_minmax(0,1fr)] sm:grid-cols-[130px_minmax(0,1fr)] sm:gap-3 sm:p-3"
  >
    <div
      :class="[
        'relative aspect-[2/3] w-full self-start overflow-hidden rounded-xl bg-gradient-to-br',
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

    <div class="min-w-0">
      <div class="flex flex-wrap items-center gap-2">
        <h3 class="line-clamp-2 text-xs font-semibold text-white min-[360px]:text-sm sm:text-base">
          {{ props.novel.title }}
        </h3>
        <span class="rounded-full border border-zinc-700 px-2 py-0.5 text-[11px] text-zinc-400">{{
          props.novel.status
        }}</span>
      </div>

      <p class="mt-1 text-xs text-zinc-400">
        {{ props.novel.author }} · {{ props.novel.releaseYear }} · {{ props.novel.ageRating }}
      </p>

      <p class="mt-1.5 line-clamp-2 text-xs text-zinc-300 sm:mt-2 sm:line-clamp-3 sm:text-sm">
        {{ props.novel.synopsis }}
      </p>

      <div class="mt-2 hidden flex-wrap gap-1.5 min-[380px]:flex">
        <span
          v-for="genre in props.novel.genres"
          :key="genre"
          class="rounded-full bg-zinc-800 px-2 py-0.5 text-[11px] text-zinc-300"
        >
          {{ genre }}
        </span>
      </div>

      <p class="mt-2 hidden text-xs text-zinc-400 min-[380px]:block">
        Оригинал: {{ props.novel.originalLanguage }} · Перевод:
        {{ props.novel.translationLanguage }}
      </p>
      <p class="mt-1 text-xs text-zinc-400">
        ★ {{ props.novel.rating }} · {{ props.novel.chapters }} глав
      </p>
    </div>
  </component>
</template>
