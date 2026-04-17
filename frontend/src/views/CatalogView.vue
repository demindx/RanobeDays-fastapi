<script setup>
	import { computed, ref } from 'vue'
	import HomeHeader from '../components/home/HomeHeader.vue'
	import MobileBottomNav from '../components/home/MobileBottomNav.vue'
	import DefaultFooter from '../components/home/DefaultFooter.vue'
	import CatalogLayout from '../components/catalog/CatalogLayout.vue'
	import CatalogToolbar from '../components/catalog/CatalogToolbar.vue'
	import CatalogFiltersPanel from '../components/catalog/CatalogFiltersPanel.vue'
	import CatalogGrid from '../components/catalog/CatalogGrid.vue'
	import CatalogList from '../components/catalog/CatalogList.vue'
	import { useAuth } from '../composables/useAuth'
	import { useCatalogFilters } from '../composables/useCatalogFilters'
	import { catalogNovels, catalogFilterOptions } from '../mocks/catalogData'

	const { isAuthenticated, user, hasUnreadNotifications } = useAuth()
	const viewMode = ref('grid')
	const mobileFiltersOpen = ref(false)

	const novelsRef = computed(() => catalogNovels)
	const { filters, filteredNovels, activeFiltersCount, toggleValue, resetFilters } = useCatalogFilters(novelsRef)

	const setViewMode = (mode) => {
		viewMode.value = mode
	}

	const closeMobileFilters = () => {
		mobileFiltersOpen.value = false
	}

	const handleResetFilters = () => {
		resetFilters()
	}
</script>

<template>
	<main class="min-h-screen bg-zinc-950 text-white">
		<div class="mx-auto flex w-full max-w-6xl flex-col gap-4 px-3 py-4 pb-24 sm:px-4 sm:py-6 md:gap-6 md:px-6 md:py-8 md:pb-8">
			<HomeHeader
				:is-authenticated="isAuthenticated"
				:user="user"
				:has-unread-notifications="hasUnreadNotifications"
			/>

			<CatalogLayout :filters-open="mobileFiltersOpen" @close-filters="closeMobileFilters">
				<template #content>
					<div class="space-y-3">
						<CatalogToolbar
							:view-mode="viewMode"
							:total="filteredNovels.length"
							:active-filters="activeFiltersCount"
							@change-view="setViewMode"
							@open-filters="mobileFiltersOpen = true"
						/>

						<p
							v-if="!filteredNovels.length"
							class="rounded-xl border border-dashed border-zinc-700 bg-zinc-900/50 px-4 py-8 text-sm text-zinc-400"
						>
							Ничего не найдено. Попробуйте ослабить фильтры или сбросить их.
						</p>
						<CatalogGrid v-else-if="viewMode === 'grid'" :novels="filteredNovels" />
						<CatalogList v-else :novels="filteredNovels" />
					</div>
				</template>

				<template #filters>
					<CatalogFiltersPanel
						:filters="filters"
						:options="catalogFilterOptions"
						@toggle="(filterKey, mode, value) => toggleValue(filterKey, mode, value)"
						@reset="handleResetFilters"
					/>
				</template>
			</CatalogLayout>

			<DefaultFooter />
		</div>

		<MobileBottomNav
			:is-authenticated="isAuthenticated"
			:user="user"
			:has-unread-notifications="hasUnreadNotifications"
		/>
	</main>
</template>
