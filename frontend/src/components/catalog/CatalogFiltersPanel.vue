<script setup>
	import FilterSection from './FilterSection.vue'

	const props = defineProps({
		filters: {
			type: Object,
			required: true
		},
		options: {
			type: Object,
			required: true
		}
	})

	const emit = defineEmits(['toggle', 'reset'])
</script>

<template>
	<aside class="space-y-3">
		<div class="rounded-xl border border-zinc-700/70 bg-zinc-900/70 p-3">
			<h2 class="text-base font-semibold text-white">Фильтры</h2>
			<p class="mt-1 text-xs text-zinc-400">Можно включать и исключать параметры.</p>
			<button
				type="button"
				class="mt-3 w-full cursor-pointer rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-zinc-200 transition hover:bg-zinc-700 active:scale-95"
				@click="emit('reset')"
			>
				Сбросить все фильтры
			</button>
		</div>

		<FilterSection
			title="Год выпуска"
			:options="props.options.releaseYears"
			:filter-state="props.filters.releaseYears"
			@toggle="(mode, value) => emit('toggle', 'releaseYears', mode, value)"
		/>
		<FilterSection
			title="Возрастное ограничение"
			:options="props.options.ageRatings"
			:filter-state="props.filters.ageRatings"
			@toggle="(mode, value) => emit('toggle', 'ageRatings', mode, value)"
		/>
		<FilterSection
			title="Жанры"
			:options="props.options.genres"
			:filter-state="props.filters.genres"
			searchable
			@toggle="(mode, value) => emit('toggle', 'genres', mode, value)"
		/>
		<FilterSection
			title="Теги"
			:options="props.options.tags"
			:filter-state="props.filters.tags"
			searchable
			@toggle="(mode, value) => emit('toggle', 'tags', mode, value)"
		/>
		<FilterSection
			title="Язык оригинала"
			:options="props.options.originalLanguages"
			:filter-state="props.filters.originalLanguages"
			@toggle="(mode, value) => emit('toggle', 'originalLanguages', mode, value)"
		/>
		<FilterSection
			title="Язык перевода"
			:options="props.options.translationLanguages"
			:filter-state="props.filters.translationLanguages"
			@toggle="(mode, value) => emit('toggle', 'translationLanguages', mode, value)"
		/>
	</aside>
</template>
