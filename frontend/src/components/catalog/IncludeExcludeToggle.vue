<script setup>
	const props = defineProps({
		option: {
			type: [String, Number],
			required: true
		},
		include: {
			type: Array,
			default: () => []
		},
		exclude: {
			type: Array,
			default: () => []
		}
	})

	const emit = defineEmits(['toggle'])

	const isIncluded = () => props.include.includes(props.option)
	const isExcluded = () => props.exclude.includes(props.option)
</script>

<template>
	<div class="flex items-center gap-1.5">
		<button
			type="button"
			:class="[
				'cursor-pointer rounded-md border px-2 py-0.5 text-[11px] transition active:scale-95',
				isIncluded() ? 'border-emerald-400 bg-emerald-400/20 text-emerald-300' : 'border-zinc-700 text-zinc-400 hover:bg-zinc-800'
			]"
			@click="emit('toggle', 'include', props.option)"
		>
			+
		</button>
		<button
			type="button"
			:class="[
				'cursor-pointer rounded-md border px-2 py-0.5 text-[11px] transition active:scale-95',
				isExcluded() ? 'border-rose-400 bg-rose-400/20 text-rose-300' : 'border-zinc-700 text-zinc-400 hover:bg-zinc-800'
			]"
			@click="emit('toggle', 'exclude', props.option)"
		>
			−
		</button>
	</div>
</template>
