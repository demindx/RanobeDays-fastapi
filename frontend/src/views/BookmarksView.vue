<script setup>
	import BookmarksToolbar from '../components/bookmarks/BookmarksToolbar.vue'
	import BookmarksContent from '../components/bookmarks/BookmarksContent.vue'
	import BookmarksSettingsModal from '../components/bookmarks/BookmarksSettingsModal.vue'
	import AppSectionSwitchTransition from '../components/shared/AppSectionSwitchTransition.vue'
	import { useBookmarks } from '../composables/useBookmarks'

	const {
		bookmarks,
		activeBookmark,
		activeBookmarkId,
		isSettingsOpen,
		setActive,
		openSettings,
		closeSettings,
		togglePrivacy,
		renameBookmark,
		createBookmark
	} = useBookmarks()
</script>

<template>
	<div>
		<div class="space-y-4 md:space-y-6">
			<BookmarksToolbar
				:bookmarks="bookmarks"
				:active-id="activeBookmarkId"
				@select="setActive"
				@open-settings="openSettings"
			/>

			<AppSectionSwitchTransition>
				<BookmarksContent
					:key="`bookmark-content-${activeBookmarkId || 'none'}`"
					:bookmark="activeBookmark"
					@open-settings="openSettings"
				/>
			</AppSectionSwitchTransition>
		</div>

		<BookmarksSettingsModal
			:open="isSettingsOpen"
			:bookmarks="bookmarks"
			:on-toggle-privacy="togglePrivacy"
			:on-rename="renameBookmark"
			:on-create="createBookmark"
			@close="closeSettings"
		/>
	</div>
</template>
