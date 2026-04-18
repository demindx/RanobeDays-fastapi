<script setup>
	const props = defineProps({
		title: {
			type: String,
			required: true
		},
		description: {
			type: String,
			default: ''
		},
		accent: {
			type: String,
			default: 'neutral'
		}
	})
</script>

<template>
	<div
		:class="[
			'space-y-2 rounded-2xl p-2.5',
			props.accent === 'include'
				? 'border border-emerald-300/25 bg-emerald-950/20'
				: props.accent === 'exclude'
					? 'border border-rose-300/25 bg-rose-950/20'
					: 'border border-zinc-700/70 bg-zinc-900/70'
		]"
	>
		<div
			:class="[
				'rounded-xl bg-zinc-900/80 p-3',
				props.accent === 'include'
					? 'border border-emerald-300/25'
					: props.accent === 'exclude'
						? 'border border-rose-300/25'
						: 'border border-zinc-700/70'
			]"
		>
			<span
				:class="[
					'inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold',
					props.accent === 'include'
						? 'border border-emerald-300/40 bg-emerald-400/15 text-emerald-300'
						: props.accent === 'exclude'
							? 'border border-rose-300/40 bg-rose-400/15 text-rose-300'
							: 'border border-zinc-500/60 bg-zinc-700/40 text-zinc-200'
				]"
			>
				{{ props.title }}
			</span>
			<p v-if="props.description" class="mt-1 text-[11px] text-zinc-400">{{ props.description }}</p>
		</div>
		<slot />
	</div>
</template>
