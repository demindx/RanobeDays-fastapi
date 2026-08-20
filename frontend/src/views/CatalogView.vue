<script setup>
import { computed, onMounted, ref } from 'vue'
import CatalogLayout from '../components/catalog/CatalogLayout.vue'
import CatalogToolbar from '../components/catalog/CatalogToolbar.vue'
import CatalogFiltersPanel from '../components/catalog/CatalogFiltersPanel.vue'
import CatalogGrid from '../components/catalog/CatalogGrid.vue'
import CatalogList from '../components/catalog/CatalogList.vue'
import AppEmptyState from '../components/shared/AppEmptyState.vue'
import AppSectionSwitchTransition from '../components/shared/AppSectionSwitchTransition.vue'
import { useCatalogFilters } from '../composables/useCatalogFilters'
import { fetchNovels } from '../api/novels'
import { fetchCategories } from '../api/categories'
import { fetchLanguages } from '../api/languages'
import { fetchCountries } from '../api/countries'
import { mapNovelsList } from '../api/mapper'

const viewMode = ref('grid')
const filtersOpen = ref(false)

const novels = ref([])
const filterOptions = ref({
  releaseYears: [],
  ageRatings: [],
  genres: [],
  tags: [],
  originalLanguages: [],
  translationLanguages: [],
})

const uniq = (values) => Array.from(new Set(values.filter(Boolean)))

const buildFilterOptions = (novels, categories, languages, countries) => ({
  releaseYears: uniq(novels.map((item) => item.releaseYear)).sort((a, b) => b - a),
  ageRatings: uniq(novels.map((item) => item.ageRating)),
  genres: uniq(categories.filter((c) => c.type === 'genre').map((c) => c.name)).sort(),
  tags: uniq(categories.filter((c) => c.type === 'tag').map((c) => c.name)).sort(),
  originalLanguages: uniq(languages.map((l) => l.name)).sort(),
  translationLanguages: uniq(countries.map((c) => c.name)).sort(),
})

onMounted(async () => {
  const [novelsData, categories, languages, countries] = await Promise.all([
    fetchNovels(),
    fetchCategories(),
    fetchLanguages(),
    fetchCountries(),
  ])
  novels.value = mapNovelsList(novelsData)
  filterOptions.value = buildFilterOptions(novels.value, categories, languages, countries)
})

const novelsRef = computed(() => novels.value)
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
            />
          </AppSectionSwitchTransition>
        </div>
      </template>

      <template #filters>
        <CatalogFiltersPanel
          :filters="filters"
          :options="filterOptions"
          @toggle="(filterKey, mode, value) => toggleValue(filterKey, mode, value)"
          @set-year-range="(bound, value) => setReleaseYearRange(bound, value)"
          @reset="handleResetFilters"
        />
      </template>
    </CatalogLayout>
  </div>
</template>
