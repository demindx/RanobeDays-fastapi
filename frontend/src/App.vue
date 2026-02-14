<script setup>
import { RouterView } from 'vue-router'
import Header from './components/layout/Header.vue'
</script>

<template>
  <div class="flex flex-col min-h-screen bg-[var(--background-color)]">
    <Header />
    <main class="flex-grow md:pt-0 pt-[60px] pb-[70px] md:pb-0">
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
