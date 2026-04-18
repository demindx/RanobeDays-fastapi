<script setup>
	import AppButton from '../shared/AppButton.vue'
	import AppPanel from '../shared/AppPanel.vue'

	const props = defineProps({
		viewMode: {
			type: String,
			required: true
		},
		total: {
			type: Number,
			default: 0
		},
		activeFilters: {
			type: Number,
			default: 0
		}
	})

	const emit = defineEmits(['change-view', 'open-filters'])
</script>

<template>
	<AppPanel class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
		<div>
			<h1 class="text-lg font-semibold text-white">Каталог новел</h1>
			<p class="text-xs text-zinc-400">
				Найдено: {{ props.total }}
				<span v-if="props.activeFilters"> · Активных фильтров: {{ props.activeFilters }}</span>
			</p>
		</div>

		<div class="flex items-center gap-2">
			<AppButton variant="neutral" size="sm" class="lg:hidden" @click="emit('open-filters')">
				Фильтры
			</AppButton>

			<div class="flex rounded-lg border border-zinc-700 bg-zinc-800 p-0.5">
				<button
					type="button"
					:class="[
						'cursor-pointer rounded-md px-3 py-1.5 text-xs transition active:scale-95',
						props.viewMode === 'grid' ? 'bg-lime-300 font-semibold text-zinc-900' : 'text-zinc-300 hover:bg-zinc-700'
					]"
					@click="emit('change-view', 'grid')"
				>
					Сетка
				</button>
				<button
					type="button"
					:class="[
						'cursor-pointer rounded-md px-3 py-1.5 text-xs transition active:scale-95',
						props.viewMode === 'list' ? 'bg-emerald-300 font-semibold text-zinc-900' : 'text-zinc-300 hover:bg-zinc-700'
					]"
					@click="emit('change-view', 'list')"
				>
					Список
				</button>
			</div>
		</div>
	</AppPanel>
</template>
