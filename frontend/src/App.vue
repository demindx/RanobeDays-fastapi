<script setup>
import { RouterView } from 'vue-router'
import Header from './components/layout/Header.vue'
</script>

<template>
  <div class="flex flex-col min-h-screen bg-[var(--background-color)]">
    <a
      href="#main-content"
      class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] focus:rounded-md focus:bg-rd-accent focus:px-3 focus:py-2 focus:font-semibold focus:text-rd-text-strong"
    >
      Перейти к основному контенту
    </a>
    <Header />
    <main
      id="main-content"
      class="flex-grow pt-[calc(60px+env(safe-area-inset-top))] pb-[calc(70px+env(safe-area-inset-bottom))] md:pt-0 md:pb-0"
      tabindex="-1"
    >
      <RouterView />
    </main>
  </div>
</template>

<style>
@import './assets/_variables.css';
@import './assets/_fonts.css';

/* Apply background color to the entire page */
html,
body {
  background-color: var(--background-color);
}

h1,
h2,
h3 {
  font-family: var(--font-display);
}
</style>
