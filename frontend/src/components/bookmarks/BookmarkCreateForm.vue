<script setup>
	import AppInput from '../shared/AppInput.vue'
	import AppButton from '../shared/AppButton.vue'

	const props = defineProps({
		modelValue: {
			type: String,
			default: ''
		},
		error: {
			type: String,
			default: ''
		}
	})

	const emit = defineEmits(['update:modelValue', 'create'])
</script>

<template>
	<div class="space-y-2">
		<div class="flex flex-col gap-2 sm:flex-row">
			<AppInput
				:value="props.modelValue"
				type="text"
				placeholder="Название новой закладки"
				class="w-full rounded-lg border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white outline-none transition focus:border-lime-300"
				@input="emit('update:modelValue', $event.target.value)"
			/>
			<AppButton variant="primary" size="md" class="font-semibold" @click="emit('create')">
				Создать
			</AppButton>
		</div>
		<p v-if="props.error" class="text-xs text-red-400">{{ props.error }}</p>
	</div>
</template>
