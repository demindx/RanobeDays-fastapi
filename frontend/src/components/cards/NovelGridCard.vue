<script setup>
	import { computed } from 'vue'
	import { RouterLink } from 'vue-router'

	const props = defineProps({
		novel: {
			type: Object,
			required: true
		}
	})

	const novelHref = computed(() =>
		props.novel.href && props.novel.href !== '#' ? props.novel.href : `/novel/${props.novel.id}`
	)

	const isInternalLink = computed(() => novelHref.value.startsWith('/'))
</script>

<template>
	<component
		:is="isInternalLink ? RouterLink : 'a'"
		:to="isInternalLink ? novelHref : undefined"
		:href="isInternalLink ? undefined : novelHref"
		class="flex h-full flex-col rounded-xl border border-zinc-700/70 bg-zinc-900/70 p-2 transition hover:border-lime-300/60 hover:bg-zinc-800/70 active:scale-[0.99] min-[480px]:rounded-2xl min-[480px]:p-2.5 sm:p-3"
	>
		<div :class="['relative aspect-[2/3] w-full overflow-hidden rounded-lg bg-gradient-to-br min-[480px]:rounded-xl', props.novel.coverStyle]">
			<img
				v-if="props.novel.coverUrl"
				:src="props.novel.coverUrl"
				:alt="props.novel.title"
				class="absolute inset-0 h-full w-full object-cover"
				loading="lazy"
			/>
		</div>
		<div class="mt-2 min-h-[2.5rem] sm:mt-3 sm:min-h-[2.75rem]">
			<h3 class="line-clamp-2 text-xs font-semibold leading-5 text-white min-[360px]:text-sm">{{ props.novel.title }}</h3>
		</div>
		<p class="mt-1 truncate text-[11px] text-zinc-400 min-[360px]:text-xs">{{ props.novel.releaseYear }} · {{ props.novel.ageRating }}</p>
		<p class="mt-1 truncate text-[11px] text-zinc-400 min-[360px]:text-xs">★ {{ props.novel.rating }} · {{ props.novel.chapters }} глав</p>
	</component>
</template>
