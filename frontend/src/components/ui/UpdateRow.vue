<script setup>
	const props = defineProps({
		update: {
			type: Object,
			required: true
		}
	})
</script>

<template>
	<a
		:href="props.update.href || '#'"
		class="flex flex-col gap-2 rounded-xl border border-zinc-700/70 bg-zinc-900/70 px-3 py-3 transition hover:border-lime-300/60 hover:bg-zinc-800/70 active:scale-[0.99] sm:flex-row sm:items-center sm:justify-between sm:gap-3 sm:px-4"
	>
		<div class="min-w-0">
			<p class="truncate text-sm font-medium text-white">{{ props.update.novelTitle }}</p>
			<p class="text-xs text-zinc-400">{{ props.update.chapter }}</p>
		</div>
		<span class="shrink-0 text-xs text-zinc-500">{{ props.update.timeAgo }}</span>
	</a>
</template>
