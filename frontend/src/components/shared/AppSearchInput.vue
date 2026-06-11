<script setup>
import AppInput from './AppInput.vue'
import SearchIcon from '../icons/SearchIcon.vue'
</script>

<template>
  <div class="relative w-full">
    <AppInput
      type="text"
      placeholder="Поиск новел..."
      class="w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2 pl-3 pr-10 text-sm text-white outline-none transition focus:border-emerald-300"
      v-bind="$attrs"
    />
    <SearchIcon
      class="pointer-events-none absolute right-2 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-300 [&>svg>path]:fill-current"
    />
  </div>
</template>
