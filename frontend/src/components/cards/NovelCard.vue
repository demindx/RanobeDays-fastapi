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
    class="block w-[58vw] max-w-44 shrink-0 snap-start cursor-pointer rounded-2xl border border-zinc-700/70 bg-zinc-900/70 p-2.5 transition hover:border-lime-300/60 card-interactive sm:w-56 sm:max-w-56 sm:p-3"
  >
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

    <div class="mt-3">
      <h3 class="line-clamp-2 text-sm font-semibold text-white">{{ props.novel.title }}</h3>
      <p class="mt-1 text-xs text-zinc-400">{{ props.novel.genre }}</p>
    </div>

    <div class="mt-3 flex items-center justify-between text-xs text-zinc-300">
      <span>{{ props.novel.chapter }}</span>
      <span>★ {{ props.novel.rating }}</span>
    </div>
  </component>
</template>
