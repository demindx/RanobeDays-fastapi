<script setup>
	import SectionTitle from '../ui/SectionTitle.vue'
	import UpdateRow from '../ui/UpdateRow.vue'

	const props = defineProps({
		updates: {
			type: Array,
			default: () => []
		}
	})
</script>

<template>
	<section class="space-y-4">
		<SectionTitle title="Последние обновления" subtitle="Новые главы и переводы" />

		<p v-if="!props.updates.length" class="rounded-xl border border-dashed border-zinc-700 bg-zinc-900/50 px-4 py-6 text-sm text-zinc-400">
			Пока нет свежих обновлений.
		</p>

		<div v-else class="space-y-2">
			<UpdateRow v-for="item in props.updates" :key="item.id" :update="item" />
		</div>
	</section>
</template>
