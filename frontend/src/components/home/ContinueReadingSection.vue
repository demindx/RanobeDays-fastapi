<script setup>
	import SectionTitle from '../ui/SectionTitle.vue'
	import ContinueCard from '../ui/ContinueCard.vue'

	const props = defineProps({
		items: {
			type: Array,
			default: () => []
		}
	})
</script>

<template>
	<section class="space-y-4">
		<SectionTitle title="Продолжить чтение" subtitle="Ваш текущий прогресс" />

		<p v-if="!props.items.length" class="rounded-xl border border-dashed border-zinc-700 bg-zinc-900/50 px-4 py-6 text-sm text-zinc-400">
			Добавьте новелы в библиотеку, чтобы отслеживать прогресс.
		</p>

		<div v-else class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
			<ContinueCard v-for="item in props.items" :key="item.id" :item="item" />
		</div>
	</section>
</template>
