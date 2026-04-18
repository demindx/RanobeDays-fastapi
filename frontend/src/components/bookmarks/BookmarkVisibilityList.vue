<script setup>
	import AppButton from '../shared/AppButton.vue'

	const props = defineProps({
		bookmarks: {
			type: Array,
			default: () => []
		}
	})

	const emit = defineEmits(['toggle'])
</script>

<template>
	<div class="space-y-2">
		<div
			v-for="bookmark in props.bookmarks"
			:key="bookmark.id"
			class="flex items-center justify-between gap-2 rounded-lg border border-zinc-700 bg-zinc-800/70 px-3 py-2"
		>
			<span class="truncate text-sm text-zinc-200">{{ bookmark.name }}</span>
			<AppButton
				:variant="bookmark.isPublic ? 'success' : 'danger'"
				size="sm"
				class="rounded-full"
				@click="emit('toggle', bookmark.id)"
			>
				{{ bookmark.isPublic ? 'Публичная' : 'Приватная' }}
			</AppButton>
		</div>
	</div>
</template>
