<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppInput from './AppInput.vue'
import SearchIcon from '../icons/SearchIcon.vue'
import { debounce } from '../../utils/debounce'

const route = useRoute()
const router = useRouter()
const query = ref(String(route.query.search || ''))

const applySearch = debounce((value) => {
  if (route.name !== 'catalog') return
  const search = value || undefined
  router.replace({ query: { ...route.query, search } })
}, 300)

watch(query, (value) => applySearch(value))

const submit = () => {
  const value = query.value.trim()
  router.push({ path: '/catalog', query: value ? { search: value } : {} })
}
</script>

<template>
  <div class="relative w-full">
    <AppInput
      v-model="query"
      type="text"
      placeholder="Поиск новел..."
      class="w-full rounded-lg border border-zinc-700 bg-zinc-800 py-2 pl-3 pr-10 text-sm text-white outline-none transition focus:border-emerald-300"
      @keyup.enter="submit"
    />
    <SearchIcon
      class="pointer-events-none absolute right-2 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-300 [&>svg>path]:fill-current"
    />
  </div>
</template>
