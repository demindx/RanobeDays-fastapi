<script setup>
	import FilterSection from './FilterSection.vue'
	import YearRangeFilterSection from './YearRangeFilterSection.vue'
	import AppButton from '../shared/AppButton.vue'
	import FilterGroup from '../shared/FilterGroup.vue'
	import AppPanel from '../shared/AppPanel.vue'

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

	const emit = defineEmits(['toggle', 'set-year-range', 'reset'])
</script>

<template>
	<aside class="space-y-3">
		<AppPanel>
			<h2 class="text-base font-semibold text-white">Фильтры</h2>
			<p class="mt-1 text-xs text-zinc-400">Год — диапазон. Остальные фильтры разделены на включение и исключение.</p>
			<AppButton variant="neutral" block class="mt-3" @click="emit('reset')">
				Сбросить все фильтры
			</AppButton>
		</AppPanel>

		<YearRangeFilterSection
			:filter-state="props.filters.releaseYearRange"
			@change="(bound, value) => emit('set-year-range', bound, value)"
		/>

		<FilterGroup title="Включить" description="Выбранные теги должны присутствовать у новелы." accent="include">
			<FilterSection
				title="Возрастное ограничение"
				mode="include"
				:options="props.options.ageRatings"
				:filter-state="props.filters.ageRatings"
				@toggle="(mode, value) => emit('toggle', 'ageRatings', mode, value)"
			/>
			<FilterSection
				title="Жанры"
				mode="include"
				:options="props.options.genres"
				:filter-state="props.filters.genres"
				searchable
				@toggle="(mode, value) => emit('toggle', 'genres', mode, value)"
			/>
			<FilterSection
				title="Теги"
				mode="include"
				:options="props.options.tags"
				:filter-state="props.filters.tags"
				searchable
				@toggle="(mode, value) => emit('toggle', 'tags', mode, value)"
			/>
			<FilterSection
				title="Язык оригинала"
				mode="include"
				:options="props.options.originalLanguages"
				:filter-state="props.filters.originalLanguages"
				@toggle="(mode, value) => emit('toggle', 'originalLanguages', mode, value)"
			/>
			<FilterSection
				title="Язык перевода"
				mode="include"
				:options="props.options.translationLanguages"
				:filter-state="props.filters.translationLanguages"
				@toggle="(mode, value) => emit('toggle', 'translationLanguages', mode, value)"
			/>
		</FilterGroup>

		<FilterGroup title="Исключить" description="Выбранные теги не должны присутствовать у новелы." accent="exclude">
			<FilterSection
				title="Возрастное ограничение"
				mode="exclude"
				:options="props.options.ageRatings"
				:filter-state="props.filters.ageRatings"
				@toggle="(mode, value) => emit('toggle', 'ageRatings', mode, value)"
			/>
			<FilterSection
				title="Жанры"
				mode="exclude"
				:options="props.options.genres"
				:filter-state="props.filters.genres"
				searchable
				@toggle="(mode, value) => emit('toggle', 'genres', mode, value)"
			/>
			<FilterSection
				title="Теги"
				mode="exclude"
				:options="props.options.tags"
				:filter-state="props.filters.tags"
				searchable
				@toggle="(mode, value) => emit('toggle', 'tags', mode, value)"
			/>
			<FilterSection
				title="Язык оригинала"
				mode="exclude"
				:options="props.options.originalLanguages"
				:filter-state="props.filters.originalLanguages"
				@toggle="(mode, value) => emit('toggle', 'originalLanguages', mode, value)"
			/>
			<FilterSection
				title="Язык перевода"
				mode="exclude"
				:options="props.options.translationLanguages"
				:filter-state="props.filters.translationLanguages"
				@toggle="(mode, value) => emit('toggle', 'translationLanguages', mode, value)"
			/>
		</FilterGroup>
	</aside>
</template>
