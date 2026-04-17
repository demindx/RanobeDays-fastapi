<script setup>
	const props = defineProps({
		item: {
			type: Object,
			required: true
		}
	})
</script>

<template>
	<article class="rounded-2xl border border-zinc-700/70 bg-zinc-900/70 p-3 sm:p-4">
		<h3 class="line-clamp-2 text-sm font-semibold text-white">{{ props.item.title }}</h3>
		<p class="mt-1 text-xs text-zinc-400">Глава {{ props.item.currentChapter }} из {{ props.item.totalChapters }}</p>

		<div class="mt-4 h-2 overflow-hidden rounded-full bg-zinc-700">
			<div class="h-full rounded-full bg-lime-300" :style="{ width: `${props.item.progress}%` }" />
		</div>

		<div class="mt-3 flex items-center justify-between gap-2">
			<span class="text-xs text-zinc-400">{{ props.item.progress }}%</span>
			<button class="cursor-pointer rounded-lg bg-lime-300 px-3 py-1 text-xs font-semibold text-zinc-900 transition hover:bg-lime-200 active:scale-95">
				Читать
			</button>
		</div>
	</article>
</template>
