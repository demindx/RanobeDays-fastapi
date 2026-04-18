<script setup>
	import { reactive, watch } from 'vue'
	import AppInput from '../shared/AppInput.vue'
	import AppButton from '../shared/AppButton.vue'

	const props = defineProps({
		bookmarks: {
			type: Array,
			default: () => []
		},
		error: {
			type: String,
			default: ''
		}
	})

	const emit = defineEmits(['rename'])

	const drafts = reactive({})

	const syncDrafts = () => {
		props.bookmarks.forEach((bookmark) => {
			drafts[bookmark.id] = bookmark.name
		})
	}

	syncDrafts()

	watch(
		() => props.bookmarks,
		() => {
			syncDrafts()
		},
		{ deep: true }
	)
</script>

<template>
	<div class="space-y-2">
		<div
			v-for="bookmark in props.bookmarks"
			:key="bookmark.id"
			class="rounded-lg border border-zinc-700 bg-zinc-800/70 p-2.5"
		>
			<div class="flex flex-col gap-2 sm:flex-row">
				<AppInput
					v-model="drafts[bookmark.id]"
					type="text"
					class="w-full rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-sm text-white outline-none transition focus:border-lime-300"
				/>
				<AppButton variant="neutral" size="sm" class="bg-zinc-900" @click="emit('rename', bookmark.id, drafts[bookmark.id])">
					Сохранить
				</AppButton>
			</div>
		</div>
		<p v-if="props.error" class="text-xs text-red-400">{{ props.error }}</p>
	</div>
</template>
