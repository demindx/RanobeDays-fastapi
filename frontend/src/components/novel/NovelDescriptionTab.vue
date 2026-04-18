<script setup>
	import AppPanel from '../shared/AppPanel.vue'
	import NovelMetaChips from './NovelMetaChips.vue'
	import NovelCommentsSection from './NovelCommentsSection.vue'

	const props = defineProps({
		novel: {
			type: Object,
			required: true
		}
	})
</script>

<template>
	<div class="space-y-3">
		<AppPanel as="section" class="rounded-2xl space-y-3">
			<NovelMetaChips :genres="props.novel.genres" :tags="props.novel.tags" :translators="props.novel.translators" />
			<div>
				<h3 class="text-base font-semibold text-white">Описание</h3>
				<p class="mt-2 whitespace-pre-line text-sm leading-6 text-zinc-300">
					{{ props.novel.description }}
				</p>
			</div>
		</AppPanel>

		<NovelCommentsSection :comments="props.novel.comments" />
	</div>
</template>
