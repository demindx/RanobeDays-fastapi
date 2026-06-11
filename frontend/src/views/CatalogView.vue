<script setup>
import { computed, ref } from 'vue'
import CatalogLayout from '../components/catalog/CatalogLayout.vue'
import CatalogToolbar from '../components/catalog/CatalogToolbar.vue'
import CatalogFiltersPanel from '../components/catalog/CatalogFiltersPanel.vue'
import CatalogGrid from '../components/catalog/CatalogGrid.vue'
import CatalogList from '../components/catalog/CatalogList.vue'
import AppEmptyState from '../components/shared/AppEmptyState.vue'
import AppSectionSwitchTransition from '../components/shared/AppSectionSwitchTransition.vue'
import { useCatalogFilters } from '../composables/useCatalogFilters'
import { catalogNovels, catalogFilterOptions } from '../mocks/catalogData'

const viewMode = ref('grid')
const mobileFiltersOpen = ref(false)

const novelsRef = computed(() => catalogNovels)
const {
  filters,
  filteredNovels,
  activeFiltersCount,
  setReleaseYearRange,
  toggleValue,
  resetFilters,
} = useCatalogFilters(novelsRef)
const currentCatalogComponent = computed(() =>
  viewMode.value === 'grid' ? CatalogGrid : CatalogList,
)

const closeMobileFilters = () => {
  mobileFiltersOpen.value = false
}

const handleResetFilters = () => {
  resetFilters()
}
</script>

<template>
  <div>
    <CatalogLayout :filters-open="mobileFiltersOpen" @close-filters="closeMobileFilters">
      <template #content>
        <div class="space-y-3">
          <CatalogToolbar
            :view-mode="viewMode"
            :total="filteredNovels.length"
            :active-filters="activeFiltersCount"
            @update:view-mode="viewMode = $event"
            @open-filters="mobileFiltersOpen = true"
          />

          <AppEmptyState v-if="!filteredNovels.length">
            Ничего не найдено. Попробуйте ослабить фильтры или сбросить их.
          </AppEmptyState>
          <AppSectionSwitchTransition v-else>
            <component :is="currentCatalogComponent" :key="viewMode" :novels="filteredNovels" />
          </AppSectionSwitchTransition>
        </div>
      </template>

      <template #filters>
        <CatalogFiltersPanel
          :filters="filters"
          :options="catalogFilterOptions"
          @toggle="(filterKey, mode, value) => toggleValue(filterKey, mode, value)"
          @set-year-range="(bound, value) => setReleaseYearRange(bound, value)"
          @reset="handleResetFilters"
        />
      </template>
    </CatalogLayout>
  </div>
</template>
