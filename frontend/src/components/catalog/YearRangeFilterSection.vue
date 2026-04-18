<script setup>
	import { computed, ref } from 'vue'
	import ChevronRightIcon from '../icons/ChevronRightIcon.vue'
	import AppInput from '../shared/AppInput.vue'
	import AppPanel from '../shared/AppPanel.vue'

	const props = defineProps({
		filterState: {
			type: Object,
			required: true
		}
	})

	const emit = defineEmits(['change'])
	const isOpen = ref(false)

	const activeCount = computed(() => {
		let count = 0
		if (props.filterState.from) count += 1
		if (props.filterState.to) count += 1
		return count
	})
</script>

<template>
	<AppPanel as="section">
		<button
			type="button"
			class="flex w-full cursor-pointer items-center justify-between gap-2 rounded-lg px-1 py-1 text-left transition hover:bg-zinc-800/50 active:scale-[0.99]"
			@click="isOpen = !isOpen"
		>
			<div class="min-w-0">
				<h3 class="text-sm font-semibold text-white">Год выпуска</h3>
			</div>
			<div class="flex items-center gap-2">
				<span v-if="activeCount" class="rounded-full bg-lime-300 px-2 py-0.5 text-[11px] font-semibold text-zinc-900">
					{{ activeCount }}
				</span>
				<ChevronRightIcon :class="['text-zinc-400 transition-transform', isOpen ? 'rotate-90' : 'rotate-0']" />
			</div>
		</button>

		<div v-if="isOpen" class="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
			<div>
				<label class="mb-1 block text-xs text-zinc-400" for="release-year-from">Год от</label>
				<AppInput
					id="release-year-from"
					:value="props.filterState.from"
					type="number"
					inputmode="numeric"
					placeholder="Например, 2020"
					min="1900"
					max="2100"
					class="year-number-input w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-center text-xs text-white outline-none transition focus:border-lime-300"
					@input="emit('change', 'from', $event.target.value)"
				/>
			</div>
			<div>
				<label class="mb-1 block text-xs text-zinc-400" for="release-year-to">Год до</label>
				<AppInput
					id="release-year-to"
					:value="props.filterState.to"
					type="number"
					inputmode="numeric"
					placeholder="Например, 2025"
					min="1900"
					max="2100"
					class="year-number-input w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-center text-xs text-white outline-none transition focus:border-lime-300"
					@input="emit('change', 'to', $event.target.value)"
				/>
			</div>
		</div>
	</AppPanel>
</template>
