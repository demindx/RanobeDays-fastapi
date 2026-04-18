<script setup>
	import BookmarkNovelCard from '../cards/BookmarkNovelCard.vue'
	import AppButton from '../shared/AppButton.vue'
	import AppEmptyState from '../shared/AppEmptyState.vue'

	const props = defineProps({
		bookmark: {
			type: Object,
			default: null
		}
	})

	const emit = defineEmits(['open-settings'])
</script>

<template>
	<section class="space-y-3">
		<div v-if="props.bookmark" class="flex items-end justify-between gap-3">
			<div>
				<h2 class="text-lg font-semibold text-white sm:text-xl">{{ props.bookmark.name }}</h2>
				<p class="text-xs text-zinc-400 sm:text-sm">Новел в закладке: {{ props.bookmark.items.length }}</p>
			</div>
		</div>

		<AppEmptyState v-if="!props.bookmark">
			Нет активной закладки. Включите хотя бы одну в настройках.
			<AppButton variant="primary" size="sm" class="mt-3 block font-semibold" @click="emit('open-settings')">
				Открыть настройки закладок
			</AppButton>
		</AppEmptyState>

		<AppEmptyState v-else-if="!props.bookmark.items.length">
			В этой закладке пока нет новел.
		</AppEmptyState>

		<div v-else class="grid grid-cols-2 gap-2.5 min-[480px]:grid-cols-3 sm:gap-3 lg:grid-cols-4">
			<BookmarkNovelCard v-for="item in props.bookmark.items" :key="item.id" :item="item" />
		</div>
	</section>
</template>
