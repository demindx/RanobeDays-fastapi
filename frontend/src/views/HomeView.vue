<script setup>
	import NovelCarouselSection from '../components/home/NovelCarouselSection.vue'
	import LatestUpdatesSection from '../components/home/LatestUpdatesSection.vue'
	import ContinueReadingSection from '../components/home/ContinueReadingSection.vue'
	import YouMayLikeSection from '../components/home/YouMayLikeSection.vue'
	import { featuredNovels, latestUpdates, continueReading, youMayLike } from '../mocks/homePageData'
</script>

<template>
	<div class="flex flex-col gap-6 md:gap-8">
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
	</div>
</template>
