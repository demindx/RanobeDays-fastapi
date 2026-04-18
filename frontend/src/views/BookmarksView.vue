<script setup>
	import HomeHeader from '../components/home/HomeHeader.vue'
	import MobileBottomNav from '../components/home/MobileBottomNav.vue'
	import DefaultFooter from '../components/home/DefaultFooter.vue'
	import BookmarksToolbar from '../components/bookmarks/BookmarksToolbar.vue'
	import BookmarksContent from '../components/bookmarks/BookmarksContent.vue'
	import BookmarksSettingsModal from '../components/bookmarks/BookmarksSettingsModal.vue'
	import { useAuth } from '../composables/useAuth'
	import { useBookmarks } from '../composables/useBookmarks'

	const { isAuthenticated, user, hasUnreadNotifications } = useAuth()
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
	<main class="min-h-screen bg-zinc-950 text-white flex flex-col">
		<div class="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-4 px-3 py-4 pb-24 sm:px-4 sm:py-6 md:gap-6 md:px-6 md:py-8 md:pb-8">
			<HomeHeader
				:is-authenticated="isAuthenticated"
				:user="user"
				:has-unread-notifications="hasUnreadNotifications"
			/>

			<BookmarksToolbar
				:bookmarks="bookmarks"
				:active-id="activeBookmarkId"
				@select="setActive"
				@open-settings="openSettings"
			/>

			<BookmarksContent :bookmark="activeBookmark" @open-settings="openSettings" />

			<div class="mt-auto">
				<DefaultFooter />
			</div>
		</div>

		<MobileBottomNav
			:is-authenticated="isAuthenticated"
			:user="user"
			:has-unread-notifications="hasUnreadNotifications"
		/>

		<BookmarksSettingsModal
			:open="isSettingsOpen"
			:bookmarks="bookmarks"
			:on-toggle-privacy="togglePrivacy"
			:on-rename="renameBookmark"
			:on-create="createBookmark"
			@close="closeSettings"
		/>
	</main>
</template>
