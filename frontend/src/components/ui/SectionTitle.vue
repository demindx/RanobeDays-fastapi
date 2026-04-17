<script setup>
	const props = defineProps({
		title: {
			type: String,
			required: true
		},
		subtitle: {
			type: String,
			default: ''
		}
	})
</script>

<template>
	<div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
		<div>
			<h2 class="text-lg font-bold text-white sm:text-xl md:text-2xl">{{ props.title }}</h2>
			<p v-if="props.subtitle" class="mt-1 text-xs text-zinc-400 sm:text-sm">{{ props.subtitle }}</p>
		</div>

		<slot name="action" />
	</div>
</template>
