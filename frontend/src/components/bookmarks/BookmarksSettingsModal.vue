<script setup>
	import { ref, watch } from 'vue'
	import BookmarkVisibilityList from './BookmarkVisibilityList.vue'
	import BookmarkRenameList from './BookmarkRenameList.vue'
	import BookmarkCreateForm from './BookmarkCreateForm.vue'
	import AppButton from '../shared/AppButton.vue'
	import AppModal from '../shared/AppModal.vue'
	import AppPanel from '../shared/AppPanel.vue'

	const props = defineProps({
		open: {
			type: Boolean,
			default: false
		},
		bookmarks: {
			type: Array,
			default: () => []
		},
		onTogglePrivacy: {
			type: Function,
			required: true
		},
		onRename: {
			type: Function,
			required: true
		},
		onCreate: {
			type: Function,
			required: true
		}
	})

	const emit = defineEmits(['close'])
	const renameError = ref('')
	const createError = ref('')
	const createName = ref('')

	const handleTogglePrivacy = (bookmarkId) => {
		props.onTogglePrivacy(bookmarkId)
	}

	const handleRename = (bookmarkId, value) => {
		const result = props.onRename(bookmarkId, value)
		renameError.value = result.ok ? '' : result.error
	}

	const handleCreate = () => {
		const result = props.onCreate(createName.value)
		createError.value = result.ok ? '' : result.error
		if (result.ok) createName.value = ''
	}

	watch(
		() => props.open,
		(next) => {
			if (next) return
			renameError.value = ''
			createError.value = ''
			createName.value = ''
		}
	)
</script>

<template>
	<AppModal
		:open="props.open"
		container-class="flex items-end justify-center px-3 py-3 sm:items-center sm:px-4 sm:py-6"
		panel-class="max-h-[92vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-zinc-700 bg-zinc-900 p-4 shadow-2xl sm:p-5"
		@close="emit('close')"
	>
			<div class="mb-4 flex items-center justify-between gap-2">
				<div>
					<h3 class="text-base font-semibold text-white sm:text-lg">Настройки закладок</h3>
					<p class="text-xs text-zinc-400">Управляйте видимостью, названиями и списком закладок.</p>
				</div>
				<AppButton variant="neutral" size="sm" class="shrink-0" @click="emit('close')">
					Закрыть
				</AppButton>
			</div>

			<div class="space-y-4">
				<AppPanel as="section">
					<h4 class="text-sm font-semibold text-white">Приватность закладок</h4>
					<p class="mb-2 mt-1 text-[11px] text-zinc-500">Публичная — видна другим, приватная — только вам.</p>
					<BookmarkVisibilityList :bookmarks="props.bookmarks" @toggle="handleTogglePrivacy" />
				</AppPanel>

				<AppPanel as="section">
					<h4 class="text-sm font-semibold text-white">Переименование</h4>
					<p class="mb-2 mt-1 text-[11px] text-zinc-500">Название должно быть уникальным и непустым.</p>
					<BookmarkRenameList :bookmarks="props.bookmarks" :error="renameError" @rename="handleRename" />
				</AppPanel>

				<AppPanel as="section">
					<h4 class="text-sm font-semibold text-white">Создать новую закладку</h4>
					<p class="mb-2 mt-1 text-[11px] text-zinc-500">Новая закладка появится в панели выбора автоматически.</p>
					<BookmarkCreateForm v-model="createName" :error="createError" @create="handleCreate" />
				</AppPanel>
			</div>
	</AppModal>
</template>
