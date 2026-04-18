<script setup>
	const props = defineProps({
		genres: {
			type: Array,
			default: () => []
		},
		tags: {
			type: Array,
			default: () => []
		},
		translators: {
			type: Array,
			default: () => []
		}
	})
</script>

<template>
	<div class="space-y-2">
		<div class="flex flex-wrap items-center gap-1.5">
			<span class="text-xs font-semibold text-zinc-400">Жанры:</span>
			<span
				v-for="genre in props.genres"
				:key="`genre-${genre}`"
				class="rounded-full border border-emerald-300/40 bg-emerald-400/15 px-2 py-0.5 text-xs text-emerald-200"
			>
				{{ genre }}
			</span>
		</div>

		<div class="flex flex-wrap items-center gap-1.5">
			<span class="text-xs font-semibold text-zinc-400">Теги:</span>
			<span
				v-for="tag in props.tags"
				:key="`tag-${tag}`"
				class="rounded-full border border-lime-300/40 bg-lime-400/15 px-2 py-0.5 text-xs text-lime-200"
			>
				{{ tag }}
			</span>
		</div>

		<div class="flex flex-wrap items-center gap-1.5">
			<span class="text-xs font-semibold text-zinc-400">Переводчики:</span>
			<span
				v-for="translator in props.translators"
				:key="`translator-${translator}`"
				class="rounded-full border border-zinc-600 bg-zinc-800 px-2 py-0.5 text-xs text-zinc-200"
			>
				{{ translator }}
			</span>
		</div>
	</div>
</template>
