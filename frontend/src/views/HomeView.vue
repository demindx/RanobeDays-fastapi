<script setup>
	import HomeHeader from '../components/home/HomeHeader.vue'
	import MobileBottomNav from '../components/home/MobileBottomNav.vue'
	import NovelCarouselSection from '../components/home/NovelCarouselSection.vue'
	import LatestUpdatesSection from '../components/home/LatestUpdatesSection.vue'
	import ContinueReadingSection from '../components/home/ContinueReadingSection.vue'
	import YouMayLikeSection from '../components/home/YouMayLikeSection.vue'
	import DefaultFooter from '../components/home/DefaultFooter.vue'
	import { featuredNovels, latestUpdates, continueReading, youMayLike } from '../mocks/homePageData'

	const isAuthenticated = false
</script>

<template>
	<main class="min-h-screen bg-zinc-950 text-white">
		<div class="mx-auto flex w-full max-w-6xl flex-col gap-6 px-3 py-4 pb-24 sm:px-4 sm:py-6 md:gap-8 md:px-6 md:py-8 md:pb-8">
			<HomeHeader :is-authenticated="isAuthenticated" />
			<NovelCarouselSection :novels="featuredNovels" />
			<ContinueReadingSection :items="continueReading" />

			<div class="grid gap-6 lg:grid-cols-10">
				<div class="lg:col-span-7">
					<LatestUpdatesSection :updates="latestUpdates" />
				</div>
				<div class="lg:col-span-3">
					<YouMayLikeSection :items="youMayLike" />
				</div>
			</div>

			<DefaultFooter />
		</div>

		<MobileBottomNav :is-authenticated="isAuthenticated" />
	</main>
</template>
