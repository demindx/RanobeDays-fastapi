<script setup>
	import AppEmptyState from '../shared/AppEmptyState.vue'
	import AppPanel from '../shared/AppPanel.vue'

	const props = defineProps({
		comments: {
			type: Array,
			default: () => []
		}
	})
</script>

<template>
	<AppPanel as="section" class="rounded-2xl space-y-3">
		<h3 class="text-base font-semibold text-white">Комментарии</h3>

		<AppEmptyState v-if="!props.comments.length" compact>
			Комментариев пока нет.
		</AppEmptyState>

		<div v-else class="space-y-2">
			<div
				v-for="comment in props.comments"
				:key="comment.id"
				class="rounded-xl border border-zinc-700/70 bg-zinc-800/50 p-3"
			>
				<div class="flex items-center justify-between gap-2">
					<p class="text-sm font-semibold text-zinc-200">{{ comment.author }}</p>
					<span class="text-xs text-zinc-500">{{ comment.timeAgo }}</span>
				</div>
				<p class="mt-1 text-sm text-zinc-300">{{ comment.text }}</p>
			</div>
		</div>
	</AppPanel>
</template>
