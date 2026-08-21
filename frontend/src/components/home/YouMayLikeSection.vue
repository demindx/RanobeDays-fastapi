<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import SectionTitle from '../ui/SectionTitle.vue'
import AppEmptyState from '../shared/AppEmptyState.vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})

const resolvedItems = computed(() =>
  props.items.map((item) => ({
    ...item,
    href: item.href && item.href !== '#' ? item.href : `/novel/${item.novelId || item.id}`,
  })),
)
</script>

<template>
  <section class="space-y-4">
    <SectionTitle title="Вам может понравиться" subtitle="Персональные рекомендации" />

    <AppEmptyState v-if="!props.items.length" compact> Пока нет рекомендаций. </AppEmptyState>

    <div v-else class="space-y-2">
      <component
        :is="item.href.startsWith('/') ? RouterLink : 'a'"
        v-for="(item, index) in resolvedItems"
        :key="item.id"
        :to="item.href.startsWith('/') ? item.href : undefined"
        :href="item.href.startsWith('/') ? undefined : item.href"
        :class="[
          'block rounded-xl border border-zinc-700/70 bg-zinc-900/70 p-3 transition hover:bg-zinc-800/70 active:scale-[0.99]',
          index % 3 === 0
            ? 'hover:border-emerald-300/60'
            : index % 3 === 1
              ? 'hover:border-lime-300/60'
              : 'hover:border-green-300/60',
        ]"
      >
        <h3 class="line-clamp-2 text-sm font-semibold text-white">{{ item.title }}</h3>
        <p class="mt-1 text-xs text-zinc-400">{{ item.genre }} • ★ {{ item.rating }}</p>
      </component>
    </div>
  </section>
</template>
