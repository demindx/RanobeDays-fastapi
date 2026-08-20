<script setup>
import AppErrorBoundary from '../components/shared/AppErrorBoundary.vue'
</script>

<template>
  <AppErrorBoundary>
    <RouterView />
  </AppErrorBoundary>
</template>
