<script setup>
	const props = defineProps({
		item: {
			type: Object,
			required: true
		}
	})
</script>

<template>
	<a
		:href="props.item.href || '#'"
		class="flex h-full flex-col rounded-xl border border-zinc-700/70 bg-zinc-900/70 p-2.5 transition hover:border-lime-300/60 hover:bg-zinc-800/70 active:scale-[0.99] sm:rounded-2xl sm:p-3"
	>
		<div :class="['relative aspect-[2/3] w-full overflow-hidden rounded-lg bg-gradient-to-br sm:rounded-xl', props.item.coverStyle]">
			<img
				v-if="props.item.coverUrl"
				:src="props.item.coverUrl"
				:alt="props.item.title"
				class="absolute inset-0 h-full w-full object-cover"
				loading="lazy"
			/>
		</div>

		<div class="mt-2 min-h-[2.6rem]">
			<h3 class="line-clamp-2 text-sm font-semibold text-white">{{ props.item.title }}</h3>
		</div>
		<p class="mt-1 truncate text-xs text-zinc-400">{{ props.item.author }}</p>
		<div class="mt-2 flex items-center justify-between text-xs text-zinc-300">
			<span>{{ props.item.chapterLabel }}</span>
			<span>★ {{ props.item.rating }}</span>
		</div>
	</a>
</template>
