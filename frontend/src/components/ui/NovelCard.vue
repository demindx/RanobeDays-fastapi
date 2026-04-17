<script setup>
	const props = defineProps({
		novel: {
			type: Object,
			required: true
		}
	})
</script>

<template>
	<a
		:href="props.novel.href || '#'"
		class="block w-[72vw] max-w-56 shrink-0 snap-start cursor-pointer rounded-2xl border border-zinc-700/70 bg-zinc-900/70 p-2.5 transition hover:border-lime-300/60 hover:bg-zinc-800/70 active:scale-[0.99] sm:w-56 sm:p-3"
	>
		<div :class="['h-28 rounded-xl bg-gradient-to-br sm:h-32', props.novel.coverStyle]" />

		<div class="mt-3">
			<h3 class="line-clamp-2 text-sm font-semibold text-white">{{ props.novel.title }}</h3>
			<p class="mt-1 text-xs text-zinc-400">{{ props.novel.genre }}</p>
		</div>

		<div class="mt-3 flex items-center justify-between text-xs text-zinc-300">
			<span>{{ props.novel.chapter }}</span>
			<span>★ {{ props.novel.rating }}</span>
		</div>
	</a>
</template>
