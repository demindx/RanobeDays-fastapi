<script setup>
	import AppButton from '../shared/AppButton.vue'

	const props = defineProps({
		activeTab: {
			type: String,
			default: 'description'
		}
	})

	const emit = defineEmits(['change'])
</script>

<template>
	<div class="flex gap-2 rounded-xl border border-zinc-700/70 bg-zinc-900/70 p-2">
		<AppButton
			:variant="props.activeTab === 'description' ? 'primary' : 'neutral'"
			size="sm"
			class="font-semibold"
			@click="emit('change', 'description')"
		>
			Описание
		</AppButton>
		<AppButton
			:variant="props.activeTab === 'chapters' ? 'primary' : 'neutral'"
			size="sm"
			class="font-semibold"
			@click="emit('change', 'chapters')"
		>
			Главы
		</AppButton>
	</div>
</template>
