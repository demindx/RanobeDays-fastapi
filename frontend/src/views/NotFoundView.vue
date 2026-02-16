<script setup>
import SectionAccentTitle from '@/components/common/SectionAccentTitle.vue'
</script>

<template>
  <section class="container mx-auto px-4 py-8 text-white">
    <SectionAccentTitle
      as="h1"
      class="mb-3"
    >
      404
    </SectionAccentTitle>
    <p class="text-gray-300 mb-4">
      Страница не найдена.
    </p>
    <router-link
      to="/"
      class="inline-flex px-4 py-2 rounded-md bg-[var(--first-color)] text-[var(--foreground-color)] font-semibold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rd-accent focus-visible:ring-offset-2 focus-visible:ring-offset-rd-bg"
    >
      На главную
    </router-link>
  </section>
</template>
