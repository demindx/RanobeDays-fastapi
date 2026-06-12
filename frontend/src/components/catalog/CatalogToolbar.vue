<script setup>
import AppButton from '../shared/AppButton.vue'
import AppPanel from '../shared/AppPanel.vue'
import AppViewModeToggle from '../shared/AppViewModeToggle.vue'

const props = defineProps({
  viewMode: {
    type: String,
    required: true,
  },
  total: {
    type: Number,
    default: 0,
  },
  activeFilters: {
    type: Number,
    default: 0,
  },
  filtersOpen: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:viewMode', 'toggle-filters'])
</script>

<template>
  <AppPanel class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
    <div>
      <h1 class="text-lg font-semibold text-white">Каталог новел</h1>
      <p class="text-xs text-zinc-400">
        Найдено: {{ props.total }}
        <span v-if="props.activeFilters"> · Активных фильтров: {{ props.activeFilters }}</span>
      </p>
    </div>

    <div class="flex items-center gap-2">
      <AppButton variant="neutral" size="sm" @click="emit('toggle-filters')">
        {{ props.filtersOpen ? 'Закрыть' : 'Фильтры' }}
      </AppButton>

      <AppViewModeToggle
        :model-value="props.viewMode"
        @update:model-value="emit('update:viewMode', $event)"
      />
    </div>
  </AppPanel>
</template>
