<script setup>
import { RouterView } from 'vue-router';
import Header from './components/Header.vue';
</script>

<template>
  <div class="flex flex-col min-h-screen bg-[#232323]">
    <Header />
    <main class="flex-grow">
      <RouterView />
    </main>
  </div>
</template>

<style>
@import "./assets/_variables.css";

/* Apply background color to the entire page */
html, body {
  background-color: #232323;
}
</style>
