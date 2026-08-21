<script setup>
import FilterSection from './FilterSection.vue'
import YearRangeFilterSection from './YearRangeFilterSection.vue'

const props = defineProps({
  filters: {
    type: Object,
    required: true,
  },
  options: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['toggle', 'set-year-range', 'reset'])
</script>

<template>
  <aside class="divide-y divide-zinc-800 rounded-xl border border-zinc-700/70 bg-zinc-900/80">
    <div class="flex items-center justify-between px-3 py-2.5">
      <h2 class="text-sm font-semibold text-zinc-200">Фильтры</h2>
      <button
        type="button"
        class="cursor-pointer text-xs text-zinc-500 transition hover:text-zinc-300"
        @click="emit('reset')"
      >
        Сбросить
      </button>
    </div>

    <YearRangeFilterSection
      :filter-state="props.filters.releaseYearRange"
      @change="(bound, value) => emit('set-year-range', bound, value)"
    />

    <FilterSection
      title="Возраст"
      :options="props.options.ageRatings"
      :include-state="props.filters.ageRatings.include"
      :exclude-state="props.filters.ageRatings.exclude"
      @toggle="(mode, value) => emit('toggle', 'ageRatings', mode, value)"
    />

    <FilterSection
      title="Жанры"
      :options="props.options.genres"
      :include-state="props.filters.genres.include"
      :exclude-state="props.filters.genres.exclude"
      searchable
      @toggle="(mode, value) => emit('toggle', 'genres', mode, value)"
    />

    <FilterSection
      title="Теги"
      :options="props.options.tags"
      :include-state="props.filters.tags.include"
      :exclude-state="props.filters.tags.exclude"
      searchable
      @toggle="(mode, value) => emit('toggle', 'tags', mode, value)"
    />

    <FilterSection
      title="Язык оригинала"
      :options="props.options.originalLanguages"
      :include-state="props.filters.originalLanguages.include"
      :exclude-state="props.filters.originalLanguages.exclude"
      @toggle="(mode, value) => emit('toggle', 'originalLanguages', mode, value)"
    />

    <FilterSection
      title="Язык перевода"
      :options="props.options.translationLanguages"
      :include-state="props.filters.translationLanguages.include"
      :exclude-state="props.filters.translationLanguages.exclude"
      @toggle="(mode, value) => emit('toggle', 'translationLanguages', mode, value)"
    />
  </aside>
</template>
