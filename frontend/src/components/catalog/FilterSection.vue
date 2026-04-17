<script setup>
	import { computed, ref } from 'vue'
	import IncludeExcludeToggle from './IncludeExcludeToggle.vue'
	import ChevronRightIcon from '../icons/ChevronRightIcon.vue'

	const props = defineProps({
		title: {
			type: String,
			required: true
		},
		options: {
			type: Array,
			default: () => []
		},
		filterState: {
			type: Object,
			required: true
		},
		searchable: {
			type: Boolean,
			default: false
		}
	})

	const emit = defineEmits(['toggle'])
	const query = ref('')
	const isOpen = ref(false)

	const activeCount = computed(() => props.filterState.include.length + props.filterState.exclude.length)

	const filteredOptions = computed(() => {
		if (!props.searchable || !query.value.trim()) return props.options
		const lower = query.value.toLowerCase()
		return props.options.filter((item) => String(item).toLowerCase().includes(lower))
	})
</script>

<template>
	<section class="rounded-xl border border-zinc-700/70 bg-zinc-900/70 p-3">
		<button
			type="button"
			class="flex w-full cursor-pointer items-center justify-between gap-2 rounded-lg px-1 py-1 text-left transition hover:bg-zinc-800/50 active:scale-[0.99]"
			@click="isOpen = !isOpen"
		>
			<div class="min-w-0">
				<h3 class="text-sm font-semibold text-white">{{ props.title }}</h3>
			</div>
			<div class="flex items-center gap-2">
				<span v-if="activeCount" class="rounded-full bg-lime-300 px-2 py-0.5 text-[11px] font-semibold text-zinc-900">
					{{ activeCount }}
				</span>
				<ChevronRightIcon :class="['text-zinc-400 transition-transform', isOpen ? 'rotate-90' : 'rotate-0']" />
			</div>
		</button>

		<div v-if="isOpen" class="mt-2">
			<input
				v-if="props.searchable"
				v-model="query"
				type="text"
				placeholder="Поиск..."
				class="mb-2 w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-xs text-white outline-none transition focus:border-lime-300"
			/>

			<div class="max-h-52 space-y-1.5 overflow-y-auto pr-1">
				<div
					v-for="option in filteredOptions"
					:key="String(option)"
					class="flex items-center justify-between gap-2 rounded-md px-1 py-1 transition hover:bg-zinc-800/60"
				>
					<span class="truncate text-xs text-zinc-200">{{ option }}</span>
					<IncludeExcludeToggle
						:option="option"
						:include="props.filterState.include"
						:exclude="props.filterState.exclude"
						@toggle="(...args) => emit('toggle', ...args)"
					/>
				</div>
			</div>
		</div>
	</section>
</template>
