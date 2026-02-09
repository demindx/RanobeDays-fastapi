<script setup>
import { RouterView } from 'vue-router';
import Header from './components/Header.vue';
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <Header />
    <main class="flex-grow">
      <RouterView />
    </main>
  </div>
</template>

<style>
@import "./assets/_variables.css";
</style>
