<script setup>
	const props = defineProps({
		open: {
			type: Boolean,
			default: false
		},
		containerClass: {
			type: String,
			default: 'flex items-center justify-center px-3 py-4 sm:px-4 sm:py-6'
		},
		panelClass: {
			type: String,
			default: 'w-full max-w-md rounded-2xl border border-zinc-700 bg-zinc-900 p-4 shadow-2xl sm:p-5'
		}
	})

	const emit = defineEmits(['close'])
</script>

<template>
	<div v-if="props.open" class="fixed inset-0 z-50 bg-black/65" :class="props.containerClass" @click.self="emit('close')">
		<div :class="props.panelClass">
			<slot />
		</div>
	</div>
</template>
