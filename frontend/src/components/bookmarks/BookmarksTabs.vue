<script setup>
	const props = defineProps({
		bookmarks: {
			type: Array,
			default: () => []
		},
		activeId: {
			type: String,
			default: null
		}
	})

	const emit = defineEmits(['select'])
</script>

<template>
	<div v-if="props.bookmarks.length" class="flex gap-2 overflow-x-auto pb-1 pr-1">
		<button
			v-for="bookmark in props.bookmarks"
			:key="bookmark.id"
			type="button"
			:class="[
				'cursor-pointer whitespace-nowrap rounded-full border px-3 py-1.5 text-xs font-medium transition active:scale-95 sm:text-sm',
				bookmark.id === props.activeId
					? 'border-emerald-300 bg-emerald-300/20 text-emerald-200'
					: 'border-zinc-700 bg-zinc-800 text-zinc-300 hover:border-lime-300/60 hover:bg-zinc-700'
			]"
			@click="emit('select', bookmark.id)"
		>
			{{ bookmark.name }}
		</button>
	</div>

	<p v-else class="text-xs text-zinc-500 sm:text-sm">Нет видимых закладок. Включите их в настройках.</p>
</template>
