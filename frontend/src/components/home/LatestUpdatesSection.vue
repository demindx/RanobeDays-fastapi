<script setup>
	import SectionTitle from '../ui/SectionTitle.vue'
	import UpdateRow from '../ui/UpdateRow.vue'
	import AppEmptyState from '../shared/AppEmptyState.vue'

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

		<AppEmptyState v-if="!props.updates.length" compact>
			Пока нет свежих обновлений.
		</AppEmptyState>

		<div v-else class="space-y-2">
			<UpdateRow v-for="item in props.updates" :key="item.id" :update="item" />
		</div>
	</section>
</template>
