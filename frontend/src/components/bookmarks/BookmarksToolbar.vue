<script setup>
	import BookmarksTabs from './BookmarksTabs.vue'
	import SettingsIcon from '../icons/SettingsIcon.vue'
	import AppButton from '../shared/AppButton.vue'
	import AppPanel from '../shared/AppPanel.vue'

	const props = defineProps({
		bookmarks: {
			type: Array,
			default: () => []
		},
		activeId: {
			type: String,
			default: null
		}
	})

	const emit = defineEmits(['select', 'open-settings'])
</script>

<template>
	<AppPanel as="section" class="rounded-2xl p-3 sm:p-4">
		<div class="mb-3 flex items-center justify-between gap-2">
			<div>
				<h1 class="text-base font-semibold text-white sm:text-lg">Закладки</h1>
				<p class="text-xs text-zinc-400">Выберите закладку и управляйте списками чтения.</p>
			</div>

			<AppButton variant="neutral" class="shrink-0 gap-1.5 text-xs sm:text-sm" @click="emit('open-settings')">
				<SettingsIcon />
				<span>Настройки</span>
			</AppButton>
		</div>

		<BookmarksTabs :bookmarks="props.bookmarks" :active-id="props.activeId" @select="(id) => emit('select', id)" />
	</AppPanel>
</template>
