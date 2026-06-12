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
const filtersOpen = ref(false)

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

const toggleFilters = () => {
  filtersOpen.value = !filtersOpen.value
}

const handleResetFilters = () => {
  resetFilters()
}

const onTagClick = (value, filterKey) => {
  const target = filters[filterKey]
  if (!target) return
  target.include = [value]
  target.exclude = []
}
</script>

<template>
  <div>
    <CatalogLayout :filters-open="filtersOpen" @close-filters="filtersOpen = false">
      <template #content>
        <div class="space-y-3">
          <CatalogToolbar
            :view-mode="viewMode"
            :total="filteredNovels.length"
            :active-filters="activeFiltersCount"
            :filters-open="filtersOpen"
            @update:view-mode="viewMode = $event"
            @toggle-filters="toggleFilters"
          />

          <AppEmptyState v-if="!filteredNovels.length">
            Ничего не найдено. Попробуйте ослабить фильтры или сбросить их.
          </AppEmptyState>
          <AppSectionSwitchTransition v-else>
            <component
              :is="currentCatalogComponent"
              :key="viewMode"
              :novels="filteredNovels"
              :filters-open="filtersOpen"
              :on-tag-click="viewMode === 'list' ? onTagClick : undefined"
            />
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
